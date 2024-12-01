import customtkinter
from customtkinter import CTkFrame, CTkScrollableFrame
from CTK import module
from CTK.Controller.chatting import Chatting
from CTK.Model.session import Session


class HistoryChat:
    def __init__(self, master,chat):
        self.title="historychat"
        self.master = master
        self.row=1
        # Tạo frame_state
        self.chat = chat
        self.chatting = Chatting(Session.user_id)
        module.chatting = self.chatting
        self.frame_state = customtkinter.CTkFrame(master=self.master, width=300, height=60, fg_color="#FFFFFF")
        # self.frame_state.grid(row=1, column=0, padx=10, pady=(5, 5), sticky="ew")
        self.frame_state.grid_columnconfigure(0, weight=1)
        self.frame_state.grid_columnconfigure(1, weight=1)
        self.frame_state.grid_columnconfigure(2, weight=1)

        # Tạo label_all và label_not_read
        self.label_all = customtkinter.CTkLabel(master=self.frame_state, width=100, height=30, text="Tất cả",
                                                fg_color="lightgreen", text_color="black", corner_radius=5)
        self.label_all.grid(row=0, column=1, padx=10, pady=10)
        self.selected_label = self.label_all  # Khởi tạo label_all là label được chọn mặc định

        # Gán sự kiện cho label_all
        self.bind_label_events(self.label_all)

        self.label_not_read = customtkinter.CTkLabel(master=self.frame_state, width=100, height=30, text="Chưa đọc",
                                                     fg_color="white", text_color="black", corner_radius=5)
        self.label_not_read.grid(row=0, column=2, padx=10, pady=10)
        self.bind_label_events(self.label_not_read)

        # Tạo separator1
        self.separator1 = customtkinter.CTkFrame(master=self.master, width=300, height=2, fg_color="#EEEEEE")
        # self.separator1.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="ew")

        # Tạo canvas history message
        self.create_canvas_history()

    def bind_label_events(self, label):
        label.bind("<Enter>", lambda event: self.on_enter(event, label))  # Khi chuột vào Label
        label.bind("<Leave>", lambda event: self.on_leave(event, label))  # Khi chuột rời khỏi Label
        label.bind("<Button-1>", lambda event: self.select_label(label))  # Khi nhấn vào Label

    def create_canvas_history(self):
        # Tạo canvas
        self.container=CTkFrame(master=self.master, width=300, height=800, fg_color="Red",
                                                      )
        self.container.grid_columnconfigure(0,weight=1)
        self.container.grid_rowconfigure(0,weight=1)
        self.frame_scroll=CTkScrollableFrame(self.container)
        self.frame_scroll.grid(row=0, column=0,sticky="nsew" )
        self.frame_scroll.grid_columnconfigure(0,weight=1)
        # self.canvas_history = customtkinter.CTkCanvas(master=self.master, width=300, height=800, bg="#FFFFFF",
        #                                               highlightthickness=0)
        # self.canvas_history.grid(row=3, column=0, sticky="nsew")

        # Tạo scrollbar
        # self.scrollbar_history = customtkinter.CTkScrollbar(master=self.canvas_history, orientation="vertical",
        #                                                     command=self.canvas_history.yview, width=15,
        #                                                     corner_radius=20)
        # self.scrollbar_history.place(relx=0.98, rely=0, relheight=1,
        #                              anchor="ne")  # Điều chỉnh relx để lấn vào bên trái một chút
        #
        # # Liên kết scrollbar với canvas
        # self.canvas_history.configure(yscrollcommand=self.scrollbar_history.set)

        # Tạo một frame bên trong canvas để chứa các tin nhắn
        self.frame_history_content = customtkinter.CTkFrame(self.frame_scroll, width=300, height=700,
                                                            fg_color="#FFFFFF")
        self.frame_history_content.grid(row=0, column=0,sticky="nsew" ,padx=10, pady=10)

        # self.canvas_history.create_window((0, 0), window=self.frame_history_content, anchor="nw")

        # Cấu hình để canvas có thể cuộn
        # self.frame_history_content.bind("<Configure>", lambda e: self.canvas_history.configure(
        #     scrollregion=self.canvas_history.bbox("all")))

        # Thêm một vài CTkLabel vào frame_history_content để kiểm tra chức năng cuộn
        # for i in range(60):  # Thêm nhiều label để kiểm tra việc cuộn
        #     self.row += 1
        #     label = customtkinter.CTkLabel(
        #         master=self.frame_history_content,
        #         text=f"Tin nhắn {i + 1}",
        #         width=295,
        #         height=30,
        #         fg_color="lightgray"
        #     )
        #     label.grid(row=self.row, column=0, padx=5, pady=5)
        #     label.bind("<Button-1>", lambda event: self.chat.chatting())
        self.load_conversations()
        # Bind sự kiện cuộn chuột vào canvas
        # self.canvas_history.bind_all("<MouseWheel>", self.on_mousewheel)

    def on_enter(self, event, label):
        label.configure(fg_color="lightgreen")

    def on_leave(self, event, label):
        if label != self.selected_label:
            label.configure(fg_color="white")

    def select_label(self, label):
        self.selected_label.configure(fg_color="white")  # Đặt lại màu cho label đã chọn
        self.selected_label = label  # Cập nhật label đã chọn
        label.configure(fg_color="lightgreen")  # Đặt màu cho label được chọn

    # def on_mousewheel(self, event):
    #     self.canvas_history.yview_scroll(int(-1 * (event.delta // 120)), "units")  # Cuộn canvas
    def hide(self):
        self.container.grid_remove()
        self.frame_state.grid_remove()

    def show(self):
        # chat_interface = ChatInterface(self.master)
        # chat_interface.show()
        self.frame_state.grid(row=1, column=0, padx=10, pady=(5, 5), sticky="ew")
        self.separator1.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="ew")
        self.container.grid(row=3, column=0, sticky="nsew")

    def load_conversations(self):
        try:

            conversations = self.chatting.get_conversations()  # Lấy danh sách các cuộc trò chuyện từ Chatting
            self.row = 0

            for conversation in conversations:
                self.row += 1
                participants = conversation['participants']
                recive_id = None

                for participant in participants:
                    user_id = participant['user_id']
                    if user_id and user_id != Session.user_id:
                        recive_id = user_id
                        break
                if recive_id is None:
                    continue  # Bỏ qua cuộc trò chuyện nếu không có recive_id

                print(f"recive id: {recive_id}")

                label = customtkinter.CTkLabel(
                    master=self.frame_history_content,
                    text=f"Cuộc trò chuyện với {conversation['conversation']['name']}",
                    width=300,
                    height=30,
                    fg_color="lightgray"
                )
                label.grid(row=self.row, column=0, padx=5, pady=5,sticky="ew")

                # Sử dụng lambda để truyền 'conversation_id' và 'recive_id' vào hàm on_click_label
                label.bind("<Button-1>", lambda event, cid=conversation['conversation']['conversation_id'],
                                                rid=recive_id: self.on_click_label(event, cid, rid))
                self.frame_history_content.columnconfigure(0, weight=1)
        except Exception as e:
            print("Lỗi load conversation:", str(e))

    def on_click_label(self, event, conversation_id, recive_id):
        print(f"Clicked label with conversation_id: {conversation_id}, recive_id: {recive_id}")
        self.chat.chatting(conversation_id, recive_id,self.chatting)

        #     for i in range(2):
        #         self.row+=1
        #         label = customtkinter.CTkLabel(
        #                     master=self.frame_history_content,
        #                     text=f"Cuộc trò chuyện với ",
        #                     width=295,
        #                     height=30,
        #                     fg_color="lightgray"
        #                 )
        #         label.grid(row=self.row, column=0, padx=5, pady=5)
        #         # Gán sự kiện nhấp chuột đơn giản để kiểm tra
        #         label.bind("<Button-1>", lambda event: print("Label clicked"))


# Sử dụng class ChatInterface
# if __name__ == "__main__":
#     root = customtkinter.CTk()  # Tạo cửa sổ chính
#     chat_interface = HistoryChat(master=root)
#     root.mainloop()
