import socket
import threading

clients = {}

def handle_client(client_socket, client_address):
    peer_id = client_socket.recv(1024).decode('utf-8')
    print(peer_id)

    clients[peer_id] = client_socket
    print(f"{peer_id} connected.")
    broadcast_user_list()
    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            print(data)
            if data.startswith("CALL_REQUEST"):
                target_peer = data.split(":")[1]
                if target_peer in clients:
                    clients[target_peer].send(f"CALL_REQUEST_FROM~{peer_id}~{client_address}".encode('utf-8'))
            elif data.startswith("CALL_ACCEPT"):
                target_peer = data.split(":")[1]
                if target_peer in clients:
                    clients[target_peer].send(f"CALL_ACCEPTED:{peer_id}".encode('utf-8'))
            elif data.startswith("DISCONNECT"):
                break
        except:
            break

    del clients[peer_id]
    client_socket.close()
    print(f"{peer_id} disconnected.")
def broadcast_user_list():
    users_list = ",".join(clients.keys())
    print(users_list)
    for client_socket in clients.values():
        client_socket.send(f"USERS_LIST:{users_list}".encode('utf-8'))
def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 9999))
    server_socket.listen(5)
    print("Server listening on port 9999")

    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

if __name__ == "__main__":
    server()
