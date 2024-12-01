# Client application
import socket
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
import os
class ClientApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("P2P File Transfer")
        self.geometry("400x300")
        self.server = None
        self.filepath = None
        self.create_widgets()

    def create_widgets(self):
        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username")
        self.username_entry.pack(pady=10)
        self.connect_btn = ctk.CTkButton(self, text="Connect", command=self.connect_to_server)
        self.connect_btn.pack(pady=10)
        self.file_btn = ctk.CTkButton(self, text="Select File", command=self.select_file)
        self.file_btn.pack(pady=10)
        self.send_btn = ctk.CTkButton(self, text="Send File", command=self.send_file)
        self.send_btn.pack(pady=10)
        self.online_users = ctk.CTkComboBox(self)
        self.online_users.pack(pady=10)

    def connect_to_server(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.connect(('192.168.110.212', 1234))
            threading.Thread(target=self.receive_data).start()
            username = self.username_entry.get()
            self.server.sendall(f"CONNECT {username}".encode())
            port = self.start_file_listener()
            self.server.sendall(f"PORT {username} {port}".encode())
        except Exception as e:
            messagebox.showerror("Connection Error", f"Could not connect to server: {e}")

    def receive_data(self):
        while True:
            try:
                data = self.server.recv(1024).decode()
                if data.startswith("ONLINE"):
                    users = data.split(" ")[1].split(',')
                    self.online_users.configure(values=users)
                elif data.startswith("RECEIVER"):
                    ip, port = data.split()[1], int(data.split()[2])
                    threading.Thread(target=self.send_file_to_peer, args=(ip, port)).start()
            except Exception as e:
                print(f"Error receiving data: {e}")
                break

    def select_file(self):
        self.filepath = filedialog.askopenfilename()
        if self.filepath:
            messagebox.showinfo("File Selected", f"Selected {os.path.basename(self.filepath)}")

    def send_file(self):
        receiver = self.online_users.get()
        if receiver and self.filepath:
            username = self.username_entry.get()
            self.server.sendall(f"REQUEST {username} {receiver}".encode())
        else:
            messagebox.showwarning("Warning", "Select a user and file to send.")

    def start_file_listener(self):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.bind(('0.0.0.0', 0))
        listener.listen(1)
        port = listener.getsockname()[1]
        print(f"Listening on port {port}")
        threading.Thread(target=self.accept_file, args=(listener,)).start()
        return port

    def accept_file(self, listener):
        conn, addr = listener.accept()
        with conn, open("received_file", 'wb') as file:
            print("Receiving file from:", addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                file.write(data)
        messagebox.showinfo("File Transfer", "File received successfully")

    def send_file_to_peer(self, ip, port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as peer_conn:
                print(f"Connecting to peer at IP: {ip}, Port: {port}")
                peer_conn.connect((ip, port))
                with open(self.filepath, 'rb') as file:
                    while (data := file.read(1024)):
                        peer_conn.send(data)
            messagebox.showinfo("File Transfer", "File sent successfully")
        except ConnectionRefusedError:
            messagebox.showerror("Connection Error", "Could not connect to the recipient.")

if __name__ == "__main__":
    app = ClientApp()
    app.mainloop()