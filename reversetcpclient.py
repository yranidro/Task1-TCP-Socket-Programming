import socket
import random
import struct
import argparse

def send_file(server_ip, server_port, file_path, Lmin, Lmax):
    # 读取文件内容
    with open(file_path, 'r') as f:
        content=f.read()

    # 随机分块
    chunks = []  #存储分块数据
    index = 0
    while index < len(content):
        chunk_size = random.randint(Lmin, Lmax)
        chunk = content[index: index + chunk_size]
        chunks.append(chunk)
        index += chunk_size
    N = len(chunks)  # 块数N

    reservedData=[]  # 用于存储反转后的数据

    # 建立TCP连接
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((server_ip, server_port))  # 连接服务器

        # 发送 Initialization(type+n 2+4)
        s.send(struct.pack('!HI', 1, N))  # type=1 + N

        # 接收 agree(type 2)
        agree=s.recv(2)
        assert struct.unpack('!H', agree)[0] == 2

        # 逐块发送 reserveRequest 接收 reverseAnswer
        for i , chunk in enumerate(chunks):
            # 发送 reverseRequest(type+length+data 2+4+n)
            s.send(struct.pack('!HI', 3, len(chunk)) + chunk.encode('ascii'))  # type=3 + length + data

            # 接收 reverseAnswer(type+length+reverseData 4+2+n)
            header=s.recv(6)  # type+length
            data_type, length = struct.unpack('!HI', header)
            reversed_data=s.recv(length).decode('ascii')  # data
            print(f"{i+1}: {reversed_data}")  # 打印反转后的数据
            reservedData.append(reversed_data)  # 保存反转后的数据

    # 将反转数据合并输出到文件
    output_file="reserved_" + file_path
    with open(output_file, 'w') as f:
        f.write(''.join(reversed(reservedData)))
    print(f"\n反转数据已保存到文件: {output_file}")

if __name__ == "__main__":
    # 解析命令行参数
    parser=argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1", help="Server IP address")
    parser.add_argument("--port", type=int, default=65432, help="Server port")
    parser.add_argument("--file", required=True, help="Path to ASCII file")
    parser.add_argument("--Lmin", type=int, default=0, help="Minimum chunk size")
    parser.add_argument("--Lmax", type=int, default=0, help="Maximum chunk size")
    args=parser.parse_args()

    send_file(args.ip, args.port, args.file, args.Lmin, args.Lmax)