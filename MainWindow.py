import tkinter as tk
import subprocess
import getpass
import pystray
from pystray import MenuItem as item
from PIL import Image
import threading
import os,sys
import glob


if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)
    

username = getpass.getuser()
tray_icon = None
python_path = ""


# Find available Python versions above 3.8
python_versions = glob.glob(os.path.expanduser(f"C:/Users/{username}/AppData/Local/Programs/Python/Python3[89]*"))
if python_versions:
    python_path = max(python_versions, key=lambda path: int(os.path.basename(path)[-2:]))

class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.uvicorn_process = None
        self.title("Email Sender")
        self.geometry('350x200')

        self.start_button = tk.Button(self, text="Start API", width=15, height=3, fg="green", command=self.start_api)
        self.start_button.pack()

        self.stop_button = tk.Button(self, text="Stop API", width=15, height=3, fg="red", command=self.stop_api)
        self.stop_button.pack()
        self.stop_button.config(state="disabled")

        self.status_label = tk.Label(self, text="API Status: Not Running", width=20, height=3, fg="orange")
        self.status_label.pack()

        self.protocol("WM_DELETE_WINDOW", self.on_window_close)

    def start_api(self):
        if not python_path:
            self.status_label.config(text="No suitable Python version found")
            return

        pyth_path = os.path.join(python_path, "python")
        py_api_main = ("main.py")
        cmd = [pyth_path, py_api_main]
        self.uvicorn_process = subprocess.Popen(cmd)

        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.status_label.config(text="API Status: Running")

    def stop_api(self):
        if self.uvicorn_process is not None:
            self.uvicorn_process.kill()
            self.uvicorn_process.wait()
            self.uvicorn_process = None

        subprocess.run(['taskkill', '/F', '/IM', 'uvicorn.exe'], capture_output=True, text=True)

        self.stop_button.config(state="disabled")
        self.start_button.config(state="normal")
        self.status_label.config(text="API Status: Not Running")

    def on_window_close(self):
        self.stop_api()
        self.destroy()

def create_tray_icon():
    global tray_icon
    icon_path = os.path.join(os.path.dirname(__file__), "inbox.png")
    icon_image = Image.open(icon_path)
    
    menu = (
        item('Start PI', lambda: mw.start_api()),
        item('Stop API', lambda: mw.stop_api()),
        item('Exit', lambda: quit_app())
    )
    tray_icon = pystray.Icon("API Icon", icon_image, "API", menu)
    tray_icon.run()

def quit_app():
    if tray_icon is not None:
        tray_icon.stop()
    mw.stop_api()
    mw.destroy()

def run_gui():
    global mw
    mw = MainWindow()
    mw.mainloop()

if __name__ == "__main__":
    gui_thread = threading.Thread(target=run_gui)
    gui_thread.start()
    create_tray_icon()
