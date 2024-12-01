import socket

# Địa chỉ IP và cổng của server signaling
SERVER_IP = '192.168.191.131'
SERVER_PORT = 7777

# Tạo socket cho server signaling
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen(2)
print("Server signaling đang chờ 2 client kết nối...")

# Chờ kết nối từ 2 client
clients = []
while len(clients) < 2:
    client_socket, client_address = server_socket.accept()
    print(f"Client kết nối từ: {client_address}")
    clients.append((client_socket, client_address))

# Gửi thông tin IP và PORT của mỗi client cho client kia
clients[0][0].send(f"{clients[1][1][0]}:{15000}".encode())  # Cổng cố định là 15000
clients[1][0].send(f"{clients[0][1][0]}:{15000}".encode())

# Đóng kết nối signaling sau khi gửi thông tin
for client in clients:
    client[0].close()

server_socket.close()
print("Đã trao đổi thông tin giữa 2 client")
