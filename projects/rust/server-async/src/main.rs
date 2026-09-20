use clap::Parser;
use rm_server_async::http::create_app;
use std::net::SocketAddr;

#[derive(Parser)]
struct Args {
    #[arg(long, default_value = "127.0.0.1:7878")]
    address: SocketAddr,
}

#[rocket::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args = Args::parse();
    let app = create_app();
    let config = app
        .figment()
        .clone()
        .merge(("address", args.address.ip()))
        .merge(("port", args.address.port()))
        .merge(("log_level", "critical"));
    app.configure(config).launch().await?;
    Ok(())
}
