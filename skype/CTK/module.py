from customtkinter import CTk

from CTK.Model.session import Session

chat = None
chatting=None
phonebook=None
list_fr=None
def import_app():
 app = CTk()
 app.geometry("1500x900")
 app.title(f"{Session.username}")
 app.resizable(True, True)
 return app

