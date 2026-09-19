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
    parse_response(&line, 1)
}

fn parse_response(line: &str, request_id: u64) -> io::Result<Value> {
    let response: Value = serde_json::from_str(line)
        .map_err(|error| io::Error::new(io::ErrorKind::InvalidData, error))?;
    let invalid = || io::Error::new(io::ErrorKind::InvalidData, "invalid response fields or id");
    let object = response.as_object().ok_or_else(invalid)?;
    if object.len() != 3 || object.get("id").and_then(Value::as_u64) != Some(request_id) {
        return Err(invalid());
    }
    match object.get("ok").and_then(Value::as_bool) {
        Some(true) if object.contains_key("data") => {}
        Some(false) => {
            let error = object
                .get("error")
                .and_then(Value::as_object)
                .ok_or_else(invalid)?;
            if error.len() != 2
                || !error.get("code").is_some_and(Value::is_string)
                || !error.get("message").is_some_and(Value::is_string)
            {
                return Err(invalid());
            }
        }
        _ => return Err(invalid()),
    }
    Ok(response)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn validates_response_envelope() {
        for response in [
            json!({"id":1,"ok":true}),
            json!({"id":true,"ok":true,"data":"pong"}),
            json!({"id":1.0,"ok":true,"data":"pong"}),
            json!({"id":2,"ok":true,"data":"pong"}),
            json!({"id":1,"ok":"yes","data":"pong"}),
            json!({"id":1,"ok":true,"data":"pong","extra":1}),
            json!({"id":1,"ok":false,"error":"bad"}),
            json!({"id":1,"ok":false,"error":{"code":"bad"}}),
            json!({"id":1,"ok":false,"error":{"code":1,"message":"bad"}}),
            json!({"id":1,"ok":false,"error":{"code":"bad","message":"bad","extra":1}}),
            json!([]),
        ] {
            assert_eq!(
                parse_response(&response.to_string(), 1).unwrap_err().kind(),
                io::ErrorKind::InvalidData
            );
        }
        for response in [
            json!({"id":1,"ok":true,"data":"pong"}),
            json!({"id":1,"ok":false,"error":{"code":"invalid_request","message":"bad"}}),
        ] {
            assert_eq!(parse_response(&response.to_string(), 1).unwrap(), response);
        }
    }
}
