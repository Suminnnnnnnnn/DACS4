import os
from tkinter import scrolledtext, Scrollbar
from CTkListbox import *
import customtkinter
from PIL import Image  # Import thư viện Pillow
from customtkinter import CTkFrame, CTkLabel

from CTK.Model.session import Session
from realtimechat.test.client import ChatClient


DARK_GREY = '#121212'
MEDIUM_GREY = '#1F1B24'
OCEAN_BLUE = '#464EB8'
WHITE = "white"
FONT = ("Helvetica", 17)
BUTTON_FONT = ("Helvetica", 15)
SMALL_FONT = ("Helvetica", 13)
def load_image(filename, size):
    """
    Tải hình ảnh từ thư mục assets/images dựa trên vị trí của file chat.py.

    Args:
        filename (str): Tên tệp hình ảnh.
        size (tuple): Kích thước (width, height) của hình ảnh sau khi thay đổi kích thước.

    Returns:
        CTkImage: Đối tượng CTkImage được tạo từ hình ảnh đã tải.
    """
    # Lấy đường dẫn đến thư mục CTK (thư mục gốc của dự án)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # CTK
    assets_dir = os.path.join(base_dir, 'assets', 'images')  # Đường dẫn đến thư mục chứa hình ảnh

    image_path = os.path.join(assets_dir, filename)
    print(f"ChatInterface - Loading image from: {image_path}")  # Kiểm tra đường dẫn
    if not os.path.exists(image_path):
        print(f"ChatInterface - File not found: {image_path}")
        raise FileNotFoundError(f"ChatInterface - File not found: {image_path}")
    image = Image.open(image_path).resize(size)
    return customtkinter.CTkImage(light_image=image, size=size)

class ChatInterface:
    def __init__(self, master):
        self.title= "chat"
        self.master = master
        self.chatclient=None
        # self.chat = chat
        self.frame_chat = customtkinter.CTkFrame(
            master=self.master, width=800, height=800, fg_color="#EEEEEE"
        )
        # self.frame_chat.grid(row=0, column=3, rowspan=4, sticky='nsew')

        self.frame_chat.columnconfigure(0, weight=1)
        self.frame_chat.rowconfigure(0, weight=1)
        self.frame_chat.rowconfigure(1, weight=8)

        # Tạo frame_options
        self.frame_options = customtkinter.CTkFrame(
            master=self.frame_chat, width=800, height=200, fg_color="White"
        )
        self.frame_options.grid(row=0, column=0, sticky='nsew')

        # Cấu hình lưới cho frame_options
        self.frame_options.columnconfigure(0, weight=1)  # Bên trái có thể giãn ra
        self.frame_options.columnconfigure(1, weight=0)  # Bên phải cố định kích thước
        self.frame_options.rowconfigure(0, weight=1)     # Hàng phía trên có thể giãn ra
        self.frame_options.rowconfigure(1, weight=0)     # Hàng chứa các nút
        self.frame_options.rowconfigure(2, weight=1)     # Hàng phía dưới có thể giãn ra

        # Tạo frame để chứa các nút bấm
        self.frame_buttons = customtkinter.CTkFrame(
            master=self.frame_options, fg_color="White"
        )
        self.frame_buttons.grid(row=1, column=1, sticky='e', padx=(0, 10))  # Đặt vào giữa theo chiều dọc và bên phải

        # Tạo các nút bấm và căn chúng vào giữa frame_buttons
        try:
            self.img_search = load_image("search.png", (20, 20))
            self.img_call = load_image("phone-call.png", (20, 20))
            self.img_video_call = load_image("video-call.png", (20, 20))
        except FileNotFoundError as e:
            print(e)
            print("Dam bao cac tep hinh anh ton tai trong thu muc")
            return
        self.button_search = customtkinter.CTkButton(
            master=self.frame_buttons, width=40, height=40, image=self.img_search, fg_color="White", text=""
        )
        self.button_search.grid(row=0, column=0, padx=(0, 5))

        self.button_call = customtkinter.CTkButton(
            master=self.frame_buttons, width=40, height=40, image=self.img_call, fg_color="White", text=""
        )
        self.button_call.grid(row=0, column=1, padx=(0, 5))

        self.button_video_call = customtkinter.CTkButton(
            master=self.frame_buttons, width=40, height=40, image=self.img_video_call, fg_color="White", text=""
        )
        self.button_video_call.grid(row=0, column=2)

        # Tạo frame_message
        self.frame_message = customtkinter.CTkFrame(
            master=self.frame_chat, width=800, height=500, fg_color="Gray"
        )
        self.frame_message.grid(row=1, column=0, sticky='nsew')
        self.frame_message.grid_columnconfigure(1, weight=1)
        self.frame_message.rowconfigure(1, weight=1)
        # self.user_listbox.selection_clear(0, customtkinter.END)
        # self.chatting()
    def hide(self):
     self.frame_chat.grid_remove()
     if self.chatclient :
      self.chatclient.client.close()

    def show(self):
        self.frame_chat.grid(row=0, column=3, rowspan=4, sticky='nsew')
        # self.chatting()
    def chatting(self,conversation_id,recive_id,chatting):
        self.chatclient =ChatClient()
        self.chatclient.connect(Session.user_id)
        # client
        print(f" : {conversation_id}")
        username_label = customtkinter.CTkLabel(self.frame_options, text="Enter username:", font=FONT,
                                                )
        username_label.grid(row=1, column=2, sticky='e')
        self.button_video_call.bind("<Button-1>",lambda event:self.chatclient.call_video(recive_id))
        self.username_textbox = customtkinter.CTkEntry(self.frame_options, font=FONT,
                                                       width=23)
        self.username_textbox.grid(row=1, column=3, sticky='e')

        self.username_button = customtkinter.CTkButton(self.frame_options, text="Join", font=BUTTON_FONT, command=lambda :self.chatclient.connect(f"{Session.user_id}"))
        self.username_button.grid(row=1, column=4, sticky='nsew')

        self.frame_typing_message = customtkinter.CTkFrame(master=self.frame_message,width=800,height=500,fg_color="Red")
        self.frame_typing_message.grid(row=2, column=1, sticky='nsew')
        self.frame_typing_message.grid_columnconfigure(1, weight=1)
        self.frame_typing_message.rowconfigure(1, weight=1)

        self.message_textbox = customtkinter.CTkEntry(self.frame_typing_message, font=FONT, width=38)
        self.message_textbox.grid(row=1, column=1, sticky='nsew')
        self.message_textbox.bind("<KeyPress>",lambda event:self.chatclient.start_typing(recive_id))
        self.message_textbox.bind("<KeyRelease>",lambda event: self.chatclient.stop_typing(recive_id))

        self.message_button = customtkinter.CTkButton(self.frame_typing_message, text="Send", font=BUTTON_FONT,  command=lambda :self.chatclient.send_message(Session.user_id,recive_id,chatting,conversation_id))
        self.message_button.grid(row=1, column=2, sticky='nsew')


        ###
        # Khung cuộn chứa tin nhắn
        import customtkinter as ctk
        from tkinter import Scrollbar

        # Khung cuộn chứa tin nhắn
        container = ctk.CTkFrame(self.frame_message, width=800, height=450)
        container.grid(row=1, column=1, sticky='nsew',padx=10, pady=10)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.scrollable_frame = ctk.CTkScrollableFrame(container,width=800,height=800,fg_color="lightgray")

        self.scrollable_frame.grid(row=0, column=0, sticky='nsew')
        self.scrollable_frame.grid_columnconfigure(2, weight=2)
        self.row = 0


        # Thêm tin nhắn vào khung
        print(recive_id)
        messages = chatting.get_message(conversation_id)
        print("thanhcong")
        recive_name=chatting.get_user_name(recive_id)
        print("thanhcong2")
        if messages:

            for i, msg in enumerate(messages, start=1):
                self.row += 1  # Tăng row cho mỗi tin nhắn
                # Tạo một frame mới cho mỗi tin nhắn
                frame_message_a = ctk.CTkFrame(self.scrollable_frame, fg_color="Pink")

                message_label = ctk.CTkLabel(frame_message_a, text=msg['message_text'], width=200, height=40,wraplength=200,
                                             fg_color="lightblue")
                message_label.grid(row=0, column=1, sticky='w', padx=10,
                                   pady=5)  # Đặt message_label vào frame_message_a

                print(msg['sender_id'])
                if msg['sender_id'] == Session.user_id:
                    username_label = ctk.CTkLabel(frame_message_a, font=FONT, text=f"{Session.username}")
                    username_label.grid(row=0, column=0, sticky='e', padx=10, pady=5)
                else:
                    username_label = ctk.CTkLabel(frame_message_a, font=FONT, text=recive_name[0]['username'])
                    username_label.grid(row=0, column=0, sticky='e', padx=10, pady=5)

                # Đặt frame_message_a vào vị trí chính xác
                frame_message_a.grid(row=self.row, column=1 if msg['sender_id'] == Session.user_id else 3,
                                     sticky='nsew', padx=10, pady=10)
        frame_empty = CTkFrame(self.scrollable_frame, width=800, height=450,fg_color="lightgray")
        frame_empty.grid(row=1, column=2, rowspan=self.row, sticky='nsew')
        self.scrollable_frame.update_idletasks()
        self.scrollable_frame._parent_canvas.yview_moveto(1.0)
        self.typ = CTkFrame(self.scrollable_frame, fg_color="Pink")
        self.typ_son=CTkLabel(self.typ, text="...", font=FONT)
        self.typ_son.grid(row=0, column=1, sticky='nsew')
        # self.typ.grid(column=1 if msg['sender_id'] == Session.user_id else 3, sticky='nsew')

        # Đặt khung cuộn



        # scrollbar.grid(row=0, column=1, sticky='ns')
        # self.message_box = scrolledtext.ScrolledText(self.frame_message, font=SMALL_FONT, width=67, height=26.5)
        # self.message_box.config(state=customtkinter.DISABLED)
        # self.message_box.grid(row=1, column=1, sticky='nsew')
        #
        # self.user_listbox = CTkListbox(self.frame_message, font=SMALL_FONT, width=100,
        #                                height=10)
        # self.user_listbox.grid(row=2, column=3, sticky='nsew')


if __name__ == "__main__":
    root = customtkinter.CTk()  # Tạo cửa sổ chính
    root.geometry("1500x900")
    root.minsize(width=400, height=800)
    chat_interface = ChatInterface(master=root)
    root.mainloop()
