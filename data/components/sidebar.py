import customtkinter as ctk


class Sidebar(ctk.CTkFrame):
    def __init__(self, parent, new_chat_command, clear_chat_command):
        super().__init__(parent, width=250)

        self.pack_propagate(False)

        title = ctk.CTkLabel(
            self,
            text="🧠 NeuroCalc",
            font=("Arial", 28, "bold")
        )
        title.pack(pady=25)

        self.new_chat_btn = ctk.CTkButton(
            self,
            text="+ New Chat",
            command=new_chat_command
        )
        self.new_chat_btn.pack(fill="x", padx=20, pady=10)

        self.clear_chat_btn = ctk.CTkButton(
            self,
            text="🗑 Clear Chat",
            command=clear_chat_command
        )
        self.clear_chat_btn.pack(fill="x", padx=20)