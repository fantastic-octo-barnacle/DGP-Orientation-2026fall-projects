use axum::{
    Json, Router,
    body::to_bytes,
    extract::{Request, State},
    http::StatusCode,
    response::IntoResponse,
};
use clap::Parser;
use rm_server_async::{Service, error};
use serde_json::Value;
use std::sync::Arc;

#[derive(Parser)]
struct Args {
    #[arg(long, default_value = "127.0.0.1:7878")]
    address: String,
}
async fn dispatch(State(service): State<Arc<Service>>, request: Request) -> impl IntoResponse {
    let method = request.method().as_str().to_owned();
    let path = request.uri().path().to_owned();
    let authorization = request
        .headers()
        .get("Authorization")
        .and_then(|v| v.to_str().ok())
        .unwrap_or("")
        .to_owned();
    let body = if matches!(method.as_str(), "POST" | "PUT") {
        let bytes = match to_bytes(request.into_body(), 512 * 1024).await {
            Ok(bytes) => bytes,
            Err(_) => {
                return (
                    StatusCode::PAYLOAD_TOO_LARGE,
                    Json(error(413, "Request body too large").1),
                );
            }
        };
        match serde_json::from_slice::<Value>(&bytes) {
            Ok(value) => value,
            Err(_) => {
                return (
                    StatusCode::BAD_REQUEST,
                    Json(error(400, "Expected UTF-8 JSON").1),
                );
            }
        }
    } else {
        Value::Null
    };
    // Password hashing is blocking. No state lock is held across an await.
    // Task: handle delay asynchronously before entering this blocking worker.
    let result =
        tokio::task::spawn_blocking(move || service.handle(&method, &path, &body, &authorization))
            .await
            .unwrap_or_else(|_| error(500, "Handler failed"));
    (StatusCode::from_u16(result.0).unwrap(), Json(result.1))
}
#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args = Args::parse();
    let listener = tokio::net::TcpListener::bind(&args.address).await?;
    println!("LISTENING {}", listener.local_addr()?);
    let app = Router::new()
        .fallback(dispatch)
        .with_state(Arc::new(Service::default()));
    // Task: request deadline, bounded graceful shutdown and cancellation.
    axum::serve(listener, app).await?;
    Ok(())
}
