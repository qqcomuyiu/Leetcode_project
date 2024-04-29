import websocket
import json
import threading

def on_message(ws, message):
    print("Received message:")
    print(json.dumps(json.loads(message), indent=4))

def on_error(ws, error):
    print("Error:", error)

def on_close(ws):
    print("### Connection closed ###")

def on_open(ws):
    print("Connection opened")

def run_websocket():
    websocket.enableTrace(True)
    # 这里的 URL 应匹配您的服务器WebSocket端点
    ws = websocket.WebSocketApp("ws://localhost:5000/live_updates",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()

if __name__ == "__main__":
    # 在一个新线程中运行 WebSocket 客户端，以避免阻塞主线程
    thread = threading.Thread(target=run_websocket)
    thread.start()
