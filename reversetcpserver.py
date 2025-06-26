import socket
import threading
import struct

def handle_client(conn, addr):
    print(f"Connected by {addr}")  # 打印客户端连接信息

    try:
        # 接收 Initialization(type+N 2+4)
        data=conn.recv(6)
        packet_type, N = struct.unpack('!HI', data) # type字段 + N 块数

        # 发送 agree(type 2)
        conn.send(struct.pack('!H', 2))  # type=2

        # N个 reverseRequest
        for _ in range(N):
            # 接收 reverseRequest(type+length+data 2+4+n)
            header = conn.recv(6)  # type+length
            data_type, length = struct.unpack('!HI', header)  # type + length
            data = conn.recv(length).decode('ascii')  # data 解码

            reversed_data=data[::-1]  # 字符串反转
            # print(f"Server: Reversed data: {reversed_data}")  # 调试输出

            # 发送 reverseAnswer(type+length+reverseData 2+4+n)
            conn.send(
                struct.pack('!HI', 4, len(reversed_data))
                + reversed_data.encode('ascii')  # type=4 + length + reverseData
            )
    finally:
        conn.close()  #关闭连接

def start_server(host='0.0.0.0', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))  # 绑定IP和端口
        s.listen()  # 开始监听
        print(f"Server listening on {host}:{port}")

        # 接收客户端连接
        while True:
            conn, addr=s.accept()  # 接受新连接
            # 为每个客户端创建新线程
            threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    start_server()  # 启动服务器