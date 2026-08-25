import customtkinter as ctk


class ChatBubble(ctk.CTkFrame):

    def __init__(self, parent, message, sender="ai"):
        super().__init__(
            parent,
            fg_color="transparent"
        )

        # ----------------------------
        # Main Row
        # ----------------------------
        self.row = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.row.pack(fill="x", padx=15, pady=8)

        # ----------------------------
        # User Bubble
        # ----------------------------
        if sender == "user":

            self.row.grid_columnconfigure(0, weight=1)

            bubble = ctk.CTkFrame(
                self.row,
                fg_color="#2563EB",
                corner_radius=18
            )

            bubble.grid(
                row=0,
                column=1,
                sticky="e"
            )

            title = ctk.CTkLabel(
                bubble,
                text="👤 You",
                font=("Arial", 13, "bold")
            )

            title.pack(anchor="e", padx=15, pady=(10, 2))

            text = ctk.CTkLabel(
                bubble,
                text=message,
                justify="left",
                wraplength=600,
                font=("Arial", 15)
            )

            text.pack(
                padx=15,
                pady=(0, 12)
            )

        # ----------------------------
        # AI Bubble
        # ----------------------------
        else:

            self.row.grid_columnconfigure(1, weight=1)

            bubble = ctk.CTkFrame(
                self.row,
                fg_color="#1E293B",
                corner_radius=18
            )

            bubble.grid(
                row=0,
                column=0,
                sticky="w"
            )

            title = ctk.CTkLabel(
                bubble,
                text="🤖 NeuroCalc",
                font=("Arial", 13, "bold")
            )

            title.pack(anchor="w", padx=15, pady=(10, 2))

            text = ctk.CTkLabel(
                bubble,
                text=message,
                justify="left",
                wraplength=600,
                font=("Arial", 15)
            )

            text.pack(
                padx=15,
                pady=(0, 12)
            )