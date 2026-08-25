import customtkinter as ctk


class ChatBubble(ctk.CTkFrame):
    def __init__(
        self,
        parent,
        message,
        sender="ai"
    ):
        super().__init__(
            parent,
            corner_radius=15
        )

        # Different colors for AI and User
        if sender == "user":
            bubble_color = "#2563EB"   # Blue
            text_color = "white"
            anchor = "e"
            title = "👤 You"

        else:
            bubble_color = "#1E293B"   # Dark Slate
            text_color = "white"
            anchor = "w"
            title = "🤖 NeuroCalc"

        self.configure(fg_color=bubble_color)

        self.pack(
            fill="x",
            padx=20,
            pady=8,
            anchor=anchor
        )

        self.title = ctk.CTkLabel(
            self,
            text=title,
            font=("Arial", 14, "bold"),
            text_color=text_color
        )

        self.title.pack(
            anchor="w",
            padx=15,
            pady=(10, 0)
        )

        self.message = ctk.CTkLabel(
            self,
            text=message,
            justify="left",
            wraplength=700,
            font=("Arial", 15),
            text_color=text_color
        )

        self.message.pack(
            anchor="w",
            padx=15,
            pady=(5, 12)
        )