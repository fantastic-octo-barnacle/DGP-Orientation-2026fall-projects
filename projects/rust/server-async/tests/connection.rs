use tokio::io::{AsyncBufReadExt, AsyncWriteExt, BufReader};
use tokio::net::{TcpListener, TcpStream};

#[tokio::test]
async fn one_request_then_close() {
    tokio::time::timeout(std::time::Duration::from_secs(3), check_connection())
        .await
        .expect("测试超过 3 秒：检查响应、连接关闭和任务结束；实现连续交互后需更新关闭断言");
}

async fn check_connection() {
    let listener = TcpListener::bind("127.0.0.1:0").await.unwrap();
    let address = listener.local_addr().unwrap();
    let worker = tokio::spawn(async move {
        let (stream, _) = listener.accept().await.unwrap();
        rm_server_async::serve_once(stream).await.unwrap();
    });
    let mut stream = TcpStream::connect(address).await.unwrap();
    stream
        .write_all(b"{\"id\":7,\"action\":\"ping\"}\n")
        .await
        .unwrap();
    let mut reader = BufReader::new(stream);
    let mut line = String::new();
    reader.read_line(&mut line).await.unwrap();
    assert_eq!(
        serde_json::from_str::<serde_json::Value>(&line).unwrap()["data"],
        "pong"
    );
    line.clear();
    assert_eq!(reader.read_line(&mut line).await.unwrap(), 0);
    worker.await.unwrap();
}
