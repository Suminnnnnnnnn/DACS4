# signup.py
import datetime
import hashlib
import os  # Thêm dòng này nếu bạn sử dụng os
from customtkinter import *
from PIL import Image
from CTK.Model.db import DB
from Model import db
from websockets import connect


def get_value():
    try:
        user_name = entry_user_name.get()
        email = entry_email.get()
        password = entry_password.get()
        password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        value = (user_name, password_hash, email, datetime.datetime.now())
        db.execute_query(query, value)
        show_login()
    except Exception as e:
        print(f"Lỗi trong get_value: {e}")


def show_login(event=None):
    try:
        app.destroy()  # Đóng cửa sổ Sign Up hiện tại
        import login  # Mở giao diện login từ file login.py
        # login.create_login_window()  # Nếu cần, gọi hàm cụ thể
        print("hi")
    except Exception as e:
        print(f"Lỗi trong show_login: {e}")


def create_signup_window():
    global db, query, app, entry_user_name, entry_email, entry_password
    db = DB(host="localhost", user="root", password="", database="skype")
    query = "INSERT INTO users (username, password_hash, email, created_at) VALUES (%s, %s, %s, %s)"
    app = CTk()
    app.geometry("600x480")
    app.resizable(0, 0)

    side_img_data = Image.open("side-img.png")
    email_icon_data = Image.open("email-icon.png")
    password_icon_data = Image.open("password-icon.png")
    avt_icon_data = Image.open("assets/images/pharmacist.png")  # Đổi tên biến để tránh trùng

    side_img = CTkImage(dark_image=side_img_data, light_image=side_img_data, size=(300, 480))
    email_icon = CTkImage(dark_image=email_icon_data, light_image=email_icon_data, size=(20, 20))
    password_icon = CTkImage(dark_image=password_icon_data, light_image=password_icon_data, size=(17, 17))
    avt_icon = CTkImage(dark_image=avt_icon_data, light_image=avt_icon_data, size=(17, 17))  # Sử dụng avt_icon_data

    CTkLabel(master=app, text="", image=side_img).pack(expand=True, side="left")

    frame = CTkFrame(master=app, width=300, height=480, fg_color="#ffffff")
    frame.pack_propagate(0)
    frame.pack(expand=True, side="right")

    CTkLabel(master=frame, text="Welcome Back!", text_color="#601E88", anchor="w", justify="left",
             font=("Arial Bold", 24)).pack(anchor="w", pady=(50, 5), padx=(25, 0))

    login_label = CTkLabel(master=frame, text="Log in", text_color="#7E7E7E", anchor="w", justify="left",
                           font=("Arial Bold", 12))
    login_label.pack(anchor="w", padx=(25, 0))
    login_label.bind("<Button-1>", show_login)  # Sử dụng hàm có nhận event

    CTkLabel(master=frame, text="  User name:", text_color="#601E88", anchor="w", justify="left",
             font=("Arial Bold", 14), image=avt_icon, compound="left").pack(anchor="w", pady=(21, 0), padx=(25, 0))
    entry_user_name = CTkEntry(master=frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1,
                               text_color="#000000")
    entry_user_name.pack(anchor="w", padx=(25, 0))

    CTkLabel(master=frame, text="  Email:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 14),
             image=email_icon, compound="left").pack(anchor="w", pady=(38, 0), padx=(25, 0))
    entry_email = CTkEntry(master=frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1,
                           text_color="#000000")
    entry_email.pack(anchor="w", padx=(25, 0))

    CTkLabel(master=frame, text="  Password:", text_color="#601E88", anchor="w", justify="left",
             font=("Arial Bold", 14), image=password_icon, compound="left").pack(anchor="w", pady=(21, 0), padx=(25, 0))
    entry_password = CTkEntry(master=frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1,
                              text_color="#000000", show="*")
    entry_password.pack(anchor="w", padx=(25, 0))

    CTkButton(master=frame, text="Sign Up", fg_color="#601E88", hover_color="#E44982", font=("Arial Bold", 12),
              text_color="#ffffff", width=225, command=get_value).pack(anchor="w", pady=(40, 0), padx=(25, 0))

    app.mainloop()


if __name__ == "__main__":
    create_signup_window()
