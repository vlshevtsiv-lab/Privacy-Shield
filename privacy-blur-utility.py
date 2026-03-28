import threading
import time

import customtkinter as ctk
import keyboard
import pyautogui
import pygetwindow as gw
import pystray
from PIL import Image, ImageDraw, ImageFilter, ImageTk
from pystray import MenuItem as item

class PrivacyShieldApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.title("Privacy Shield")
        self.geometry("500x300")

        self.blur = ctk.IntVar(value=20)
        self.hotkey = ctk.StringVar(value="ctrl+shift+x")
        self.status = ctk.StringVar(value="Inactive")
        self.overlay = None
        self.overlay_img = None
        self.service_active = False
        self.stop_event = threading.Event()
        self.listener_thread = None
        self.hotkey_id = None
        self.tray = None

        self._build_ui()
        self.protocol("WM_DELETE_WINDOW", self.hide_to_tray)

    def _build_ui(self):
        box = ctk.CTkFrame(self, corner_radius=14)
        box.pack(fill="both", expand=True, padx=14, pady=14)

        ctk.CTkLabel(box, text="Privacy Shield", font=ctk.CTkFont(size=26, weight="bold")).pack(anchor="w", padx=16, pady=(14, 6))

        self.status_lbl = ctk.CTkLabel(box, textvariable=self.status, text_color="#ff6b6b")
        self.status_lbl.pack(anchor="w", padx=16,)

        ctk.CTkLabel(box, text="Blur Intensity 1-50").pack(anchor="w", padx=16, pady=(12, 0))
        ctk.CTkSlider(box, from_=1, to=50, number_of_steps=49, variable=self.blur).pack(fill="x", padx=16, pady=6)

        ctk.CTkLabel(box, text="Global Hotkey").pack(anchor="w", padx=16, pady=(8, 0))
        ctk.CTkEntry(box, textvariable=self.hotkey).pack(fill="x", padx=16, pady=6)

        row = ctk.CTkFrame(box, fg_color="transparent")
        row.pack(fill="x", padx=16, pady=14)

        self.start_btn = ctk.CTkButton(row, text="Start Service", command=self.toggle_service)
        self.start_btn.pack(side="left", padx=(0, 8))

        ctk.CTkButton(row, text="Hide to Tray", command=self.hide_to_tray).pack(side="left")

        ctk.CTkButton(row, text="Exit", fg_color="#ff6b6b", hover_color="#ff4c4c", command=self.exit_app).pack(side="right")

    def set_status(self, active):
        self.status.set("Active" if active else "Inactive")
        self.status_lbl.configure(text_color="#4ade80" if active else "#ff6b6b")
        self.start_btn.configure(text="Stop Service" if active else "Start Service")

    def toggle_service(self):
        if self.service_active:
            self.stop_event.set()
            if self.listener_thread and self.listener_thread.is_alive():
                self.listener_thread.join(timeout=1)
            self.hide_overlay()
            self.service_active = False
            self.set_status(False)
            return
        
        try:
            keyboard.parse_hotkey(self.hotkey.get().strip().lower())
        except Exception:
            self.status.set("invalid Hotkey")
            self.status_lbl.configure(text_color="#ff6b6b")
            return
        
        self.stop_event.clear()
        self.listener_thread = threading.Thread(target=self.listen_hotkey, daemon=True)
        self.listener_thread.start()
        self.service_active = True
        self.set_status(True)

    def listen_hotkey(self):
        self.hotkey_id = keyboard.add_hotkey(self.hotkey.get().strip().lower(), lambda: self.after(0, self.toggle_overlay))

        while not self.stop_event.is_set():
            time.sleep(0.1)
        
        if self.hotkey_id is not None:
            keyboard.remove_hotkey(self.hotkey_id)
            self.hotkey_id = None

    def toggle_overlay(self):
        if self.overlay and self.overlay.winfo_exists():
            self.hide_overlay()
            return
        
        win = gw.getActiveWindow()
        if not win or win.width <= 0 or win.height <= 0:
            return
        
        x, y, w, h = win.left, win.top, win.width, win.height

        img = pyautogui.screenshot(region=(x, y, w, h)).filter(ImageFilter.GaussianBlur(radius=int(self.blur.get())))

        self.overlay_img = ImageTk.PhotoImage(img)
        self.overlay = ctk.CTkToplevel(self)
        self.overlay.overrideredirect(True)
        self.overlay.attributes("-topmost", True)
        self.overlay.geometry(f"{w}x{h}+{x}+{y}")

        lbl = ctk.CTkLabel(self.overlay, text="", image=self.overlay_img)
        lbl.pack(fill="both", expand=True)

        self.overlay.bind("<Button-1>", lambda _e: self.hide_overlay())
        lbl.bind("<Button-1>", lambda _e: self.hide_overlay())
                 
    def hide_overlay(self):
        if self.overlay and self.overlay.winfo_exists():
            self.overlay.destroy()
        self.overlay = None

    def hide_to_tray(self):
        self.withdraw()
        if self.tray:
            return

        icon = Image.new("RGBA", (64, 64), (20, 22, 30, 255))
        d = ImageDraw.Draw(icon)
        d.rounded_rectangle((10, 10, 54, 54), radius=10, outline=(102, 226, 138), width=3)
        d.polygon([(32, 16), (46, 24), (42, 40), (32, 48), (22, 40), (18, 24)], fill=(102, 226, 138))

        menu = (
            item("Show", lambda _i, _m: self.after(0, self.show_from_tray)),
            item("Toggle Service", lambda _i, _m: self.after(0, self.toggle_service)),
            item("Exit", lambda _i, _m: self.after(0, self.exit_app))
        )

        self.tray = pystray.Icon("Privacy Shield", icon, "Privacy Shield", menu)
        threading.Thread(target=self.tray.run, daemon=True).start()

    def show_from_tray(self):
        self.deiconify()
        self.lift()
        self.focus_force()

    def exit_app(self):
        self.stop_event.set()
        self.hide_overlay()

        if self.hotkey_id is not None:
            keyboard.remove_hotkey(self.hotkey_id)
            
        if self.tray:
            self.tray.stop()
            self.tray = None

        self.destroy()


if __name__ == "__main__":
    PrivacyShieldApp().mainloop()