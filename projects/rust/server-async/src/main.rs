use tokio::net::TcpListener;
#[tokio::main]
async fn main() -> std::io::Result<()> {
    let address = std::env::args()
        .nth(1)
        .unwrap_or_else(|| "127.0.0.1:7878".to_owned());
    let listener = TcpListener::bind(&address).await?;
    println!("LISTENING {}", listener.local_addr()?);
    loop {
        let (stream, _) = listener.accept().await?;
        // 明确等待当前连接完成；候选人在并发阶段改变任务组织方式。
        if let Err(error) = rm_server_async::serve_once(stream).await {
            eprintln!("连接结束: {error}");
        }
    }
}
