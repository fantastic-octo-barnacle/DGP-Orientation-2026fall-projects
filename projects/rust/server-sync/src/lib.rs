pub mod protocol;
use std::io::{self, BufRead, BufReader, Write};
use std::net::TcpStream;

/// 基线每连接只处理一条消息，然后关闭。连续交互属于后续任务。
pub fn serve_once(mut stream: TcpStream) -> io::Result<()> {
    let mut reader = BufReader::new(stream.try_clone()?);
    let mut line = String::new();
    if reader.read_line(&mut line)? == 0 {
        return Ok(());
    }
    let response = protocol::handle(&line);
    writeln!(stream, "{response}")?;
    Ok(())
}
