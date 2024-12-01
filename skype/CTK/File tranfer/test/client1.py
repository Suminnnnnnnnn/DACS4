import socket
import threading
import customtkinter as ctk
from tkinter import filedialog


class FileTransferClient:
    def __init__(self, master):
        self.master = master
        self.master.title("File Transfer Client")
        self.frame = ctk.CTkFrame(master=self.master)
        self.frame.pack(padx=20, pady=20)

        self.label = ctk.CTkLabel(master=self.frame, text="File Transfer")
        self.label.pack(pady=10)

        self.send_button = ctk.CTkButton(master=self.frame, text="Select File to Send", command=self.select_file)
        self.send_button.pack(pady=10)

        self.start_button = ctk.CTkButton(master=self.frame, text="Start Server", command=self.start_server)
        self.start_button.pack(pady=10)

        self.peer = None

    def connect_to_server(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(('127.0.0.1', 12343))
        port = self.server.getsockname()[1]
        self.sock.send(f"{self.master.title()}~127.0.0.1~{port}".encode())
        threading.Thread(target=self.receive_info).start()

    def receive_info(self):
        try:
            data = self.sock.recv(1024).decode()
            print(f"Data received from server: {data}")  # In ra dữ liệu nhận được từ server
            if '~' in data:
                peer_ip, peer_port = data.split('~')
                print(f"Connecting to peer at {peer_ip}:{peer_port}")
                self.connect_to_peer(peer_ip, int(peer_port))
            else:
                print(f"Unexpected data format received: {data}")
        except ConnectionResetError as e:
            print(f"Connection to server lost: {e}")
        except ValueError as e:
            print(f"ValueError: {e}")

    def connect_to_peer(self, ip, port):
        self.peer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.peer.connect((ip, port))
        except ConnectionRefusedError:
            print(f"Could not connect to peer at {ip}:{port}. Connection refused.")

    def select_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.send_file(file_path)

    def send_file(self, file_path):
        with open(file_path, 'rb') as f:
            data = f.read()
            self.peer.sendall(data)
        print(f"File {file_path} sent successfully!")

    def start_server(self):
        host = '127.0.0.1'
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, 0))
        self.server.listen(1)
        self.master.winfo_serverport = self.server.getsockname()[1]  # Đảm bảo sử dụng đúng cách để lấy cổng
        self.connect_to_server()
        print(f"Server listening on {host}:{self.master.winfo_serverport}")
        conn, addr = self.server.accept()
        self.peer = conn


root = ctk.CTk()
app = FileTransferClient(master=root)
root.mainloop()
