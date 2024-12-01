import socket
import threading
import Chatter
class ChatServer:
    def __init__(self, host='0.0.0.0', port=12345):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((host, port))
        self.server.listen(5)
        self.chatters = []
        print(f"Server started on {host}:{port}")

    def handle_client(self, client_socket):
        try:
            # Nhận thông tin đăng nhập từ peer
            login_data = client_socket.recv(1024).decode('utf-8')
            nickname, ip, port = login_data.split(':')
            new_chatter = Chatter(nickname, ip, int(port))
            self.chatters.append(new_chatter)
            print(f"{new_chatter} has joined the chat.")

            # Gửi danh sách các chatters cho peer mới
            self.send_chatter_list(client_socket)

            # Gửi thông tin peer mới cho các peer còn lại
            self.notify_all_peers(new_chatter)

            while True:
                # Chờ nhận thông tin từ peer (giả sử để lắng nghe tín hiệu đăng xuất)
                message = client_socket.recv(1024).decode('utf-8')
                if message == "LOGOUT":
                    self.chatters.remove(new_chatter)
                    print(f"{new_chatter} has left the chat.")
                    self.notify_all_peers(new_chatter, logout=True)
                    break
        finally:
            client_socket.close()

    def send_chatter_list(self, client_socket):
        chatter_list = "\n".join([str(chatter) for chatter in self.chatters])
        client_socket.send(chatter_list.encode('utf-8'))

    def notify_all_peers(self, chatter, logout=False):
        message = f"ADD:{chatter}" if not logout else f"REMOVE:{chatter}"
        for c in self.chatters:
            if c != chatter:
                try:
                    peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    peer_socket.connect((c.ip, c.port))
                    peer_socket.send(message.encode('utf-8'))
                    peer_socket.close()
                except:
                    pass

    def start(self):
        while True:
            client_socket, addr = self.server.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

if __name__ == "__main__":
    chat_server = ChatServer()
    chat_server.start()
