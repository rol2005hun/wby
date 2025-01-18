import os
import socket
import tkinter as tk
from tkinter import ttk
from renderer import WBYRenderer

class Browser:
    def __init__(self, root):
        self.root = root
        self.root.title("Wolimby Search")
        self.root.geometry("1024x768")

        style = ttk.Style()
        style.configure("TButton", font=("Arial", 15), padding=(1, 1), width=3)

        nav_frame = ttk.Frame(root)
        nav_frame.pack(fill="x", pady=5)

        self.back_button = ttk.Button(nav_frame, text="←", style="TButton", command=self.go_back)
        self.back_button.pack(side="left", padx=5, pady=5)

        self.forward_button = ttk.Button(nav_frame, text="→", style="TButton", command=self.go_forward)
        self.forward_button.pack(side="left", padx=5, pady=5)

        self.refresh_button = ttk.Button(nav_frame, text="⟳", style="TButton", command=self.refresh_page)
        self.refresh_button.pack(side="left", padx=5, pady=5)

        self.url_entry = ttk.Entry(nav_frame, font=("Arial", 15), width=60)
        self.url_entry.pack(side="left", fill="x", expand=True, padx=5)
        self.url_entry.bind("<Return>", self.on_return_pressed)

        self.display_area = tk.Text(root, wrap="word", bg="white", fg="black", font=("Arial", 16), height=25)
        self.display_area.pack(expand=True, fill="both", padx=5, pady=5)

        self.history = []
        self.history_index = -1

        self.renderer = WBYRenderer(self.display_area)

    def on_return_pressed(self, event):
        url = self.url_entry.get()
        self.load_page(url)
        self.update_history(url)

    def load_page(self, url=None, event=None):
        self.renderer.clear_widgets()

        if url is None:
            url = self.url_entry.get()

        if url.startswith("wby:"):
            parts = url[4:].split("/", 1)
            if len(parts) < 2:
                self.display_area.delete(1.0, tk.END)
                self.display_area.insert(tk.END, "Invalid URL format. Expected format: wby:<IP>/<path>")
                return
            
            ip, file_path = parts
            file_content = self.fetch_file_from_server(ip, file_path)
            if file_content:
                self.display_area.delete(1.0, tk.END)
                self.renderer.render(file_content)
            else:
                self.display_area.delete(1.0, tk.END)
                self.display_area.insert(tk.END, f"File not found on server: {file_path}")
            return

        elif url.startswith("localwby:"):
            file_path = url.replace("localwby:", "") + ".wby"
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                self.display_area.delete(1.0, tk.END)
                self.renderer.render(content)
            else:
                self.display_area.delete(1.0, tk.END)
                self.display_area.insert(tk.END, f"Local file not found: {file_path}")
            return

        else:
            self.display_area.delete(1.0, tk.END)
            self.display_area.insert(tk.END, "Invalid protocol. Use 'localwby' for local files or 'wby' for server files.")

    def update_history(self, url):
        self.history = self.history[:self.history_index + 1]
        self.history.append(url)
        self.history_index += 1

    def go_back(self):
        if self.history_index > 0:
            self.history_index -= 1
            self.url_entry.delete(0, tk.END)
            self.url_entry.insert(0, self.history[self.history_index])
            self.load_page()

    def go_forward(self):
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.url_entry.delete(0, tk.END)
            self.url_entry.insert(0, self.history[self.history_index])
            self.load_page()

    def refresh_page(self):
        if self.history_index >= 0:
            self.load_page()

    def fetch_file_from_server(self, ip, file_path):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((ip, 5000))
                request = f"GET {file_path} WBY/1.0\r\n\r\n"
                s.sendall(request.encode())
                response = s.recv(4096).decode()
                if response.startswith("WBY/1.0 100 SENT"):
                    return response.split("\r\n\r\n", 1)[1]
                self.display_area.delete(1.0, tk.END)
                self.display_area.insert(tk.END, f"Error: File not found on server or invalid response: {response}")
                return None
        except Exception as e:
            self.display_area.delete(1.0, tk.END)
            self.display_area.insert(tk.END, f"Error fetching file from server: {e}")
            return None

if __name__ == "__main__":
    root = tk.Tk()
    browser = Browser(root)
    root.mainloop()