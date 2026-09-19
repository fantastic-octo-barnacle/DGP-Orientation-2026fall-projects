use crate::{Service, error};
use rocket::data::ToByteUnit;
use rocket::http::{Method, Status};
use rocket::route::{Handler, Outcome};
use rocket::serde::json::Json;
use rocket::{Build, Data, Request, Rocket, Route};
use serde_json::Value;
use std::sync::Arc;

#[derive(Clone)]
struct Dispatch(Arc<Service>);

#[rocket::async_trait]
impl Handler for Dispatch {
    async fn handle<'r>(&self, request: &'r Request<'_>, data: Data<'r>) -> Outcome<'r> {
        let method = request.method().as_str().to_owned();
        let path = request.uri().path().as_str().to_owned();
        let authorization = request
            .headers()
            .get_one("Authorization")
            .unwrap_or("")
            .to_owned();
        let body = if matches!(request.method(), Method::Post | Method::Put) {
            let bytes = match data.open(512.kibibytes()).into_bytes().await {
                Ok(bytes) if bytes.is_complete() => bytes,
                Ok(_) => {
                    return Outcome::from(
                        request,
                        (
                            Status::PayloadTooLarge,
                            Json(error(413, "Request body too large").1),
                        ),
                    );
                }
                Err(_) => {
                    return Outcome::from(
                        request,
                        (
                            Status::BadRequest,
                            Json(error(400, "Cannot read request").1),
                        ),
                    );
                }
            };
            match serde_json::from_slice::<Value>(&bytes) {
                Ok(body) => body,
                Err(_) => {
                    return Outcome::from(
                        request,
                        (
                            Status::BadRequest,
                            Json(error(400, "Expected UTF-8 JSON").1),
                        ),
                    );
                }
            }
        } else {
            Value::Null
        };
        // Password hashing is blocking. No state lock is held across an await.
        let service = self.0.clone();
        let (status, body) = rocket::tokio::task::spawn_blocking(move || {
            service.handle(&method, &path, &body, &authorization)
        })
        .await
        .unwrap_or_else(|_| error(500, "Handler failed"));
        Outcome::from(request, (Status::new(status), Json(body)))
    }
}

pub fn create_app() -> Rocket<Build> {
    let dispatch = Dispatch(Arc::new(Service::default()));
    let routes: Vec<_> = [
        Method::Get,
        Method::Post,
        Method::Put,
        Method::Delete,
        Method::Patch,
        Method::Head,
        Method::Options,
    ]
    .into_iter()
    .map(|method| Route::new(method, "/<_..>", dispatch.clone()))
    .collect();
    rocket::build().mount("/", routes)
}
