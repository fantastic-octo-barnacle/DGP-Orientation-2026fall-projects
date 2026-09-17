use serde_json::{Value, json};

pub const MAX_ID: u64 = 9_007_199_254_740_991;

pub fn failure(id: Value, code: &str, message: &str) -> Value {
    json!({"id": id, "ok": false, "error": {"code": code, "message": message}})
}

/// 起始服务只实现 ping。其他动作在项目任务中逐步加入。
pub fn handle(line: &str) -> Value {
    let request: Value = match serde_json::from_str(line) {
        Ok(value) => value,
        Err(_) => return failure(Value::Null, "invalid_json", "expected JSON"),
    };
    let Some(object) = request.as_object() else {
        return failure(Value::Null, "invalid_request", "expected object");
    };
    let Some(id) = object
        .get("id")
        .and_then(Value::as_u64)
        .filter(|id| *id <= MAX_ID)
    else {
        return failure(Value::Null, "invalid_request", "invalid id");
    };
    let Some(action) = object.get("action").and_then(Value::as_str) else {
        return failure(json!(id), "invalid_request", "action must be a string");
    };
    if action != "ping" {
        return failure(json!(id), "unknown_action", "action is not supported");
    }
    if object.len() != 2 {
        return failure(json!(id), "invalid_request", "extra fields");
    }
    json!({"id": id, "ok": true, "data": "pong"})
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn ping_and_errors() {
        assert_eq!(handle(r#"{"id":1,"action":"ping"}"#)["data"], "pong");
        assert_eq!(handle("{")["error"]["code"], "invalid_json");
        assert_eq!(
            handle(r#"{"id":true,"action":"ping"}"#)["error"]["code"],
            "invalid_request"
        );
        assert_eq!(
            handle(r#"{"id":1,"action":"other"}"#)["error"]["code"],
            "unknown_action"
        );
    }
}
