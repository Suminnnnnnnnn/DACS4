# CTK/Controller/switch_phonebook.py
import mysql

from CTK.Model.db import DB
from CTK.Model.session import Session
from CTK import module
from CTK.security.token import verify_token


class SwitchViewPhoneBook:
    def __init__(self, view, list_view, selected_view):
        """
        view: đối tượng PhoneBook
        list_view: dict chứa các view với key là tên view
        selected_view: tên view cần hiển thị ban đầu
        """
        self.view = view
        self.db= DB(host="localhost", user="root", password="", database="skype")
        self.list_view = list_view  # dict
        self.selected_view = selected_view
        self.current_views = []  # Lưu trữ các view hiện tại
        self.switch_view(selected_view)  # Hiển thị view ban đầu

    def switch_view(self, selected_view):
        # Ẩn tất cả các view hiện tại
        if module.chat:
            module.chat.hide()
        print(self.current_views)
        for view in self.current_views:
            self.view.hide_another_list(view)

        # Lấy view cần hiển thị từ list_view
        view_to_show = self.list_view.get(selected_view)

        if view_to_show is not None:
            self.view.show_another_list(view_to_show)
            self.current_views = [view_to_show]  # Cập nhật current_views thành danh sách chứa view_to_show
            print(f"Đã chuyển đến view: {selected_view}")
        else:
            print(f"View '{selected_view}' không tồn tại trong list_view.")

    def get_list_fr(self):
        user = Session.get_user()


        query = """
                    SELECT users.username , users.user_id
                    FROM friends 
                    JOIN users ON friends.friend_id = users.user_id 
                    WHERE friends.user_id = %s AND friends.status = 'accepted'
                    UNION
                    SELECT users.username , users.user_id
                    FROM friends 
                    JOIN users ON friends.user_id = users.user_id   
                    WHERE friends.friend_id = %s AND friends.status = 'accepted'
                    """
        result = self.db.fetch_query(query, (user[0], user[0]))
        usernames = [{'username': row['username'], 'user_id': row['user_id']} for row in result]
            # Danh sách các username


        return usernames

    def get_list_invi(self):
        user = Session.get_user()
        query = "SELECT SQL_NO_CACHE user_id, friend_id FROM friends WHERE friend_id=%s AND status='pending'"
        friend_ids = self.db.fetch_query(query, (user[0],))
        invitations = []  # Danh sách chứa thông tin về lời mời kết bạn

        for friend in friend_ids:
            query1 = "SELECT SQL_NO_CACHE username FROM users WHERE user_id=%s"
            result = self.db.fetch_query(query1, (friend['user_id'],))
            if result:
                invitations.append({
                    'friend_id': friend['user_id'],  # Thêm friend_id vào kết quả
                    'username': result[0]['username']  # Thêm username vào kết quả
                })

        print(invitations)
        return invitations  # Trả về danh sách các từ điển

    def accept_friend_request(self, to_user):
       query="UPDATE friends SET status = 'accepted' WHERE user_id = %s AND friend_id = %s AND status = 'pending'"
       value=(to_user,Session.user_id)
       query1= "INSERT INTO friends(user_id, friend_id, status) VALUES(%s, %s, 'accepted')"
       value1=(Session.user_id, to_user)
       self.db.execute_query(query,value)
       self.db.execute_query(query1,value1)
    def reject_friend_request(self, to_user):
        # Thực thi
        value=(to_user,Session.user_id)
        self.db.execute_query("UPDATE friends SET status='blocked' WHERE user_id=%s AND friend_id=%s",
                             value)

    def chatting(self,recive_id):
        querycheck = """
        SELECT conversation_id 
        FROM conversations 
        WHERE is_group = 0 
        AND (SELECT COUNT(*) 
             FROM conversation_participants 
             WHERE conversation_id = conversations.conversation_id 
             AND user_id IN (%s, %s)) = 2
        """
        conversations = self.db.fetch_query(querycheck, (Session.user_id, recive_id))

        if conversations:
            print(conversations[0]['conversation_id'])
            return conversations[0]['conversation_id']
        else:
            try:
                recive_name=self.get_user_name(recive_id)
                query1 = "INSERT INTO conversations (name, is_group) VALUES (%s, %s)"
                self.db.execute_query(query1, (f"{Session.username} va {recive_name[0]['username']}", 0))

                conversation_id = self.db.cursor.lastrowid
                print(f"Last inserted conversation ID: {conversation_id}")

                if conversation_id:
                    query2 = """
                    INSERT INTO conversation_participants (conversation_id, user_id) 
                    VALUES (%s, %s), (%s, %s)
                    """
                    self.db.execute_query(query2, (conversation_id, Session.user_id, conversation_id, recive_id))
                    print("Thêm thành công chat")
                    print(conversation_id)
                    return conversation_id

                else:
                    print("Không thể lấy được conversation_id")
            except mysql.connector.Error as err:
                print(f"Lỗi khi thực thi truy vấn: {err}")

    def get_user_name(self, user_id):
        query = """ Select username from users where user_id = %s  """
        username = self.db.fetch_query(query, (user_id,))
        print(username)
        return username