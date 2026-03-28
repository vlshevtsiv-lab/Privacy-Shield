# Privacy-Shield

📷 Preview
<img width="504" height="333" alt="image" src="https://github.com/user-attachments/assets/494d7ed8-875f-4fbd-a28f-0e42d44c999d" />


🚀 Features
🔥 Instant Blur Overlay
Blur your currently active window with one key press.
🎛️ Adjustable Blur Intensity
Choose how strong the blur effect is (1–50).
⌨️ Custom Global Hotkey
Set your own shortcut (default: Ctrl + Shift + X).
🖥️ Works on Any Window
Automatically detects and blurs the active window.
🧊 Clean UI (CustomTkinter)
Modern dark-themed interface.
📌 System Tray Support
Run in the background and control from tray.

🧠 How It Works
Detects the currently active window
Takes a screenshot of that window
Applies a Gaussian blur effect
Displays it as an always-on-top overlay
Click or press the hotkey again to remove it

🛠️ Requirements

Install dependencies:

pip install customtkinter keyboard pyautogui pygetwindow pystray pillow

▶️ Usage

Run the app:

python main.py
Steps:
Set your blur intensity
Choose a hotkey (optional)
Click Start Service
Press your hotkey to toggle blur

⚠️ Notes
May require administrator privileges for global hotkeys
Screenshot + blur may cause slight delay on high-resolution screens
Works best on single-monitor setups

💡 Future Improvements
Faster screenshot system (e.g., mss)
Real-time blur instead of static image
Multi-monitor support
Smooth fade animations
Selective area blur

📄 License

Free to use and modify.
