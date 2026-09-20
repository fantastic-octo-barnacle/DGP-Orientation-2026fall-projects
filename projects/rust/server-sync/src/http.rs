//! Synchronous application assembly and startup.

use crate::{Service, infrastructure};
use rocket::{Build, Rocket};
use std::net::SocketAddr;

pub fn create_app() -> Rocket<Build> {
    with_service(Service::default())
}

/// Inject business settings without changing the HTTP infrastructure.
pub fn with_service(service: Service) -> Rocket<Build> {
    infrastructure::create_app(service)
}

pub fn run(address: SocketAddr, service: Service) -> Result<(), Box<dyn std::error::Error>> {
    infrastructure::run(address, service)
}
