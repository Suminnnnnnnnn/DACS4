import socket
import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext
from CTK import module

class ChatClient:
    HOST = '10.60.135.42'
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

        self.chatinterface=module.chat
    # def add_message(self, message):
    #     self.message_box.config(state=tk.NORMAL)
    #     self.message_box.insert(tk.END, message + '\n')
    #     self.message_box.config(state=tk.DISABLED)
    def add_message(self, message):
          self.chatinterface.message_box.config(state=tk.NORMAL)
          self.chatinterface.message_box.insert(tk.END, message + '\n')
          self.chatinterface.message_box.config(state=tk.DISABLED)

    # def update_user_list(self, users):
    #     self.user_listbox.delete(0, tk.END)
    #     for user in users:
    #         self.user_listbox.insert(tk.END, user)
    #     self.user_listbox.selection_clear(0, tk.END)
    def update_user_list(self,users):
          print(f"Updating user list with {users}")
          # self.chatinterface.user_listbox.delete(0, tk.END)
          # unique_users = set(users)  # Xóa bỏ các giá trị trùng lặp
          # if len(users) > 1:
          self.chatinterface.user_listbox.delete(0,"end")
          for user in users:
              print(f"Inserting user: {user}")
              self.chatinterface.user_listbox.insert("END", user)
          # self.chatinterface.user_listbox.selection_clear(0)

    def connect(self):
        try:
            self.client.connect((self.HOST, self.PORT))
            self.add_message("[SERVER] Successfully connected to the server")

        except:
            messagebox.showerror("Unable to connect", f"Cannot connect to server {self.HOST}:{self.PORT}")
            return

        username = self.chatinterface.username_textbox.get()
        if username:
            self.client.sendall(username.encode())
        else:
            messagebox.showerror("Invalid username", "Username cannot be empty")
            return

        threading.Thread(target=self.listen_for_messages_from_server).start()

        self.chatinterface.username_textbox.configure(state=tk.DISABLED)
        self.chatinterface.username_button.configure(state=tk.DISABLED)

    # def send_message(self):
    #     selected_indices = self.chatinterface.user_listbox.curselection()
    #     if not selected_indices:
    #         messagebox.showerror("No user selected", "Please select a user to send a message to")
    #         return
    #
    #     selected_user = self.chatinterface.user_listbox.get(selected_indices)
    #     message = self.chatinterface.message_textbox.get().strip()
    #     if message:
    #         self.client.sendall(f"{selected_user}~{message}".encode())
    #         print(message)
    #         self.chatinterface.message_textbox.delete(0, len(message))
    #     else:
    #         messagebox.showerror("Empty message", "Message cannot be empty")
    # def send_message(self):
    #     selected_indices = self.chatinterface.user_listbox.curselection()
    #     if not selected_indices:
    #         messagebox.showerror("No user selected", "Please select a user to send a message to")
    #         return
    #
    #     # Đảm bảo rằng chỉ mục được chọn nằm trong khoảng hợp lệ
    #     selected_index = selected_indices[0]
    #     if selected_index < 0 or selected_index >= self.chatinterface.user_listbox.size():
    #         messagebox.showerror("Invalid selection", "The selected user index is invalid")
    #         return
    #
    #     selected_user = self.chatinterface.user_listbox.get(selected_index)
    #     message = self.chatinterface.message_textbox.get().strip()
    #     if message:
    #         self.client.sendall(f"{selected_user}~{message}".encode())
    #         self.chatinterface.message_textbox.delete(0, tk.END)
    #     else:
    #         messagebox.showerror("Empty message", "Message cannot be empty")
    def send_message(self):
        selected_indices = self.chatinterface.user_listbox.curselection()
        print(f"Selected indices: {selected_indices}")

        if   selected_indices is None :
            messagebox.showerror("No user selected", "Please select a user to send a message to")
            return

        selected_index = selected_indices
        print(f"Selected index: {selected_index}")
        #
        # if selected_index < 0 or selected_index >= self.chatinterface.user_listbox.size():
        #     messagebox.showerror("Invalid selection", "The selected user index is invalid")
        #     return

        selected_user = self.chatinterface.user_listbox.get(selected_index).strip()
        print(f"Selected user: {selected_user}")

        message = self.chatinterface.message_textbox.get().strip()
        if message:
            self.client.sendall(f"{selected_user}~{message}".encode())
            self.chatinterface.message_textbox.delete(0, tk.END)
        else:
            messagebox.showerror("Empty message", "Message cannot be empty")

    def listen_for_messages_from_server(self):
        while True:
            try:
                message = self.client.recv(2048).decode('utf-8')
                if message.startswith("SERVER~"):
                    users = message.split("~")[1].split(",")
                    print(users)
                    self.update_user_list(users)
                else:
                    username, content = message.split("~", 1)
                    self.add_message(f"[{username}] {content}")
            except Exception as e:
                messagebox.showerror("Error", f"Connection lost: {e}")
                print(f"Connection lost{e}")
                self.client.close()
                break
    #
    # def setup_gui(self):
    #     # self.root.geometry("600x700")
    #     # self.root.title("Messenger Client")
    #     # self.root.resizable(True, True)
    #
    #     # self.root.grid_rowconfigure(0, weight=1)
    #     # self.root.grid_rowconfigure(1, weight=4)
    #     # self.root.grid_rowconfigure(2, weight=1)
    #
    #
    #
    #     top_frame = tk.Frame(self.root, width=600, height=100, bg=self.DARK_GREY)
    #     top_frame.grid(row=0, column=0, sticky=tk.NSEW)
    #
    #     middle_frame = tk.Frame(self.root, width=600, height=400, bg=self.MEDIUM_GREY)
    #     middle_frame.grid(row=1, column=0, sticky=tk.NSEW)
    #
    #     bottom_frame = tk.Frame(self.root, width=600, height=100, bg=self.DARK_GREY)
    #     bottom_frame.grid(row=2, column=0, sticky=tk.NSEW)
    #
    #     username_label = tk.Label(top_frame, text="Enter username:", font=self.FONT, bg=self.DARK_GREY, fg=self.WHITE)
    #     username_label.pack(side=tk.LEFT, padx=10)
    #
    #     self.username_textbox = tk.Entry(top_frame, font=self.FONT, bg=self.MEDIUM_GREY, fg=self.WHITE, width=23)
    #     self.username_textbox.pack(side=tk.LEFT)
    #
    #     self.username_button = tk.Button(top_frame, text="Join", font=self.BUTTON_FONT, bg=self.OCEAN_BLUE, fg=self.WHITE, command=self.connect)
    #     self.username_button.pack(side=tk.LEFT, padx=15)
    #
    #     self.message_textbox = tk.Entry(bottom_frame, font=self.FONT, bg=self.MEDIUM_GREY, fg=self.WHITE, width=38)
    #     self.message_textbox.pack(side=tk.LEFT, padx=10)
    #
    #     self.message_button = tk.Button(bottom_frame, text="Send", font=self.BUTTON_FONT, bg=self.OCEAN_BLUE, fg=self.WHITE, command=self.send_message)
    #     self.message_button.pack(side=tk.LEFT, padx=10)
    #
    #     self.message_box = scrolledtext.ScrolledText(middle_frame, font=self.SMALL_FONT, bg=self.MEDIUM_GREY, fg=self.WHITE, width=67, height=26.5)
    #     self.message_box.config(state=tk.DISABLED)
    #     self.message_box.pack(side=tk.TOP)
    #
    #     self.user_listbox = tk.Listbox(middle_frame, font=self.SMALL_FONT, bg=self.MEDIUM_GREY, fg=self.WHITE, width=20, height=10, selectmode=tk.SINGLE)
    #     self.user_listbox.pack(side=tk.RIGHT, padx=10)
    #     self.user_listbox.selection_clear(0, tk.END)

def main():
    root = tk.Tk()
    app = ChatClient(root)
    root.mainloop()

if __name__ == '__main__':
    main()
