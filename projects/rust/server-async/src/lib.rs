pub mod protocol;
use tokio::io::{AsyncBufReadExt, AsyncWriteExt, BufReader};
use tokio::net::TcpStream;

/// 异步读写不自动带来跨连接并发；基线每连接只处理一条消息。
pub async fn serve_once(stream: TcpStream) -> std::io::Result<()> {
    let (reader, mut writer) = stream.into_split();
    let mut reader = BufReader::new(reader);
    let mut line = String::new();
    if reader.read_line(&mut line).await? == 0 {
        return Ok(());
    }
    let response = protocol::handle(&line);
    writer.write_all(format!("{response}\n").as_bytes()).await?;
    Ok(())
}
