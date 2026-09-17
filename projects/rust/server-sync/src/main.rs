use std::net::TcpListener;
fn main() -> std::io::Result<()> {
    let address = std::env::args()
        .nth(1)
        .unwrap_or_else(|| "127.0.0.1:7878".to_owned());
    let listener = TcpListener::bind(&address)?;
    println!("LISTENING {}", listener.local_addr()?);
    for stream in listener.incoming() {
        match stream {
            Ok(stream) => {
                if let Err(error) = rm_server_sync::serve_once(stream) {
                    eprintln!("连接结束: {error}");
                }
            }
            Err(error) => eprintln!("接受连接失败: {error}"),
        }
    }
    Ok(())
}
