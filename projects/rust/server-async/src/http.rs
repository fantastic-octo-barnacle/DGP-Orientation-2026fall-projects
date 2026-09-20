use crate::{ROUTES, Service, error, route_error};
use rocket::data::ToByteUnit;
use rocket::fairing::{Fairing, Info, Kind};
use rocket::http::{Method, Status};
use rocket::route::{Handler, Outcome};
use rocket::serde::json::Json;
use rocket::{Build, Data, Orbit, Request, Response, Rocket, Route};
use serde_json::Value;
use std::sync::Arc;
use std::time::Instant;

struct ConsoleOutput;

#[rocket::async_trait]
impl Fairing for ConsoleOutput {
    fn info(&self) -> Info {
        Info {
            name: "Console output",
            kind: Kind::Liftoff | Kind::Request | Kind::Response,
        }
    }

    async fn on_liftoff(&self, rocket: &Rocket<Orbit>) {
        let address = std::net::SocketAddr::new(rocket.config().address, rocket.config().port);
        eprintln!("Listening on http://{address}");
        eprintln!("Press Ctrl+C to exit. All in-memory data is lost on exit.");
        eprintln!("Routes:");
        for (method, path) in ROUTES {
            eprintln!("  {method} {path}");
        }
    }

    async fn on_request(&self, request: &mut Request<'_>, _: &mut Data<'_>) {
        request.local_cache(Instant::now);
    }

    async fn on_response<'r>(&self, request: &'r Request<'_>, response: &mut Response<'r>) {
        let elapsed = request.local_cache(Instant::now).elapsed();
        eprintln!(
            "{} {:?} -> {} {:.1}ms",
            request.method(),
            request.uri().path().as_str(),
            response.status().code,
            elapsed.as_secs_f64() * 1000.0,
        );
    }
}

#[derive(Clone)]
struct Dispatch(Arc<Service>);

#[rocket::async_trait]
impl Handler for Dispatch {
    async fn handle<'r>(&self, request: &'r Request<'_>, data: Data<'r>) -> Outcome<'r> {
        let method = request.method().as_str().to_owned();
        let path = request.uri().path().as_str().to_owned();
        if let Some(status) = route_error(&method, &path) {
            return Outcome::from(
                request,
                (
                    Status::new(status),
                    Json(
                        error(
                            status,
                            if status == 404 {
                                "Not found"
                            } else {
                                "Method not allowed"
                            },
                        )
                        .1,
                    ),
                ),
            );
        }
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
        Method::Trace,
        Method::Connect,
    ]
    .into_iter()
    .map(|method| Route::new(method, "/<_..>", dispatch.clone()))
    .collect();
    rocket::build().attach(ConsoleOutput).mount("/", routes)
}
