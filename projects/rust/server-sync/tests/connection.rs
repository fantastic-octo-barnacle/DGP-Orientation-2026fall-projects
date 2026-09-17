use std::io::{BufRead, BufReader, Write};
use std::net::{TcpListener, TcpStream};

#[test]
fn one_request_then_close() {
    let listener = TcpListener::bind("127.0.0.1:0").unwrap();
    let address = listener.local_addr().unwrap();
    let worker = std::thread::spawn(move || {
        let (stream, _) = listener.accept().unwrap();
        rm_server_sync::serve_once(stream).unwrap();
    });
    let mut stream = TcpStream::connect(address).unwrap();
    stream
        .set_read_timeout(Some(std::time::Duration::from_secs(2)))
        .unwrap();
    writeln!(stream, r#"{{"id":7,"action":"ping"}}"#).unwrap();
    let mut reader = BufReader::new(stream);
    let mut line = String::new();
    reader.read_line(&mut line).unwrap();
    assert_eq!(
        serde_json::from_str::<serde_json::Value>(&line).unwrap()["id"],
        7
    );
    line.clear();
    assert_eq!(reader.read_line(&mut line).unwrap(), 0);
    worker.join().unwrap();
}
