import threading
import customtkinter as ctk
from components.chat_area import ChatArea
from components.sidebar import Sidebar
from core import NeuroCalcCore


class NeuroCalcGUI:

    def __init__(self):
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.window = ctk.CTk()
        self.window.title("NeuroCalc v2.0")
        self.window.geometry("1400x800")

        # Core engine instance handles intent routing
        self.core = NeuroCalcCore()

        # Main Layout
        self.main_frame = ctk.CTkFrame(self.window)
        self.main_frame.pack(fill="both", expand=True)

        # Sidebar
        self.sidebar = Sidebar(
            self.main_frame, self.new_chat, self.clear_chat
        )
        self.sidebar.pack(side="left", fill="y", padx=10, pady=10)

        # Content Frame
        self.content = ctk.CTkFrame(self.main_frame)
        self.content.pack(
            side="right", fill="both", expand=True, padx=10, pady=10
        )

        # Header
        self.header = ctk.CTkFrame(self.content, height=60)
        self.header.pack(fill="x", padx=10, pady=(10, 5))
        self.header.pack_propagate(False)

        self.header_title = ctk.CTkLabel(
            self.header,
            text="🧠 NeuroCalc v2.0",
            font=("Arial", 24, "bold"),
        )
        self.header_title.pack(side="left", padx=20)

        self.status = ctk.CTkLabel(
            self.header, text="🟢 Local Mode", font=("Arial", 16)
        )
        self.status.pack(side="right", padx=20)

        # Chat Area
        self.chat_box = ChatArea(self.content)
        self.chat_box.pack(fill="both", expand=True, padx=10, pady=10)

        # =============================
        # Bottom Input Area
        # =============================
        self.bottom = ctk.CTkFrame(self.content, fg_color="transparent")
        self.bottom.pack(fill="x", padx=20, pady=15)

        self.entry = ctk.CTkEntry(
            self.bottom,
            placeholder_text="Message NeuroCalc...",
            height=45,
            corner_radius=20,
            font=("Segoe UI", 15),
        )
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.entry.bind("<Return>", self.send_message_event)

        self.send_btn = ctk.CTkButton(
            self.bottom,
            text="➜",
            width=55,
            height=45,
            corner_radius=20,
            command=self.send_message,
        )
        self.send_btn.pack(side="right")

    def send_message(self):
        message = self.entry.get().strip()

        if not message:
            return

        # Display user message with blue tag formatting and clear entry
        self.chat_box.add_user_message(message)
        self.entry.delete(0, "end")

        # Disable input controls while processing
        self.send_btn.configure(state="disabled")
        self.entry.configure(state="disabled")

        # Process response via core in a background thread
        threading.Thread(
            target=self._process_response,
            args=(message,),
            daemon=True,
        ).start()

    def _process_response(self, message):
        """Processes request off the main UI thread with temporary feedback."""
        # Show thinking message on the main thread
        self.window.after(
            0, lambda: self.chat_box.add_ai_message("⏳ Thinking...")
        )

        try:
            response = self.core.process(message)
        except Exception as e:
            response = f"Error: {e}"

        # Update UI with the final answer on the main thread
        self.window.after(
            0, lambda: self._update_ui_with_response(response)
        )

    def _update_ui_with_response(self, response):
        """Replaces the loader and updates GUI elements on the main thread."""
        # Remove temporary loader if ChatArea supports it, or append cleanly
        if hasattr(self.chat_box, "replace_last_message"):
            self.chat_box.replace_last_message(str(response))
        else:
            self.chat_box.add_ai_message(str(response))

        # Re-enable input controls
        self.send_btn.configure(state="normal")
        self.entry.configure(state="normal")
        self.entry.focus()

    def new_chat(self):
        if hasattr(self.core, "reset_history"):
            self.core.reset_history()

        if hasattr(self.chat_box, "reset_chat"):
            self.chat_box.reset_chat()

    def clear_chat(self):
        if hasattr(self.chat_box, "reset_chat"):
            self.chat_box.reset_chat()

    def send_message_event(self, event):
        self.send_message()

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = NeuroCalcGUI()
    app.run()