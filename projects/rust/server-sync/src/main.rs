use clap::Parser;
use rm_server_sync::{Service, error};
use serde_json::Value;
use std::io::Read;
use tiny_http::{Header, Response, Server, StatusCode};

#[derive(Parser)]
struct Args {
    #[arg(long, default_value = "127.0.0.1:7878")]
    address: String,
}
fn main() -> Result<(), Box<dyn std::error::Error + Send + Sync>> {
    let args = Args::parse();
    let server = Server::http(&args.address)?;
    println!("LISTENING {}", server.server_addr());
    let service = Service::default();
    // Task: bound request reading and support bounded shutdown.
    for mut request in server.incoming_requests() {
        let method = request.method().as_str().to_owned();
        let path = request.url().split('?').next().unwrap_or("/").to_owned();
        let authorization = request
            .headers()
            .iter()
            .find(|h| h.field.equiv("Authorization"))
            .map(|h| h.value.as_str().to_owned())
            .unwrap_or_default();
        let result = if matches!(method.as_str(), "POST" | "PUT") {
            let mut bytes = Vec::new();
            match request
                .as_reader()
                .take(512 * 1024 + 1)
                .read_to_end(&mut bytes)
            {
                Err(_) => error(400, "Cannot read request"),
                Ok(_) if bytes.len() > 512 * 1024 => error(413, "Request body too large"),
                Ok(_) => match serde_json::from_slice::<Value>(&bytes) {
                    Ok(body) => service.handle(&method, &path, &body, &authorization),
                    Err(_) => error(400, "Expected UTF-8 JSON"),
                },
            }
        } else {
            service.handle(&method, &path, &Value::Null, &authorization)
        };
        let response = Response::from_string(result.1.to_string())
            .with_status_code(StatusCode(result.0))
            .with_header(Header::from_bytes("Content-Type", "application/json").unwrap());
        if let Err(error) = request.respond(response) {
            eprintln!("Response failed: {error}");
        }
    }
    Ok(())
}
