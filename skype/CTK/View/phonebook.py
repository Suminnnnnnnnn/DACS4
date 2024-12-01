# CTK/View/phonebook.py
from CTK.Model.list import ListArray
from CTK import module
import customtkinter
from customtkinter import CTkLabel, CTkEntry, CTkButton
from PIL import Image
import os


def load_image(filename, size):
    """
    Tải hình ảnh từ thư mục assets/images dựa trên vị trí của file phonebook.py.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # CTK
    assets_dir = os.path.join(base_dir, 'assets', 'images')  # Đường dẫn đến thư mục chứa hình ảnh
    image_path = os.path.join(assets_dir, filename)
    print(f"PhoneBook - Loading image from: {image_path}")  # Kiểm tra đường dẫn
    if not os.path.exists(image_path):
        print(f"PhoneBook - File not found: {image_path}")
        raise FileNotFoundError(f"PhoneBook - File not found: {image_path}")
    image = Image.open(image_path).resize(size)
    return customtkinter.CTkImage(light_image=image, size=size)

class PhoneBook:
    def __init__(self, master, app):
        from CTK.Controller.switch_phonebook import SwitchViewPhoneBook
        self.app = app
        self.master = master
        self.title = "phonebook"

        # Tải hình ảnh
        self.img_icon = load_image("pharmacist.png", (50, 50))
        self.ctk_img_search = load_image("search.png", (20, 20))

        # Tạo frame_container và các widget khác
        self.frame_container = customtkinter.CTkFrame(master=self.master, width=800, height=300, fg_color="Red")
        self.frame_container.columnconfigure(0, weight=1)
        # Tạo các frame khác
        self.create_list_another(self.app)
        self.create_list_friend()
        self.create_frame_invitations()
        self.create_frame_group()
        self.create_frame_group_invitations()

        # Tạo list_view sau khi các frame đã được tạo
        self.list_view = {
            "frame_friend": self.frame_friend,
            "frame_group": self.frame_group,
            "frame_invitations": self.frame_invitations,
            "frame_group_invitations": self.frame_group_invitations
            # Thêm các view khác nếu cần
        }
        # Khởi tạo SwitchViewPhoneBook
        self.sw_phonebook = SwitchViewPhoneBook(self, self.list_view, "frame_friend")
        self.sw_phonebook.switch_view("frame_friend")
        print("sw_phonebook has been initialized.")
        # Tạo các nút với chữ căn giữa và thêm lệnh chuyển đổi view
        self.list_fr = customtkinter.CTkButton(
            master=self.frame_container,
            width=300,
            height=70,
            text="Danh sách",
            fg_color="lightgreen",
            text_color="black",
            corner_radius=5,
            anchor="center",
            command=lambda: self.sw_phonebook.switch_view("frame_friend")
        )
        self.list_fr.grid(row=1, column=0, padx=10, pady=(5, 5), sticky="nsew")

        self.list_group = customtkinter.CTkButton(
            master=self.frame_container,
            width=295,
            height=70,
            text="Danh sách nhóm",
            fg_color="lightgreen",
            text_color="black",
            corner_radius=5,
            anchor="right",
            command=lambda: self.sw_phonebook.switch_view("frame_group")
        )
        self.list_group.grid(row=2, column=0, padx=10, pady=(5, 5), sticky="nsew")

        self.fr_invitations = customtkinter.CTkButton(
            master=self.frame_container,
            width=295,
            height=70,
            text="Lời mời kết bạn",
            fg_color="lightgreen",
            text_color="black",
            corner_radius=5,
            anchor="right",
            command=lambda: self.sw_phonebook.switch_view("frame_invitations")
        )
        self.fr_invitations.grid(row=3, column=0, padx=10, pady=(5, 5), sticky="nsew")

        self.group_invitations = customtkinter.CTkButton(
            master=self.frame_container,
            width=295,
            height=70,
            text="Lời mời group",
            fg_color="lightgreen",
            text_color="black",
            corner_radius=5,
            anchor="right",
            command=lambda: self.sw_phonebook.switch_view("frame_group_invitations")
        )
        self.group_invitations.grid(row=4, column=0, padx=10, pady=(5, 5), sticky="nsew")






    def create_list_another(self, master):
        self.frame_list_fr = customtkinter.CTkFrame(master=self.app, width=800, height=800, fg_color="Red")
        self.frame_list_fr.columnconfigure(0, weight=1)
        self.frame_list_fr.rowconfigure(1, weight=1)
        # Tạo frame_head và frame_title
        self.frame_head = customtkinter.CTkFrame(master=self.frame_list_fr, width=800, height=100, fg_color="White")
        self.frame_head.grid(row=0, column=0, sticky='nsew')

        self.frame_title = customtkinter.CTkFrame(master=self.frame_head, width=300, height=300, fg_color="White")
        self.frame_title.grid(row=0, column=0, padx=10, pady=(5, 5), sticky="nsew")

        self.icon = customtkinter.CTkLabel(master=self.frame_title, width=50, height=50, image=self.img_icon, text="")
        self.icon.grid(row=0, column=0, padx=10, pady=(5, 5), sticky="nsew")

        self.label_title = customtkinter.CTkLabel(master=self.frame_title, width=50, height=50, text="Danh sách bạn bè")
        self.label_title.grid(row=0, column=1, padx=10, pady=(5, 5), sticky="nsew")

    def create_list_friend(self):
        # Tạo frame_friend
        self.frame_friend = customtkinter.CTkFrame(master=self.frame_list_fr, width=800, height=300, fg_color="Blue")
        self.frame_friend.columnconfigure(0, weight=1)
        self.frame_friend.rowconfigure(1, weight=1)

        # Tạo frame_search trong frame_friend
        self.frame_search = customtkinter.CTkFrame(master=self.frame_friend, width=800, height=100, fg_color="White")
        self.frame_search.grid(row=0, column=0, padx=10, pady=(5, 5), sticky="ew")

        # Tạo icon tìm kiếm
        search_icon = CTkLabel(master=self.frame_search, width=20, height=20, fg_color="#FFFFFF",
                               image=self.ctk_img_search, text=None)
        search_icon.grid(row=0, column=0, padx=5, pady=5)

        # Tạo ô tìm kiếm
        search_entry = CTkEntry(master=self.frame_search, width=200, height=20, placeholder_text="Tìm kiếm...",
                                fg_color="#FFFFFF", border_width=0)
        search_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Tạo son_frame_friend và các widget bên trong
        self.son_frame_friend = customtkinter.CTkFrame(master=self.frame_friend, width=800, height=300,
                                                       fg_color="Green")
        self.son_frame_friend.grid(row=1, column=0, padx=10, pady=(5, 5), sticky="nsew")
        self.son_frame_friend.columnconfigure(0, weight=1)

    def show_another_list(self, another_frame):
        if another_frame is not None:
            another_frame.grid(row=1, column=0, sticky='nsew')
            if not hasattr(self, 'sw_phonebook'):
                print("Error: sw_phonebook is not initialized")
                return
            if another_frame == self.frame_friend:

                self.label_title.configure(text="Danh sách bạn bè")
                data = self.sw_phonebook.get_list_fr()
                module.list_fr=ListArray()
                print(data)
                self.grandchildren_frame_friend = customtkinter.CTkFrame(master=self.son_frame_friend, width=800,
                                                                         height=300, fg_color="#FFFFFF")
                self.grandchildren_frame_friend.grid(row=0, column=0, padx=10, pady=(5, 5), sticky="nsew")
                for i, datas in enumerate(data):
                     module.list_fr.add_friend(datas['user_id'],datas['username'])
                     print(datas)
                     label_text = f"{datas['username']}"
                     self.label_friend = customtkinter.CTkLabel(master=self.grandchildren_frame_friend, width=20,
                                                               height=20, fg_color="Yellow", text=label_text)
                     self.label_friend.grid(row=i, column=0, padx=10, pady=(5, 5), sticky="ew")
                     self.label_friend.bind("<Button-1>", lambda event,
                                                rid=datas['user_id']: self.on_click_label(event, rid))
            elif another_frame == self.frame_invitations:

                self.label_title.configure(text="Lời mời kết bạn")
                data = self.sw_phonebook.get_list_invi()
                self.clear_frame(self.son_frame_invitations)  # Clear previous content

                for i, invitation in enumerate(data):  # Duyệt qua từng từ điển trong data
                    username = invitation['username']  # Lấy username
                    friend_id = invitation['friend_id']  # Lấy friend_id

                    label_text = f"{username}"
                    grandchildren_frame = customtkinter.CTkFrame(master=self.son_frame_invitations, width=800,
                                                                 height=50, fg_color="#FFFFFF")
                    grandchildren_frame.grid(row=i, column=0, padx=10, pady=(5, 5), sticky="nsew")
                    grandchildren_frame.columnconfigure(1, weight=1)
                    grandchildren_frame.columnconfigure(2, weight=1)
                    grandchildren_frame.columnconfigure(3, weight=1)

                    self.label_invi = customtkinter.CTkLabel(master=grandchildren_frame, width=50, height=50,
                                                             fg_color="Yellow", text=label_text)
                    self.label_invi.grid(row=0, column=0, padx=10, pady=(5, 5), sticky="ew")

                    # Cập nhật các lệnh cho nút Accept và Reject để sử dụng friend_id
                    self.button_accept = CTkButton(master=grandchildren_frame, width=50, height=50,
                                                   text="Accept invitation",
                                                   command=lambda : self.accept_invitation(
                                                       friend_id))
                    self.button_accept.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

                    self.button_reject = CTkButton(master=grandchildren_frame, width=50, height=50,
                                                   text="Reject invitation",
                                                   command=lambda : self.reject_invitation(
                                                       friend_id))
                    self.button_reject.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

            elif another_frame == self.frame_group:

                self.label_title.configure(text="Danh sách nhóm")
            elif another_frame == self.frame_group_invitations:

                self.label_title.configure(text="Lời mời vào nhóm")
        else:
            print("Error: another_frame is None")
    def on_click_label(self, event, recive_id):
        conversation_id=self.sw_phonebook.chatting(recive_id)
        module.chat.show()
        module.chat.chatting(conversation_id, recive_id,module.chatting)
    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def accept_invitation(self, friend_id):
        self.sw_phonebook.accept_friend_request(friend_id)
        self.sw_phonebook.switch_view("frame_invitations")
        print(f"Accepted invitation from {friend_id} ")
        # Thêm logic chấp nhận lời mời kết bạn

    def reject_invitation(self, friend_id):
        self.sw_phonebook.reject_friend_request(friend_id)
        self.sw_phonebook.switch_view("frame_invitations")
        print(f"Rejected invitation from {friend_id}")

    def hide_another_list(self, another_frame):
        if another_frame is not None:
            another_frame.grid_remove()
        else:
            print("Error: another_frame is None")

    def show(self):
        self.frame_container.grid(row=3, column=0, padx=10, pady=(5, 5), sticky="nsew")
        self.frame_list_fr.grid(row=0, column=3, rowspan=4, sticky='nsew')
        print("aa")

    def hide(self):
        self.frame_container.grid_remove()
        self.frame_list_fr.grid_remove()
    def create_frame_group(self):
        # Tạo frame_group
        self.frame_group = customtkinter.CTkFrame(master=self.frame_list_fr, width=800, height=300, fg_color="Purple")
        self.frame_group.columnconfigure(0, weight=1)
        self.frame_group.rowconfigure(1, weight=1)

    def create_frame_invitations(self):
        # Tạo frame_invitations
        self.frame_invitations = customtkinter.CTkFrame(master=self.frame_list_fr, width=800, height=300,
                                                        fg_color="Orange")
        self.frame_invitations.columnconfigure(0, weight=1)
        self.frame_invitations.rowconfigure(1, weight=1)
        self.son_frame_invitations = customtkinter.CTkFrame(master=self.frame_invitations, width=800, height=300,
                                                       fg_color="Green")
        self.son_frame_invitations.grid(row=1, column=0, padx=10, pady=(5, 5), sticky="nsew")
        self.son_frame_invitations.columnconfigure(0, weight=1)

    def create_frame_group_invitations(self):
        # Tạo frame_group_invitations
        self.frame_group_invitations = customtkinter.CTkFrame(master=self.frame_list_fr, width=800, height=300,
                                                              fg_color="Brown")
        self.frame_group_invitations.columnconfigure(0, weight=1)
        self.frame_group_invitations.rowconfigure(1, weight=1)
