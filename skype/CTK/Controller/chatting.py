

from CTK.Model.db import DB



class Chatting:
    def __init__(self,user_id):

        self.db = DB(host="localhost", user="root", password="", database="skype")
        self.user_id = user_id

#     def get_conversations(self):
#         query="""
#     SELECT c.conversation_id, c.name, c.is_group
# FROM conversations c
# JOIN conversation_participants cp ON c.conversation_id = cp.conversation_id
# WHERE cp.user_id = %s
#     """
#         value=self.db.fetch_query(query, (self.user_id,))
#         conversations_id=value['conversation_id']
#         query1 = """ Select user_id from conversations_participants where conversation_id = (%s)  """
#         value1=self.db.fetch_query(query1, (conversations_id,))
#         result=((value),(value1))
#         return result
    def get_conversations(self):
        query = """
        SELECT c.conversation_id, c.name, c.is_group
        FROM conversations c
        JOIN conversation_participants cp ON c.conversation_id = cp.conversation_id
        WHERE cp.user_id = %s
        """
        conversations = self.db.fetch_query(query, (self.user_id,))

        result = []
        for conversation in conversations:
            conversation_id = conversation['conversation_id']

            # Lấy tất cả các user_id tham gia cuộc trò chuyện này
            query1 = "SELECT user_id FROM conversation_participants WHERE conversation_id = %s"
            participants = self.db.fetch_query(query1, (conversation_id,))

            # Thêm thông tin cuộc trò chuyện và người tham gia vào kết quả
            result.append({
                'conversation': conversation,
                'participants': participants
            })
        print(result)
        return result

    def send_message(self,conversation_id,sender_id,message):
        query="""
        INSERT INTO messages (conversation_id, sender_id, message_text)
        VALUES (%s, %s, %s)
    """
        value=(conversation_id, sender_id, message)
        self.db.execute_query(query, value)
    def get_message(self,conversation_id):
        query=""" Select sender_id, message_text from messages where conversation_id = %s ORDER BY sent_at  """
        messages = self.db.fetch_query(query, (conversation_id,))
        print(f"Cac tin nhan: {messages}")
        return messages
    def get_user_name(self,user_id):
        query=""" Select username from users where user_id = %s  """
        username = self.db.fetch_query(query, (user_id,))
        print(username)
        return username