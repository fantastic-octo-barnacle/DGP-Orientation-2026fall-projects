//! 显式运行的阶段自查，不会随 cargo test 执行，也不检查候选人的命令行界面。
use serde_json::{Value, json};
use std::io::{BufRead, BufReader, Write};
use std::net::TcpStream;
use std::time::Duration;

fn call(address: &str, request: Value) -> Value {
    let mut stream = TcpStream::connect(address).expect("connect");
    stream
        .set_read_timeout(Some(Duration::from_secs(3)))
        .unwrap();
    writeln!(stream, "{request}").unwrap();
    let mut line = String::new();
    BufReader::new(stream).read_line(&mut line).unwrap();
    let response: Value = serde_json::from_str(&line).expect("JSON response");
    assert_eq!(response["id"], request["id"]);
    assert_eq!(response["ok"], true, "{response}");
    response["data"].clone()
}
fn main() {
    let args: Vec<String> = std::env::args().collect();
    let stage = args.get(1).map(String::as_str).unwrap_or("baseline");
    let address = args.get(2).map(String::as_str).unwrap_or("127.0.0.1:7878");
    assert_eq!(call(address, json!({"id":1,"action":"ping"})), "pong");
    match stage {
        "baseline" => {}
        "actions" => {
            assert_eq!(
                call(address, json!({"id":2,"action":"echo","data":"hello"})),
                "hello"
            );
            assert_eq!(
                call(
                    address,
                    json!({"id":3,"action":"delay","milliseconds":50,"data":"later"})
                ),
                "later"
            );
        }
        _ => panic!("use baseline or actions"),
    }
    println!("PASS: {stage}; continue with acceptance.md");
}
