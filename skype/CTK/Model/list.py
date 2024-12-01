class ListArray:
    def __init__(self):
        self.friends_list = []

    def add_friend(self, user_id, username):
        friend = {
            'user_id': user_id,
            'username': username,
        }
        self.friends_list.append(friend)

    def remove_friend(self, user_id):
        self.friends_list = [friend for friend in self.friends_list if friend['user_id'] != user_id]

    def get_friend(self, user_id):
        for friend in self.friends_list:
            if friend['user_id'] == user_id:
                return friend
        return None

    def display_friends(self):
        for friend in self.friends_list:
            print(f"ID: {friend['user_id']}, Username: {friend['username']}")
#
#
# # Sử dụng class ListArray
# friends = ListArray()
#
# # Thêm bạn bè
# friends.add_friend(1, 'Alice', 'alice@example.com')
# friends.add_friend(2, 'Bob', 'bob@example.com')
#
# # Hiển thị danh sách bạn bè
# friends.display_friends()
#
# # Lấy thông tin bạn bè
# print(friends.get_friend(1))
#
# # Xóa bạn bè
# friends.remove_friend(1)
#
# # Hiển thị lại danh sách bạn bè sau khi xóa
# friends.display_friends()
