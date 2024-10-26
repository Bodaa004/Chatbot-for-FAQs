import customtkinter as ctk
from chat import get_response, bot_name

class ChatApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat with " + bot_name)
        self.root.geometry("600x400")

        # Configure the appearance
        ctk.set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"
        ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"

        self.chat_window = ctk.CTkTextbox(root, wrap='word', state='disabled')
        self.chat_window.pack(padx=10, pady=10, fill='both', expand=True)

        self.entry_frame = ctk.CTkFrame(root)
        self.entry_frame.pack(padx=10, pady=10, fill='x', side='bottom')

        self.entry_box = ctk.CTkEntry(self.entry_frame, font=("Arial", 14))
        self.entry_box.pack(padx=10, pady=10, fill='x', expand=True, side='left')
        self.entry_box.bind("<Return>", self.send_message)

        self.send_button = ctk.CTkButton(self.entry_frame, text="Send", command=self.send_message)
        self.send_button.pack(padx=10, pady=10, side='right')

    def send_message(self, event=None):
        user_input = self.entry_box.get()
        if user_input.strip():
            self.chat_window.configure(state='normal')
            self.chat_window.insert('end', "You: " + user_input + "\n")
            self.entry_box.delete(0, 'end')

            response = get_response(user_input)
            if isinstance(response, str):  # Ensure the response is a string
                self.chat_window.insert('end', bot_name + ": " + response + "\n")
            else:
                self.chat_window.insert('end', bot_name + ": [Error: Response is not a string]\n")
            self.chat_window.yview('end')
            self.chat_window.configure(state='disabled')

if __name__ == "__main__":
    root = ctk.CTk()
    app = ChatApplication(root)
    root.mainloop()
