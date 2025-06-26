1.程序概述
    本项目实现了一个基于 TCP socket 的客户端-服务端程序，功能如下：
        客户端：将文本文件分块发送到服务端，接受反转后的数据块，并最终输出完整的反转文件。
        服务端：接收客户端发送的数据块，反转后返回，支持多客户端并发处理。

2.运行环境
    操作系统：Windows/Linux
    Python版本：3.6及以上
    依赖库：无额外依赖

3.文件说明
    reversetcpserver.py       服务端程序（监听端口、处理请求）
    reversetcpclient.py        客户端程序（发送文件并接收结果）

4.配置选项
    参数         默认值           说明
    ip	         127.0.0.1       服务器IP地址
    port	   65432         服务器端口号
    file	       无           待反转的文本文件路径
    Lmin		0            最小分块大小
    Lmax		0            最大分块大小

5.使用示例
    启动服务端：
        python reversetcpserver.py
    启动客户端：
        python reversetcpclient.py --ip 127.0.0.1 --port 65432 --file data.txt --Lmin 3 --Lmax 6