import datetime
import mysql.connector
from mysql.connector import Error


class DB:
    def __init__(self, host, user, password, database):
        """Khởi tạo đối tượng DB và kết nối đến cơ sở dữ liệu MySQL."""
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None  # Thêm thuộc tính cursor
        # Tự động kết nối khi khởi tạo
        self.connect()

    def connect(self):
        """Tạo kết nối đến cơ sở dữ liệu MySQL."""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor()  # Khởi tạo cursor
                print("Kết nối thành công đến cơ sở dữ liệu MySQL")
        except Error as e:
            print(f"Lỗi khi kết nối đến MySQL: {e}")

    def execute_query(self, query, params=None):
        """Thực thi các truy vấn INSERT, UPDATE, DELETE."""
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
            print("Thực thi truy vấn thành công")
        except Error as e:
            print(f"Lỗi khi thực thi truy vấn: {e}")

    def execute_many(self, query, params_list):
        """Thực thi nhiều truy vấn INSERT cùng một lúc."""
        try:
            self.cursor.executemany(query, params_list)
            self.connection.commit()
            print("Thực thi truy vấn thành công cho nhiều dòng")
        except Error as e:
            print(f"Lỗi khi thực thi truy vấn: {e}")

    def fetch_query(self, query, params=None):
        """Thực thi truy vấn SELECT và trả về kết quả."""
        self.connect()
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query, params)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"Lỗi khi thực thi truy vấn: {e}")
            return None

    def close(self):
        """Đóng kết nối với cơ sở dữ liệu MySQL."""
        if self.connection.is_connected():
            self.cursor.close()  # Đóng cursor
            self.connection.close()
            print("Đã đóng kết nối với MySQL")




# Sử dụng class DB
if __name__ == "__main__":
    # Thông tin kết nối
    db = DB(host="localhost", user="root", password="", database="skype")

    # Thực hiện truy vấn SELECT
    result = db.fetch_query("SELECT * FROM users")
    print(result)

    # Thực hiện truy vấn INSERT nhiều dòng
    query = "INSERT INTO users (username, password_hash, email, created_at) VALUES (%s, %s, %s, %s)"
    values = [
        ("bim", "abc123", "bim@gmail.com", datetime.datetime.now()),
        ("sa", "abc123", "sa@gmail.com", datetime.datetime.now()),
        ("duc", "abc123", "duc@gmail.com", datetime.datetime.now()),
        ("huyen", "abc123", "huyen@gmail.com", datetime.datetime.now())
    ]
    db.execute_many(query, values)

    # Thực hiện lại truy vấn SELECT để kiểm tra kết quả
    result = db.fetch_query("SELECT * FROM users")
    print(result)

    # Đóng kết nối
    db.close()
