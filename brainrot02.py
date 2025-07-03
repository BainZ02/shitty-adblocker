import tkinter as tk
from tkinter import filedialog, messagebox
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

class SpotifyAdBlocker:
    def __init__(self):
        self.session = requests.Session()
        retry = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
        self.blocked_urls = []

    def block_ad_requests(self, url):
        for ad_url in self.blocked_urls:
            if ad_url in url:
                print(f"Blocking ad request: {url}")
                return None
        return self.session.get(url)

    def get(self, url):
        response = self.block_ad_requests(url)
        if response:
            return response
        else:
            return None

class Brainrot02App:
    def __init__(self, root):
        self.root = root
        self.root.title("brainrot02 Spotify Ad Blocker")
        self.ad_blocker = SpotifyAdBlocker()

        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.root, text="brainrot02 Spotify Ad Blocker")
        self.label.pack(pady=10)

        self.upload_button = tk.Button(self.root, text="Upload URL List", command=self.upload_file)
        self.upload_button.pack(pady=5)

        self.unblock_button = tk.Button(self.root, text="Unblock All", command=self.unblock_all)
        self.unblock_button.pack(pady=5)

        self.status_label = tk.Label(self.root, text="")
        self.status_label.pack(pady=10)

    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                urls = file.readlines()
                self.ad_blocker.blocked_urls = [url.strip() for url in urls]
                self.status_label.config(text="URLs loaded and ready to block!")
                messagebox.showinfo("Success", "URLs loaded and ready to block!")

    def unblock_all(self):
        self.ad_blocker.blocked_urls = []
        self.status_label.config(text="All URLs unblocked!")
        messagebox.showinfo("Success", "All URLs unblocked!")

if __name__ == "__main__":
    root = tk.Tk()
    app = Brainrot02App(root)
    root.mainloop()