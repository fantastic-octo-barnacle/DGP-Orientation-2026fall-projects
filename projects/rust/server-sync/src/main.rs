use clap::Parser;
use rm_server_sync::{Service, http};
use std::net::SocketAddr;

#[derive(Parser)]
struct Args {
    #[arg(long, default_value = "127.0.0.1:7878")]
    address: SocketAddr,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args = Args::parse();
    http::run(args.address, Service::default())
}
