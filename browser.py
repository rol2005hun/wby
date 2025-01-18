import os
import socket
import threading
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
        self.update_navigation_buttons()

    def on_return_pressed(self, event):
        url = self.url_entry.get()
        self.load_page(url)
        self.update_history(url)

    def load_page(self, url=None, event=None):
        self.renderer.clear_widgets()

        if url is None:
            url = self.url_entry.get()

        self.display_area.delete(1.0, tk.END)
        self.display_area.insert("1.0", "Loading...", "center")

        if url.startswith("wby:"):
            parts = url[4:].split("/", 1)
            if len(parts) < 2:
                self.display_error("Invalid URL format. Expected format: wby:<IP>/<path>")
                return
            
            ip, file_path = parts
            self.fetch_file_from_server(ip, file_path, self.handle_server_response)
        elif url.startswith("localwby:"):
            file_path = url.replace("localwby:", "") + ".wby"
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                self.display_area.delete(1.0, tk.END)
                self.renderer.render(content)
            else:
                self.display_error(f"Local file not found: {file_path}")
        else:
            self.display_error("Invalid protocol. Use 'localwby' for local files or 'wby' for server files.")

        self.update_navigation_buttons()

    def handle_server_response(self, result):
        if result is None:
            self.display_error("Error fetching file from server.")
        elif result.startswith("Error"):
            self.display_error(result)
        else:
            self.display_area.delete(1.0, tk.END)
            self.renderer.render(result)

    def display_error(self, message):
        self.display_area.delete(1.0, tk.END)
        self.display_area.tag_configure("center", justify="center")
        self.display_area.tag_configure("error", foreground="red", font=("Arial", 20, "bold"))
        self.display_area.insert("1.0", message, ("center", "error"))

    def update_history(self, url):
        self.history = self.history[:self.history_index + 1]
        self.history.append(url)
        self.history_index += 1
        self.update_navigation_buttons()

    def update_navigation_buttons(self):
        if self.history_index > 0:
            self.back_button["state"] = "normal"
        else:
            self.back_button["state"] = "disabled"

        if self.history_index < len(self.history) - 1:
            self.forward_button.pack(side="left", padx=5, pady=5)
        else:
            self.forward_button.pack_forget()

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

    def fetch_file_from_server(self, ip, file_path, callback):
        def worker():
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as test_socket:
                    test_socket.settimeout(3)
                    if test_socket.connect_ex((ip, 5000)) != 0:
                        callback(f"Error: Target server {ip} is not reachable.")
                        return

                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((ip, 5000))
                    request = f"GET {file_path} WBY/1.0\r\n\r\n"
                    s.sendall(request.encode())
                    response = s.recv(4096).decode()
                    if response.startswith("WBY/1.0 100 SENT"):
                        content = response.split("\r\n\r\n", 1)[1]
                        callback(content)
                    else:
                        callback(f"Error: File not found on server or invalid response: {response}")
            except Exception as e:
                callback(f"Error fetching file from server: {e}")

        threading.Thread(target=worker, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    browser = Browser(root)
    root.mainloop()