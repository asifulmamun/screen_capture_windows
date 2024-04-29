import tkinter as tk
from tkinter import ttk
import time
import threading
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon

class TimerApp:
    def __init__(self, master):
        self.master = master
        master.title("Timer App")

        self.label = ttk.Label(master, text="Timer: 00:00:00")
        self.label.pack()

        self.start_button = ttk.Button(master, text="Start", command=self.start_timer)
        self.start_button.pack()

        self.stop_button = ttk.Button(master, text="Stop", command=self.stop_timer)
        self.stop_button.pack()

        self.is_running = False
        self.elapsed_time = 0
        self.screenshot_thread = None
        self.timer_thread = None

        self.create_system_tray()

    def create_system_tray(self):
        self.app = QApplication([])
        self.tray_icon = QSystemTrayIcon(QIcon("icon.ico"), self.app)
        self.tray_icon.setToolTip("Timer App")

        self.menu = QMenu()
        self.restore_action = QAction("Restore", self.app)
        self.quit_action = QAction("Quit", self.app)
        self.restore_action.triggered.connect(self.restore)
        self.quit_action.triggered.connect(self.quit)
        self.menu.addAction(self.restore_action)
        self.menu.addAction(self.quit_action)
        self.tray_icon.setContextMenu(self.menu)

    def run(self):
        self.tray_icon.show()
        self.app.exec_()

    def start_timer(self):
        if not self.is_running:
            self.is_running = True
            self.start_button.config(state="disabled")
            self.stop_button.config(state="normal")
            self.elapsed_time = 0
            self.update_timer()

            # Start a thread for capturing screenshots
            self.screenshot_thread = threading.Thread(target=self.capture_screenshots)
            self.screenshot_thread.start()

            # Start a thread for the timer
            self.timer_thread = threading.Thread(target=self.run_timer)
            self.timer_thread.start()

    def stop_timer(self):
        if self.is_running:
            self.is_running = False
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")
            if self.timer_thread:
                self.timer_thread.join()  # Wait for timer thread to finish
            if self.screenshot_thread:
                self.screenshot_thread.join()  # Wait for screenshot thread to finish

    def run_timer(self):
        while self.is_running:
            self.elapsed_time += 1
            time.sleep(1)
            self.update_timer()

    def update_timer(self):
        hours = self.elapsed_time // 3600
        minutes = (self.elapsed_time % 3600) // 60
        seconds = self.elapsed_time % 60
        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        self.label.config(text=f"Timer: {time_str}")

    def capture_screenshots(self):
        while self.is_running:
            # Capture screenshot
            # Implement screenshot capturing logic here
            print("Capturing screenshot...")
            time.sleep(5)  # Placeholder for demonstration

    def restore(self):
        self.master.deiconify()

    def quit(self):
        self.tray_icon.hide()
        self.app.quit()

def main():
    root = tk.Tk()
    app = TimerApp(root)
    root.protocol("WM_DELETE_WINDOW", app.quit)  # Handle window close button
    root.withdraw()  # Hide the main window initially
    app.run()

if __name__ == "__main__":
    main()
