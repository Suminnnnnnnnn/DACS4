# switch_view.py

class SwitchView:
    def __init__(self, list_view, selected_view):
        """
        list_view: dict chứa các view với key là tên view
        selected_view: tên view cần hiển thị ban đầu
        """
        self.list_view = list_view  # dict
        self.selected_view = selected_view
        self.current_views = []
        self.switch_view(selected_view)

    def switch_view(self, selected_view):
        # Định nghĩa mapping từ selected_view đến các view cần hiển thị
        view_mapping = {
            "phonebook": ["phonebook"],
            "historychat": ["historychat", "chat"],
            "chat": ["chat"]
        }

        # Ẩn tất cả các view hiện tại
        for view in self.current_views:
            view.hide()
            print(f"Đã hide {view.title}")

        # Lấy danh sách các view cần hiển thị dựa trên selected_view
        views_to_show = [self.list_view[name] for name in view_mapping.get(selected_view, [])]

        # Hiển thị các view cần thiết
        for view in views_to_show:
            view.show()
            print(f"Đã hiển thị {view.title}")

        # Cập nhật current_views
        self.current_views = views_to_show

        for view in self.current_views:

            print(f"{view.title}")

        print(f"Đã chuyển đến view: {selected_view}")
