fn main() {
    let address = std::env::args()
        .nth(1)
        .unwrap_or_else(|| "127.0.0.1:7878".to_owned());
    match rm_client_sync::ping(&address) {
        Ok(response) => println!("{response}"),
        Err(error) => {
            eprintln!("请求失败: {error}");
            std::process::exit(1);
        }
    }
}
