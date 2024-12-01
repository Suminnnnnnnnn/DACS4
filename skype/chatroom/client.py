import socket
import threading

def listen_for_updates(server_ip, server_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((server_ip, server_port))
        chatter_list = client_socket.recv(1024).decode('utf-8')
        print("Connected peers:")
        print(chatter_list)

        while True:
            try:
                update = client_socket.recv(1024).decode('utf-8')
                if update.startswith("ADD:"):
                    print(f"New peer added: {update[4:]}")
                elif update.startswith("REMOVE:"):
                    print(f"Peer removed: {update[7:]}")
            except:
                break

def start_peer(nickname, ip, port, server_ip, server_port):
    threading.Thread(target=listen_for_updates, args=(server_ip, server_port)).start()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((server_ip, server_port))
        login_message = f"{nickname}:{ip}:{port}"
        client_socket.send(login_message.encode('utf-8'))

        try:
            while True:
                command = input("Enter 'LOGOUT' to logout: ")
                if command == "LOGOUT":
                    client_socket.send(command.encode('utf-8'))
                    break
        except:
            pass

if __name__ == "__main__":
    nickname = input("Enter your nickname: ")
    ip = '192.168.1.159'
    port = 12346
    server_ip = '192.168.1.159'
    server_port = 12345

    start_peer(nickname, ip, port, server_ip, server_port)
