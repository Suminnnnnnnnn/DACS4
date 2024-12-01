
import socket
import threading


clients = {}

# Server logic
def handle_client(conn, addr):
    while True:
        try:
            data = conn.recv(1024).decode()
            print("Received data:", data)
            if data.startswith("CONNECT"):
                username = data.split()[1]
                clients[username] = conn, addr
                # Gửi danh sách người dùng trực tuyến
                conn.sendall(f"ONLINE {', '.join(clients.keys())}".encode())
            elif data.startswith("REQUEST"):
                _, sender, receiver = data.split()
                if receiver in clients:
                    receiver_conn, receiver_addr = clients[receiver]
                    sender_conn, sender_addr = clients[sender]
                    # Gửi địa chỉ của người nhận cho người gửi
                    sender_conn.sendall(f"RECEIVER {receiver_addr[0]} {receiver_addr[1]}".encode())
                else:
                    conn.sendall("User not online.".encode())
        except:
            conn.close()
            break

# Main server function
def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('192.168.110.212', 1234))
    server.listen()
    print("Server started on port 12345")

    while True:
        conn, addr = server.accept()
        print("Accepted connection from", addr)
        threading.Thread(target=handle_client, args=(conn, addr)).start()
if __name__ == "__main__":
    main()