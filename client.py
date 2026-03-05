import socket

HEADER = 64
TCP_PORT = 5050
UDP_PORT = 5051
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
TCP_ADDR = (SERVER, TCP_PORT)
UDP_ADDR = (SERVER, UDP_PORT)


# -------------------- TCP CLIENT --------------------
tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_client.connect(TCP_ADDR)


def send_tcp(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' '*(HEADER - len(send_length))
    tcp_client.send(send_length)
    tcp_client.send(message)
    print("[TCP SERVER]", tcp_client.recv(2048).decode(FORMAT))


# -------------------- UDP CLIENT --------------------
udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send_udp(msg):
    udp_client.sendto(msg.encode(FORMAT), (UDP_ADDR))
    data, _ = udp_client.recvfrom(1024)
    print("[UDP SERVER]", data.decode(FORMAT))



# -------------------- TEST MESSAGES --------------------
if __name__ == "__main__":
    #TCP Test
    send_tcp("Hello TCP World!")
    input()
    send_tcp("Hello TCP Message!")

    #UDP Test
    send_udp("Hello UDP World!")
    input()
    send_udp("Hello UDP Message!")

    #Dissconnect TCP
    send_tcp(DISCONNECT_MESSAGE)