use std::io::{BufRead, BufReader, Write};
use std::net::TcpListener;

#[test]
fn sends_ping_and_reads_matching_response() {
    let listener = TcpListener::bind("127.0.0.1:0").unwrap();
    let address = listener.local_addr().unwrap();
    let worker = std::thread::spawn(move || {
        let (mut stream, _) = listener.accept().unwrap();
        let mut line = String::new();
        BufReader::new(stream.try_clone().unwrap())
            .read_line(&mut line)
            .unwrap();
        let request: serde_json::Value = serde_json::from_str(&line).unwrap();
        assert_eq!(request["action"], "ping");
        writeln!(stream, r#"{{"id":1,"ok":true,"data":"pong"}}"#).unwrap();
    });
    let response = rm_client_sync::ping(&address.to_string()).unwrap();
    assert_eq!(response["data"], "pong");
    worker.join().unwrap();
}
