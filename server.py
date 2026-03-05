import socket
import threading

HEADER = 64
TCP_PORT = 5050
UDP_PORT = 5051
SERVER = socket.gethostbyname(socket.gethostname())  #my loccal ipv4 address to run in my local network
TCP_ADDR = (SERVER, TCP_PORT)
UDP_ADDR = (SERVER, UDP_PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"


# -----------------TCP SERVER--------------
tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #That's how we create new socket. pick the type INET(over the internet), pick the method(SOCK_STREAM)
tcp_server.bind(TCP_ADDR)

def handle_tcp_client(conn, addr): #Handle the indiviual connection between the client and server
    print(f"[NEW TCP-CONNECTION] {addr} connected.")
    
    connected = True
    while connected:
        msg_length  = conn.recv(HEADER).decode(FORMAT)#How many bytes we want to receive and decoded it into string using utf-8 format 
        if msg_length:
            msg_length = int(msg_length.strip()) #Converted it into int
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[TCP {addr}] {msg}")
            conn.send("TCP Msg received".encode(FORMAT)) #send msg from server to client
  

    conn.close() #close the current connection


def start_tcp_server(): #Handle new connection
    tcp_server.listen()
    print(f"[TCP LISTENING] Server is listening on {TCP_ADDR}")
    while True:
        conn, addr =tcp_server.accept() 
        thread = threading.Thread(target=handle_tcp_client, args=(conn, addr))
        thread.start()
        print(f"[TCP ACTIVE CONNECTIONS] {threading.active_count() - 1}") #How many active threads are active on this process   #The amount of threads will represent the amount of clients connected



# -----------------UDP SERVER--------------
udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_server.bind(UDP_ADDR)

def start_udp_server():
    print(f"[UDP LISTENING] Server is listening on {UDP_ADDR}")
    while True:
        data, addr = udp_server.recvfrom(1024)
        print(f"[UDP {addr}] {data.decode(FORMAT)}")
        udp_server.sendto("UDP Msg received".encode(FORMAT), addr)



# -----------------START SERVER--------------
if __name__ == "__main__":
    tcp_thread = threading.Thread(target=start_tcp_server)
    udp_thread = threading.Thread(target=start_udp_server)
    tcp_thread.start()
    udp_thread.start()