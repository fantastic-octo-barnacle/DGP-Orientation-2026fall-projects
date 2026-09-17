use serde_json::{Value, json};
use std::io::{self, BufRead, BufReader, Write};
use std::net::TcpStream;

/// 每次调用建立一个连接，发送固定 ping 并检查对应响应。
pub fn ping(address: &str) -> io::Result<Value> {
    let mut stream = TcpStream::connect(address)?;
    let request = json!({"id": 1, "action": "ping"});
    writeln!(stream, "{request}")?;
    let mut reader = BufReader::new(stream);
    let mut line = String::new();
    if reader.read_line(&mut line)? == 0 {
        return Err(io::Error::new(io::ErrorKind::UnexpectedEof, "peer closed"));
    }
    let response: Value = serde_json::from_str(&line)
        .map_err(|error| io::Error::new(io::ErrorKind::InvalidData, error))?;
    if response["id"] != 1 || !response["ok"].is_boolean() {
        return Err(io::Error::new(
            io::ErrorKind::InvalidData,
            "response id or ok is invalid",
        ));
    }
    Ok(response)
}
