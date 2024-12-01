from datetime import datetime, timedelta
import jwt
import os

class Session:
    user_id = None
    username = None
    email = None
    token = None
    SECRET_KEY = "messironaldo"  # Khóa bí mật cho JWT

    @classmethod
    def set_user(cls, user_id, username, email, token=None):
        cls.user_id = user_id
        cls.username = username
        cls.email = email
        cls.token = token

    @classmethod
    def get_user(cls):
        return cls.user_id, cls.username, cls.email

    @classmethod
    def clear_session(cls):
        cls.user_id = None
        cls.username = None
        cls.email = None
        cls.token = None

    # @classmethod
    # def create_token(cls):
    #     """Tạo token chứa thông tin người dùng"""
    #     if cls.user_id and cls.username and cls.email:
    #         token = jwt.encode(
    #             {"user_id": cls.user_id, "username": cls.username, "email": cls.email, "exp": datetime.utcnow() + timedelta(days=1)},
    #             cls.SECRET_KEY,
    #             algorithm="HS256"
    #         )
    #         cls.token = token
    #         return token
    #     raise ValueError("Session chưa có thông tin người dùng để tạo token!")
    #
    # @classmethod
    # def verify_token(cls, token):
    #     """Xác minh token và trả về thông tin nếu hợp lệ"""
    #     try:
    #         decoded = jwt.decode(token, cls.SECRET_KEY, algorithms=["HS256"])
    #         return decoded  # Trả về dữ liệu trong token
    #     except jwt.ExpiredSignatureError:
    #         print("Token đã hết hạn!")
    #     except jwt.InvalidTokenError:
    #         print("Token không hợp lệ!")
    #     return None
