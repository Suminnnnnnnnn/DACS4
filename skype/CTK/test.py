import socket
import threading
import customtkinter as ctk

from aiortc import RTCPeerConnection
import cv2
import pyaudio
import asyncio
import tkinter as tk
from tkinter import messagebox


class VideoChatApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("400x500")
        self.root.title("P2P Video Call")
        ctk.set_appearance_mode("dark")

        # UI Elements
        self.user_label = ctk.CTkLabel(self.root, text="Enter Username:")
        self.user_label.pack(pady=10)
        self.username_entry = ctk.CTkEntry(self.root, width=200)
        self.username_entry.pack(pady=10)
        self.connect_button = ctk.CTkButton(self.root, text="Connect", command=self.connect_to_server)
        self.connect_button.pack(pady=10)

        self.online_list_label = ctk.CTkLabel(self.root, text="Online Users:")
        self.online_list_label.pack(pady=10)
        self.online_list = tk.Listbox(self.root, width=30, height=10)
        self.online_list.pack(pady=10)

        self.call_button = ctk.CTkButton(self.root, text="Call Selected", command=self.request_call)
        self.call_button.pack(pady=10)

        # Socket and connection data
        self.username = ""
        self.server_ip = '192.168.1.8'
        self.server_port = 9999
        self.connection = None
        self.call_accepted = False
        self.target_peer = None
        self.peer_connection = RTCPeerConnection()

    def connect_to_server(self):
        self.username = self.username_entry.get()
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((self.server_ip, self.server_port))
        self.connection.send(self.username.encode('utf-8'))

        # Start receiving updates from server
        threading.Thread(target=self.listen_for_server, daemon=True).start()

    def listen_for_server(self):
        while True:
            try:
                data = self.connection.recv(1024).decode('utf-8')
                print(data)
                if data.startswith("USERS_LIST"):
                    users = data.split(":")[1].split(",")
                    self.update_user_list(users)
                elif data.startswith("CALL_REQUEST_FROM"):
                    caller = data.split(":")[1]
                    self.show_call_request(caller)
                elif data.startswith("CALL_ACCEPTED"):
                    peer = data.split(":")[1]
                    if peer == self.target_peer:
                        self.call_accepted = True

                        asyncio.run(self.start_video_audio_call())
            except:
                break

    def show_call_request(self, caller):
        # Hiển thị hộp thoại yêu cầu gọi đến
        response = messagebox.askyesno("Incoming Call", f"{caller} wants to call you. Accept?")
        if response:
            self.connection.send(f"CALL_ACCEPT:{caller}".encode('utf-8'))
            self.call_accepted = True
            asyncio.run(self.start_video_audio_call())
        else:
            self.connection.send(f"CALL_REJECT:{caller}".encode('utf-8'))

    def request_call(self):
        selected_peer = self.online_list.get(tk.ACTIVE)
        self.target_peer = selected_peer
        self.connection.send(f"CALL_REQUEST:{selected_peer}".encode('utf-8'))

    async def start_video_audio_call(self):
        video_stream = cv2.VideoCapture(0)
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)

        # Display video in new window
        cv2.namedWindow("Video Call", cv2.WINDOW_NORMAL)

        while self.call_accepted:
            ret, frame = video_stream.read()
            if not ret:
                break
            cv2.imshow("Video Call", frame)
            audio_data = stream.read(1024)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        video_stream.release()
        cv2.destroyAllWindows()
        stream.stop_stream()
        stream.close()
        audio.terminate()




    def on_closing(self):
        if self.connection:
            self.connection.send("DISCONNECT".encode('utf-8'))
            self.connection.close()
        self.root.destroy()

    def update_user_list(self, users):
        self.online_list.delete(0, tk.END)  # Xóa toàn bộ danh sách hiện tại
        for user in users:
            self.online_list.insert(tk.END, user)  # Thêm từng user vào Listbox

if __name__ == "__main__":
    root = ctk.CTk()
    app = VideoChatApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
