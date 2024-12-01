import pickle
import socket
import struct
import threading
import time
import tkinter as tk
from tkinter import messagebox, scrolledtext

import cv2

from CTK import module
from CTK.Model.session import Session
import customtkinter as ctk

class ChatClient:
    HOST = '192.168.1.9'
    PORT = 1234

    DARK_GREY = '#121212'
    MEDIUM_GREY = '#1F1B24'
    OCEAN_BLUE = '#464EB8'
    WHITE = "white"
    FONT = ("Helvetica", 17)
    BUTTON_FONT = ("Helvetica", 15)
    SMALL_FONT = ("Helvetica", 13)

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.root = root
        # self.setup_gui()
        # app=import_app()
        # self.chatinterface = ChatInterface(app)
        self.typing=False
        self.chatinterface=module.chat
    # def add_message(self, message):
    #     self.message_box.config(state=tk.NORMAL)
    #     self.message_box.insert(tk.END, message + '\n')
    #     self.message_box.config(state=tk.DISABLED)
    def add_message(self, username, message, user_id):
        # Tạo một frame mới cho mỗi tin nhắn
        frame_message = ctk.CTkFrame(self.chatinterface.scrollable_frame, fg_color="Pink")

        # Tạo các label cho username và message
        username_label = ctk.CTkLabel(frame_message, font=self.FONT, text=username)
        message_label = ctk.CTkLabel(frame_message, text=message, width=200, height=40, fg_color="lightblue",wraplength=200)

        # Căn chỉnh vị trí của các label tùy vào người gửi hay nhận
        if user_id == Session.user_id:
            # Tin nhắn của người dùng
            username_label.grid(row=0, column=0, sticky='e', padx=10, pady=5)
            message_label.grid(row=0, column=1, sticky='w', padx=10, pady=5)
            frame_message.grid(row=self.chatinterface.row + 1, column=1, sticky='nsew', padx=10, pady=10)
        else:
            # Tin nhắn của người nhận
            username_label.grid(row=0, column=0, sticky='e', padx=10, pady=5)
            message_label.grid(row=0, column=1, sticky='w', padx=10, pady=5)
            frame_message.grid(row=self.chatinterface.row + 1, column=3, sticky='nsew', padx=10, pady=10)

        # Tăng số hàng sau mỗi tin nhắn để tránh chồng chéo
        self.chatinterface.row += 1
        self.chatinterface.scrollable_frame.update_idletasks()

    def connect(self,user_id):
        try:
            self.client.connect((self.HOST, self.PORT))
            self.my_ip=self.client.getsockname()[0]
            # self.add_message("[SERVER] Successfully connected to the server")

        except:
            messagebox.showerror("Unable to connect", f"Cannot connect to server {self.HOST}:{self.PORT}")
            return

        # username = self.chatinterface.username_textbox.get()
        username=Session.username
        data = f"{user_id}~{username}".encode('utf-8')
        if user_id:
            self.client.sendall(data)
        else:
            messagebox.showerror("Invalid userid", "Username cannot be empty")
            return

        threading.Thread(target=self.listen_for_messages_from_server).start()
    def send_message(self,sender_id,recive_id,chatting,conversation_id):
        # selected_indices = self.chatinterface.user_listbox.curselection()
        # print(f"Selected indices: {selected_indices}")
        if  sender_id and recive_id is None :
            messagebox.showerror("No user selected", "Please select a user to send a message to")
            return
        message = self.chatinterface.message_textbox.get().strip()
        if chatting.send_message(conversation_id, sender_id, message):
            return f"Da them tin nhan den co so du lieu: {conversation_id} {sender_id} {message}"
        if message:
            self.add_message(Session.username,message,sender_id)
            self.client.sendall(f"{recive_id}~{message}~{Session.username}".encode())
            self.chatinterface.message_textbox.delete(0, tk.END)
            self.chatinterface.scrollable_frame._parent_canvas.yview_moveto(1.0)
        else:
            messagebox.showerror("Empty message", "Message cannot be empty")

    def call_video(self, recive_id):
        message = "CALL_REQUEST"
        peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        peer_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        peer_socket.bind(('0.0.0.0', 15000))  # Fixed port for peer connections

        # Send initial call request to server with peer address
        address = (f"{self.my_ip}", 15000)
        self.client.sendall(f"{recive_id}~{address}~{message}".encode())

        # Wait for confirmation from the receiving peer
        confirmation_received = self.wait_for_confirmation(peer_socket)
        if confirmation_received:
            threading.Thread(target=self.receive_video, args=(self.conn,)).start()
            threading.Thread(target=self.send_video, args=(self.conn,)).start()
        else:
            print("No confirmation received. Call aborted.")

    def wait_for_confirmation(self, peer_socket):
        # Waits for a connection confirmation message from the other peer
        try:
            peer_socket.listen(1)
            conn, addr = peer_socket.accept()
            self.conn=conn
            print("Connected with:", addr)
            confirmation_msg = conn.recv(1024).decode()
            if confirmation_msg == "CALL_CONFIRM":
                print("Confirmation received. Starting video.")
                return True
        except Exception as e:
            print("Error during confirmation:", e)
        return False

    def listen_for_video(self, address, recive_id, message):
        if message == "CALL_REQUEST":
            if messagebox.askyesno("CALL_VIDEO", "Incoming video call. Accept?"):
                peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                peer_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

                ip, port = address.strip("()").split(", ")
                ip = ip.strip("'")
                port = int(port)

                # Connect to the calling peer with retry attempts
                connected = False
                for attempt in range(5):
                    try:
                        peer_socket.connect((ip, port))
                        print(f"Connected to peer at {ip}:{port}")
                        connected = True
                        break
                    except socket.error:
                        print(f"Connection attempt {attempt + 1} failed. Retrying...")
                        time.sleep(2)

                if connected:
                    try:
                        peer_socket.sendall("CALL_CONFIRM".encode())
                        threading.Thread(target=self.send_video, args=(peer_socket,)).start()
                        threading.Thread(target=self.receive_video, args=(peer_socket,)).start()


                    except socket.error as e:
                        print("Error sending confirmation:", e)
                        peer_socket.close()
                        messagebox.showerror("Error", "Unable to connect to the caller.")
                else:
                    messagebox.showerror("Error", "Unable to connect to the caller.")

    def receive_video(self, client_socket):
        print("Client socket:", client_socket)
        data = b""
        payload_size = struct.calcsize("Q")

        while True:
            try:
                while len(data) < payload_size:
                    packet = client_socket.recv(4096)
                    if not packet:
                        print("Disconnected by peer.")
                        return
                    data += packet

                packed_msg_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = struct.unpack("Q", packed_msg_size)[0]

                while len(data) < msg_size:
                    packet = client_socket.recv(4096)
                    if not packet:
                        print("Disconnected by peer.")
                        return
                    data += packet

                frame_data = data[:msg_size]
                data = data[msg_size:]
                frame = pickle.loads(frame_data)

                # Giảm độ phân giải để cải thiện hiệu suất
                frame = cv2.resize(frame, (1000, 1000))

                cv2.imshow("Receiving Video", frame)
                if cv2.waitKey(1) == 27:  # Press 'ESC' to exit
                    break
                time.sleep(0.033)  # Tạo độ trễ nhỏ để duy trì tốc độ khoảng 30 FPS

            except socket.error as e:
                print("Error receiving video:", e)
                client_socket.close()
                return
            except Exception as e:
                print("Other error:", e)
                client_socket.close()
                return

    def send_video(self, peer_socket):
        cap = cv2.VideoCapture(0)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.resize(frame, (1000, 1000))
            data = pickle.dumps(frame)
            message = struct.pack("Q", len(data)) + data

            try:
                peer_socket.sendall(message)
                print("Sent video frame")
            except socket.error as e:
                print("Error sending video:", e)
                peer_socket.close()
                return
            except Exception as e:
                print("Other error:", e)
                peer_socket.close()
                return

            cv2.imshow("Sending Video", frame)
            if cv2.waitKey(1) == 27:  # Press 'ESC' to exit
                break
            time.sleep(
                0.033)  # Tạo độ trễ nhỏ để duy trì tốc độ khoảng 30 FPS

    def listen_for_messages_from_server(self):
        while True:
            try:
                message = self.client.recv(2048).decode('utf-8')
                if message.startswith("SERVER~"):
                    users = message.split("~")[1].split(",")
                    print(users)
                    # self.update_user_list(users)
                else:
                    time.sleep(1)
                    username, user_id, content = message.split("~")
                    print(content)
                    if content=="typing":
                     print("typing")
                     self.chatinterface.typ.grid(row=self.chatinterface.row+1,column=3,sticky='nsew', padx=10, pady=10)
                     self.chatinterface.typ_son.configure(text="Đang soạn tin nhắn")
                     self.chatinterface.scrollable_frame._parent_canvas.yview_moveto(1.0)
                    elif content=="stop_typing":
                     print("stop_typing")
                     self.chatinterface.typ.grid_remove()
                    elif content=="CALL_REQUEST":
                        self.listen_for_video(username,user_id,content)
                    else:
                     self.add_message(username,content,user_id)
            except Exception as e:
                messagebox.showerror("Error", f"Connection lost: {e}")
                print(f"Connection lost{e}")
                self.client.close()
                break

    def start_typing(self,recive_id ):

        if not self.typing:
            typing="typing"
            self.client.sendall(f"{recive_id}~{typing}~{Session.username}".encode())
            self.typing = True

    def stop_typing(self, recive_id ):
         # Wait briefly to confirm stop typing
        if self.typing:
            stop_typing="stop_typing"
            self.client.sendall(f"{recive_id}~{stop_typing}~{Session.username}".encode())
            self.typing = False
def main():
    root = tk.Tk()
    app = ChatClient(root)
    root.mainloop()

if __name__ == '__main__':
    main()
