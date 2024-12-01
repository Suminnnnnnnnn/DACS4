import socket
import threading

clients = {}


def handle_client(conn, addr):
    try:
        data = conn.recv(1024).decode()
        peer_info = data.split('~')
        peer_id, peer_ip, peer_port = peer_info
        clients[peer_id] = (peer_ip, peer_port)

        if len(clients) == 2:
            client_ids = list(clients.keys())
            for id in client_ids:
                peer_id = client_ids[1] if id == client_ids[0] else client_ids[0]
                conn_info = f"{clients[peer_id][0]}~{clients[peer_id][1]}"
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn_to_peer:
                    conn_to_peer.connect((clients[id][0], int(clients[id][1])))
                    conn_to_peer.send(conn_info.encode())
            clients.clear()
    except Exception as e:
        print(f"Error handling client {addr}: {e}")
    finally:
        conn.close()


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 12343))
    server.listen(2)
    print("Server started, waiting for connections...")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()


if __name__ == "__main__":
    main()
