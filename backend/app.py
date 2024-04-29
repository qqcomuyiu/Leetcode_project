from flask import Flask, jsonify
from flask_socketio import SocketIO, emit
import threading
import time
import api  # 确保 api.py 在同一目录下

app = Flask(__name__)
socketio = SocketIO(app)
data = {}

@app.route('/api/data')
def get_data():
    return jsonify(data)

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('live_update', {'data': 'Connected to live transit updates'})

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

def send_live_updates():
    """定期从API获取数据并发送实时交通更新给所有连接的客户端"""
    while True:
        global data
        data = api.combine_data()  # 获取实时和静态数据的组合
        socketio.emit('live_update', {'data': data})
        time.sleep(60)  # 每60秒更新一次

if __name__ == '__main__':
    # 使用后台线程运行实时数据更新任务
    thread = threading.Thread(target=send_live_updates)
    thread.daemon = True
    thread.start()
    
    socketio.run(app, debug=True,allow_unsafe_werkzeug=True)
