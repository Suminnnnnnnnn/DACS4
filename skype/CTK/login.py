import hashlib
from customtkinter import *
from PIL import Image
from CTK.security.token import get_token
from CTK.security.token import verify_token
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from CTK.Model.db import DB
from CTK.Model.session import Session
from CTK.View.main import create_main_window


def auto_login():
    if os.path.exists("token.txt"):
        with open("token.txt", "r") as f:
            token = f.read().strip()
        # Xác minh token
        decoded = verify_token(token)
        print(decoded)
        if decoded:
            # Tự động thiết lập session
            Session.set_user(decoded['user_id'], decoded['username'], decoded['email'], token)
            try:
                    create_main_window()
            except Exception as e:
                print(f"Lỗi trong show_main: {e}")
            print("Tự động đăng nhập thành công!")
            return True
        else:
            print("Token không hợp lệ hoặc đã hết hạn. Yêu cầu đăng nhập lại.")
            create_login_window()
    else:
        print("Không tìm thấy token. Yêu cầu đăng nhập.")
        create_login_window()
    return False

def get_value():
    try:
        email_get = email.get()
        password_get = password.get()
        password_hash = hashlib.sha256(password_get.encode('utf-8')).hexdigest()
        value = (email_get, password_hash)
        data = db.fetch_query(query, value)
        print(data)

        if data and data[0]['email'] == email_get and data[0]['password_hash'] == password_hash:

            Session.set_user(user_id=data[0]['user_id'], username=data[0]['username'], email=data[0]['email'])
            token= get_token(email_get,password_get)
            show_main()
        else:
            print("Sai data hoặc không tìm thấy người dùng")
    except Exception as e:
        print(f"Lỗi trong get_value: ",e)

def show_main():
    try:
        if app:
            app.destroy()
            create_main_window()

    except Exception as e:
        print(f"Lỗi trong show_main: {e}")

def show_sign_up(event=None):  # Thêm tham số event
    try:
        app.destroy()
        from signup import create_signup_window  # Giả sử bạn có hàm này trong signup.py
        create_signup_window()
    except Exception as e:
        print(f"Lỗi trong show_sign_up: {e}")


def create_login_window():
    # Tạo giao diện chính
    global app,email,password,db,query
    app = CTk()
    app.geometry("600x480")
    app.resizable(0, 0)

    # Kết nối cơ sở dữ liệu
    db = DB(host="localhost", user="root", password="", database="skype")
    query = "SELECT * FROM users WHERE email=%s AND password_hash=%s"

    # Load hình ảnh
    side_img_data = Image.open("side-img.png")
    email_icon_data = Image.open("email-icon.png")
    password_icon_data = Image.open("password-icon.png")
    google_icon_data = Image.open("google-icon.png")

    # Tạo các thành phần giao diện
    side_img = CTkImage(dark_image=side_img_data, light_image=side_img_data, size=(300, 480))
    email_icon = CTkImage(dark_image=email_icon_data, light_image=email_icon_data, size=(20, 20))
    password_icon = CTkImage(dark_image=password_icon_data, light_image=password_icon_data, size=(17, 17))
    google_icon = CTkImage(dark_image=google_icon_data, light_image=google_icon_data, size=(17, 17))

    CTkLabel(master=app, text="", image=side_img).pack(expand=True, side="left")

    frame = CTkFrame(master=app, width=300, height=480, fg_color="#ffffff")
    frame.pack_propagate(0)
    frame.pack(expand=True, side="right")

    CTkLabel(master=frame, text="Welcome Back!", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 24)).pack(anchor="w", pady=(50, 5), padx=(25, 0))

    sign_in = CTkLabel(master=frame, text="Sign in to your account", text_color="#7E7E7E", anchor="w", justify="left", font=("Arial Bold", 12))
    sign_in.pack(anchor="w", padx=(25, 0))
    sign_in.bind("<Button-1>", lambda event: show_sign_up())  # Sửa ở đây

    CTkLabel(master=frame, text="  Email:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 14), image=email_icon, compound="left").pack(anchor="w", pady=(38, 0), padx=(25, 0))

    email = CTkEntry(master=frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000")
    email.pack(anchor="w", padx=(25, 0))

    CTkLabel(master=frame, text="  Password:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 14), image=password_icon, compound="left").pack(anchor="w", pady=(21, 0), padx=(25, 0))

    password = CTkEntry(master=frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000", show="*")
    password.pack(anchor="w", padx=(25, 0))

    login = CTkButton(master=frame, text="Login", fg_color="#601E88", hover_color="#E44982", font=("Arial Bold", 12), text_color="#ffffff", width=225, command=get_value)
    login.pack(anchor="w", pady=(40, 0), padx=(25, 0))

    CTkButton(master=frame, text="Continue With Google", fg_color="#EEEEEE", hover_color="#EEEEEE", font=("Arial Bold", 9), text_color="#601E88", width=225, image=google_icon).pack(anchor="w", pady=(20, 0), padx=(25, 0))
    print(os.listdir())


    app.mainloop()
if __name__ == "__main__":
    auto_login()

