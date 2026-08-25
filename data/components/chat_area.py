import customtkinter as ctk
from components.chat_bubble import ChatBubble


class ChatArea(ctk.CTkScrollableFrame):

    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color="transparent"
        )

        self.messages = []

        # Welcome Message
        self.add_ai_message(
            "👋 Welcome to NeuroCalc v3.0!\n\n"
            "I'm your AI learning companion.\n"
            "Ask me anything..."
        )

    # ----------------------------
    # Add User Message
    # ----------------------------
    def add_user_message(self, message):

        bubble = ChatBubble(
            self,
            message,
            sender="user"
        )

        # THIS WAS MISSING
        bubble.pack(
            fill="x",
            padx=10,
            pady=5
        )

        self.messages.append(bubble)

        self.after(100, self.scroll_to_bottom)

    # ----------------------------
    # Add AI Message
    # ----------------------------
    def add_ai_message(self, message):

        bubble = ChatBubble(
            self,
            message,
            sender="ai"
        )

        # THIS WAS MISSING
        bubble.pack(
            fill="x",
            padx=10,
            pady=5
        )

        self.messages.append(bubble)

        self.after(100, self.scroll_to_bottom)

    # ----------------------------
    # Auto Scroll
    # ----------------------------
    def scroll_to_bottom(self):
        self.update_idletasks()
        self._parent_canvas.yview_moveto(1.0)

    # ----------------------------
    # Reset Chat
    # ----------------------------
    def reset_chat(self):

        for widget in self.winfo_children():
            widget.destroy()

        self.messages.clear()

        self.add_ai_message(
            "👋 New conversation started.\n\n"
            "How can I help you today?"
        )