import os
from tkinter import messagebox

import customtkinter as ctk
import mysql
from PIL import Image, ImageGrab, ImageFilter

from customtkinter import CTk, CTkFrame, CTkButton, CTkImage, CTkEntry, CTkLabel
from CTK.Controller.switch_view import SwitchView
from CTK.Model.db import DB
from CTK.Model.session import Session


from CTK.module import import_app
from CTK import module

# Khởi tạo biến toàn cục để theo dõi label đang được chọn

selected_label = None
selected_view  = None
global frame_1, history_chat,frame_chat,app,sw_v


db = DB(host="localhost", user="root", password="", database="skype")

# Lấy đường dẫn đến thư mục CTK (thư mục gốc của dự án)
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # CTK
assets_dir = os.path.join(base_dir, 'assets', 'images')  # Đường dẫn đến thư mục chứa hình ảnh

print(f"Base directory: {base_dir}")
print(f"Assets directory: {assets_dir}")

# Hàm tải hình ảnh
def load_image(filename, size):
    image_path = os.path.join(assets_dir, filename)
    print(f"Loading image from: {image_path}")  # Kiểm tra đường dẫn
    if not os.path.exists(image_path):
        print(f"File not found: {image_path}")
        raise FileNotFoundError(f"File not found: {image_path}")
    image = Image.open(image_path).resize(size)
    return CTkImage(image, size=size)

def sw_view(selected_view):
  sw_v.switch_view(selected_view)

def add_fr(entry_friend):
    email_add = (entry_friend.get(),)
    print(email_add)

    query = "SELECT * FROM users WHERE email=%s"
    data = db.fetch_query(query, email_add)
    print(data)

    if data and data[0]['email']:
        query_addfr = "INSERT INTO friends (user_id, friend_id, status) VALUES (%s, %s, %s)"
        values_addfr = (Session.user_id, data[0]['user_id'], 'pending')  # Truyền giá trị vào tuple
        db.execute_query(query_addfr, values_addfr)
        print("Da gui loi moi kb")
    else:
        print("Sai data hoặc không tìm thấy người dùng")


# Hàm tạo nhóm
def create_group(name, user_ids):
        try:
            # Tạo nhóm mới
            query="INSERT INTO conversations (name, is_group) VALUES (%s, %s)"
            db.execute_query(query,(name,True))
            conversation_id = db.cursor.lastrowid
            # Thêm các thành viên vào nhóm
            for user_id in user_ids:
                db.execute_query("INSERT INTO conversation_participants (conversation_id, user_id) VALUES (%s, %s)",
                               (conversation_id, user_id))
            print(f"Nhóm '{name}' đã được tạo với ID: {conversation_id}")
        except mysql as e:
            print(f"Lỗi khi tạo nhóm: {e}")




# Tạo cửa sổ thêm nhóm
def open_add_group_window():
    toplevel = ctk.CTkToplevel(app)
    toplevel.geometry("320x500")
    toplevel.maxsize(width=320, height=500)
    toplevel.grid_rowconfigure(2, weight=1)

    frame_container1 = ctk.CTkFrame(toplevel, fg_color="Red")
    frame_container1.grid(row=1, column=0)

    input_name = ctk.CTkEntry(frame_container1, placeholder_text="Enter group name")
    input_name.grid(row=0, column=0, padx=10, pady=10)

    def add_group():
        group_name = input_name.get().strip()
        if not group_name:
            messagebox.showerror("Invalid group name", "Group name cannot be empty")
            return

        selected_user_ids = get_selected_user_ids()
        if not selected_user_ids:
            messagebox.showerror("No users selected", "Please select at least one user to add to the group")
            return

        # Gọi hàm để tạo nhóm và thêm thành viên vào cơ sở dữ liệu
        selected_user_ids.append(int(Session.user_id))
        create_group(group_name, selected_user_ids)

    button_add = ctk.CTkButton(frame_container1, text="Add", command=add_group)
    button_add.grid(row=0, column=1, padx=10, pady=10)

    list_array = module.list_fr.friends_list
    print(list_array)

    frame_container2 = ctk.CTkFrame(toplevel, fg_color="Red")
    frame_container2.grid(row=2, column=0, sticky='nsew')
    frame_container2.grid_rowconfigure(0, weight=1)
    frame_container2.grid_columnconfigure(0, weight=1)

    frame_list = ctk.CTkFrame(frame_container2, fg_color="Green")
    frame_list.grid(row=0, column=0, sticky="ew")
    frame_list.grid_rowconfigure(0, weight=1)
    frame_list.grid_columnconfigure(0, weight=1)

    scroll_frame = ctk.CTkScrollableFrame(frame_list)
    scroll_frame.grid(row=0, column=0, sticky="nsew")
    global check_vars
    check_vars = []

    def checkbox_event(check_var):
        print("Checkbox toggled, current value:", check_var.get())

    for i, list_item in enumerate(list_array):
        frame_son = ctk.CTkFrame(scroll_frame)
        frame_son.grid(row=i, column=0, padx=10, pady=10)

        name_label = ctk.CTkLabel(frame_son, text=f"{list_item['username']}", width=120)
        name_label.grid(row=0, column=0)

        check_var = ctk.StringVar(value="off")
        checkbox = ctk.CTkCheckBox(frame_son, text="CTkCheckBox",
                                   command=lambda var=check_var: checkbox_event(var),
                                   variable=check_var,
                                   onvalue=list_item['user_id'],
                                   offvalue="off")
        checkbox.grid(row=0, column=1)

        check_vars.append(check_var)
# Hàm lấy tất cả user_id đã chọn
def get_selected_user_ids():
    selected_user_ids = []
    for check_var in check_vars:
        if check_var.get() != "off":
            selected_user_ids.append(int(check_var.get()))  # Chuyển đổi sang số nguyên
    print("Selected user IDs:", selected_user_ids)
    return selected_user_ids

# Gọi hàm để mở cửa sổ thêm nhóm



def create_blurred_overlay():
    app.update_idletasks()  # Cập nhật thông tin về kích thước cửa sổ trước khi tính toán

    # Chụp ảnh màn hình của cửa sổ chính
    x = app.winfo_rootx()
    y = app.winfo_rooty()
    w = app.winfo_width() + x
    h = app.winfo_height() + y
    screenshot = ImageGrab.grab(bbox=(x, y, w, h))

    # Làm mờ ảnh
    blurred_screenshot = screenshot.filter(ImageFilter.GaussianBlur(10))

    # Lưu ảnh tạm
    blurred_screenshot.save("blurred_background.png")

    # Tạo overlay frame phủ kín toàn bộ cửa sổ chính
    overlay = ctk.CTkFrame(master=app, width=app.winfo_width(), height=app.winfo_height(), fg_color="#000000")
    overlay.place(x=0, y=0)

    # Mở ảnh mờ đã lưu bằng Pillow
    bg_image_pil = Image.open("blurred_background.png")

    # Tạo CTkImage từ ảnh đã mở
    bg_image = ctk.CTkImage(dark_image=bg_image_pil, size=(app.winfo_width(), app.winfo_height()))

    # Sử dụng ảnh làm nền cho overlay
    bg_label = ctk.CTkLabel(master=overlay, image=bg_image, text="")
    bg_label.place(x=0, y=0)

    # Tạo modal
    modal_width = 600
    modal_height = 600
    modal = ctk.CTkFrame(master=overlay, width=modal_width, height=modal_height, fg_color="#f0f0f0")
    modal.columnconfigure(0, weight=3)
    modal.columnconfigure(2, weight=3)
    modal.rowconfigure(0, weight=1)
    modal.rowconfigure(5, weight=1)
    modal.place(x=750,y=450,anchor="center")

    # Thêm các widget vào modal
    label = ctk.CTkLabel(master=modal, text="Add Friend", font=("Arial", 16),width=200,height=100)
    label.grid(column=1, row=1,padx=10, pady=10)


    entry_friend = ctk.CTkEntry(master=modal, placeholder_text="Enter friend's email",width=200,height=100)
    entry_friend.grid(column=1, row=2,padx=10, pady=10)

    btn_submit = ctk.CTkButton(master=modal, text="Add Friend",width=200,height=100,command = lambda : add_fr(entry_friend))
    btn_submit.grid(column=1, row=3,padx=10, pady=10)

    btn_cancel = ctk.CTkButton(master=modal, text="Cancel", command=lambda: close_add_friend_modal(overlay, modal), width=200, height=100)
    btn_cancel.grid(column=1, row=4,padx=10, pady=10)
def close_add_friend_modal(overlay, modal):
    modal.destroy()
    overlay.destroy()

def show_chat():

    print("a")
# Hàm tạo và chạy cửa sổ chính
def create_main_window():
    global app,sw_v,chat # Để có thể truy cập từ các phần khác nếu cần
    # Khởi tạo ứng dụng
    app= import_app()
    # app = CTk()
    # app.geometry("1500x900")
    # app.title(f"{Session.username}")
    # app.resizable(True, True)

    # Tải hình ảnh cho các button
    try:
        ctk_img_user = load_image("pharmacist.png", (50, 50))
        ctk_img_chat = load_image("message.png", (40, 40))
        ctk_img_phone_book = load_image("phonebook.png", (40, 40))
        ctk_img_online = load_image("online-meeting.png", (40, 40))
        ctk_img_note = load_image("note-board.png", (40, 40))
        ctk_img_bot = load_image("bot.png", (40, 40))
        ctk_img_setting = load_image("setting.png", (40, 40))
        ctk_img_search = load_image("search.png", (20, 20))
        ctk_img_addfr=load_image("add-user.png", (20, 20))
        ctk_img_addgroup = load_image("employees.png", (20, 20))
    except FileNotFoundError as e:
        print(e)
        print("Đảm bảo rằng tất cả các tệp hình ảnh tồn tại trong thư mục assets/images.")
        return  # Kết thúc hàm nếu không tìm thấy tệp hình ảnh

    # Cấu hình lưới (grid) cho cửa sổ chính
    app.grid_columnconfigure(0, weight=0)  # Cột menu
    app.grid_columnconfigure(1, weight=0)  # Cột chứa frame_search và frame_history_mess
    app.grid_columnconfigure(2, weight=0)  # Cột separator
    app.grid_columnconfigure(3, weight=1)  # Cột chat
    app.grid_rowconfigure(0, weight=0)  # Hàng cho frame_search
    app.grid_rowconfigure(1, weight=0)  # Hàng cho frame_state
    app.grid_rowconfigure(2, weight=0)  # Hàng cho separator1
    app.grid_rowconfigure(3, weight=1)  # Hàng cho frame_history_mess

    # Tạo frame menu
    frame_menu = CTkFrame(master=app, width=100, height=800, fg_color="#1e90ff")
    frame_menu.grid(row=0, column=0, rowspan=4, padx=0, pady=0, sticky="nsew")
    frame_menu.grid_rowconfigure(6, weight=1)
    frame_menu.grid_rowconfigure(7, weight=1)
    frame_menu.grid_rowconfigure(8, weight=1)

    # Tạo các button trong frame_menu
    def create_menu_button(frame, image, row, **kwargs):
        btn = CTkButton(master=frame, width=50, height=50, image=image, text="", fg_color="#1e90ff", **kwargs)
        btn.grid(row=row, column=0, padx=20, pady=20)
        return btn

    btn_in4 = create_menu_button(frame_menu, ctk_img_user, 0, corner_radius=10, border_width=2, border_color="white")
    btn_chat = create_menu_button(frame_menu, ctk_img_chat, 1,command=lambda :sw_view("historychat"))


    btn_phone_book = create_menu_button(frame_menu, ctk_img_phone_book, 2,command= lambda :sw_view("phonebook"))
    btn_online = create_menu_button(frame_menu, ctk_img_online, 3)
    btn_note = create_menu_button(frame_menu, ctk_img_note, 4)
    btn_bot = create_menu_button(frame_menu, ctk_img_bot, 5)
    btn_setting = create_menu_button(frame_menu, ctk_img_setting, 9)

    # Tạo frame 1 (chứa frame_search và frame_history_mess)

    frame_1 = CTkFrame(master=app, width=400, height=850, fg_color="#FFFFFF")
    frame_1.grid(row=0, column=1, rowspan=4, padx=0, pady=0, sticky="nsew")
    frame_1.grid_columnconfigure(0, weight=1)
    frame_1.grid_rowconfigure(0, weight=0)  # frame_search
    frame_1.grid_rowconfigure(1, weight=0)  # frame_state
    frame_1.grid_rowconfigure(2, weight=0)  # separator1
    frame_1.grid_rowconfigure(3, weight=1)  # frame_history_mess

    # Tạo frame tìm kiếm
    frame_search = CTkFrame(master=frame_1, width=300, height=50, fg_color="#FFFFFF")
    frame_search.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="ew")

    # Tạo frame chứa search_icon và search_icon
    frame_search_1=CTkFrame(master=frame_search,width=200,height=50,fg_color="#FFFFFF", border_width=1, corner_radius=10)
    frame_search_1.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="ew")
    # Tạo icon tìm kiếm
    search_icon = CTkLabel(master=frame_search_1, width=20, height=20, fg_color="#FFFFFF", image=ctk_img_search, text=None)
    search_icon.grid(row=0, column=0, padx=5, pady=5, sticky="w")

    # Tạo ô tìm kiếm với viền xóa
    search_entry = CTkEntry(master=frame_search_1, width=200, height=20, placeholder_text="Tìm kiếm...", fg_color="#FFFFFF", border_width=0)
    search_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

    # Tạo button kết bạn, và tạo nhóm chat
    frame_add=CTkFrame(master=frame_search,width=200,height=50,fg_color="#FFFFFF", border_width=1, corner_radius=10)
    frame_add.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
    btn_addfr=CTkButton(master=frame_add,width=10,height=10,fg_color="#FFFFFF",image=ctk_img_addfr,text="",command=create_blurred_overlay)
    btn_addfr.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    btn_addgroup=CTkButton(master=frame_add,width=10,height=10,fg_color="#FFFFFF",image=ctk_img_addgroup,text="",command=open_add_group_window)
    btn_addgroup.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

    # history_chat = HistoryChat(master=frame_1)

    # Tạo vạch ranh giới bằng CTkFrame
    separator = CTkFrame(master=app, width=1, height=800, fg_color="#EEEEEE")
    separator.grid(row=0, column=2, rowspan=4, padx=0, pady=0, sticky="ns")

    # Tạo frame chat
    # frame_chat = ChatInterface(master=app)
    from CTK.View.phonebook import PhoneBook
    from CTK.View.chat import ChatInterface

    phonebook = PhoneBook(frame_1, app)
    module.phonebook=phonebook
    # global chat
    chat = ChatInterface(app)
    module.chat=chat
    from CTK.View.option import HistoryChat
    historychat = HistoryChat(frame_1,chat)

    list_view = {
        "phonebook": phonebook,
        "historychat": historychat,
        "chat": chat
    }
    sw_v=SwitchView(list_view,"phonebook")

    # Chạy ứng dụng
    app.minsize(width=400, height=800)
    app.mainloop()

# Chạy ứng dụng chỉ khi main.py được chạy trực tiếp
if __name__ == "__main__":
    create_main_window()
