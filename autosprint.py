import ctypes
import threading
import time
import tkinter as tk
from tkinter import messagebox

try:
    import pygame
except ImportError:
    pygame = None

user32 = ctypes.WinDLL("user32", use_last_error=True)
KEYEVENTF_KEYUP = 0x0002
VK_CONTROL = 0x11

def set_ctrl(down):
    user32.keybd_event(VK_CONTROL, 0, 0 if down else KEYEVENTF_KEYUP, 0)

class SprintHelper:
    def __init__(self, root):
        self.root = root
        self.root.title("MCPE 1.1.5 — AutoSprint")
        self.root.geometry("440x355")
        self.root.resizable(False, False)
        self.root.configure(bg="#17191f")

        self.running = True
        self.enabled = tk.BooleanVar(value=False)
        self.deadzone = tk.DoubleVar(value=0.65)
        self.status_text = tk.StringVar(value="Инициализация…")
        self.controller_text = tk.StringVar(value="Геймпад не обнаружен")
        self.joystick = None
        self.ctrl_down = False

        tk.Label(root, text="MCPE AUTOSPRINT", bg="#17191f", fg="#f3f4f6",
                 font=("Segoe UI", 18, "bold")).pack(pady=(17, 2))
        tk.Label(root, text="Minecraft Pocket Edition 1.1.5 • Windows 10",
                 bg="#17191f", fg="#9ca3af", font=("Segoe UI", 9)).pack()

        panel = tk.Frame(root, bg="#222631", padx=14, pady=12)
        panel.pack(fill="x", padx=18, pady=(17, 10))
        tk.Label(panel, text="СОСТОЯНИЕ ГЕЙМПАДА", bg="#222631",
                 fg="#a78bfa", font=("Segoe UI", 8, "bold")).pack(anchor="w")
        tk.Label(panel, textvariable=self.controller_text, bg="#222631",
                 fg="#e5e7eb", font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(4, 0))

        tk.Label(root, text="УПРАВЛЕНИЕ ПРОГРАММОЙ — ТОЛЬКО С ПК",
                 bg="#17191f", fg="#a78bfa",
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=22, pady=(9, 5))

        self.enable_button = tk.Button(
            root, text="ВКЛЮЧИТЬ AUTOSPRINT", command=self.toggle_enabled,
            bg="#2563eb", fg="white", activebackground="#1d4ed8",
            activeforeground="white", relief="flat", bd=0,
            font=("Segoe UI", 10, "bold"), padx=14, pady=10)
        self.enable_button.pack(fill="x", padx=22)

        self.status = tk.Label(root, textvariable=self.status_text, bg="#17191f",
                               fg="#60a5fa", font=("Segoe UI", 11, "bold"))
        self.status.pack(pady=(13, 7))

        tk.Label(root, text="Чувствительность левого стика",
                 bg="#17191f", fg="#e5e7eb",
                 font=("Segoe UI", 9)).pack()
        self.scale = tk.Scale(root, from_=0.30, to=0.95, resolution=0.05,
                              orient="horizontal", variable=self.deadzone,
                              bg="#17191f", fg="#e5e7eb", troughcolor="#343946",
                              highlightthickness=0, activebackground="#a78bfa",
                              length=320)
        self.scale.pack(pady=(0, 3))

        tk.Label(root,
                 text="Геймпад не используется для управления программой.\n"
                      "Все его кнопки остаются доступны игре. Закрой окно, чтобы остановить.",
                 bg="#17191f", fg="#9ca3af", font=("Segoe UI", 8),
                 justify="center").pack(pady=(5, 0))

        self.init_controller()
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.root.after(100, self.poll)

    def toggle_enabled(self):
        self.enabled.set(not self.enabled.get())
        if self.enabled.get():
            self.enable_button.config(text="ВЫКЛЮЧИТЬ AUTOSPRINT", bg="#b91c1c",
                                      activebackground="#991b1b")
        else:
            self.enable_button.config(text="ВКЛЮЧИТЬ AUTOSPRINT", bg="#2563eb",
                                      activebackground="#1d4ed8")
            self.release_ctrl()

    def init_controller(self):
        if pygame is None:
            self.controller_text.set("Не удалось загрузить модуль геймпада")
            self.status_text.set("ОШИБКА ЗАПУСКА")
            return
        try:
            pygame.init()
            pygame.joystick.init()
            self.find_controller()
        except Exception:
            self.controller_text.set("Ошибка инициализации геймпада")

    def find_controller(self):
        if pygame is None:
            return
        try:
            pygame.event.pump()
            count = pygame.joystick.get_count()
            if count and self.joystick is None:
                self.joystick = pygame.joystick.Joystick(0)
                self.joystick.init()
                self.controller_text.set("Подключён: " + self.joystick.get_name())
            elif not count:
                self.joystick = None
                self.controller_text.set("Геймпад не обнаружен — подключи контроллер")
        except Exception:
            self.joystick = None

    def release_ctrl(self):
        if self.ctrl_down:
            set_ctrl(False)
            self.ctrl_down = False

    def poll(self):
        if not self.running:
            return
        try:
            if pygame is not None:
                pygame.event.pump()
                if self.joystick is None or not self.joystick.get_init():
                    self.find_controller()

            forward = False
            if self.joystick is not None:
                # Read ONLY left-stick vertical axis. No gamepad buttons are polled.
                if self.joystick.get_numaxes() > 1:
                    forward = self.joystick.get_axis(1) < -self.deadzone.get()

            want_sprint = self.enabled.get() and forward
            if want_sprint and not self.ctrl_down:
                set_ctrl(True)
                self.ctrl_down = True
            elif not want_sprint:
                self.release_ctrl()

            if self.joystick is None:
                self.status_text.set("ОЖИДАНИЕ ГЕЙМПАДА")
                self.status.config(fg="#60a5fa")
            elif not self.enabled.get():
                self.status_text.set("AUTOSPRINT ВЫКЛЮЧЕН")
                self.status.config(fg="#fbbf24")
            elif self.ctrl_down:
                self.status_text.set("СПРИНТ АКТИВЕН")
                self.status.config(fg="#34d399")
            else:
                self.status_text.set("ГОТОВ • НАЖМИ СТИК ВПЕРЁД")
                self.status.config(fg="#60a5fa")
        except Exception:
            self.release_ctrl()
            self.status_text.set("ОШИБКА ЧТЕНИЯ ГЕЙМПАДА")
        self.root.after(12, self.poll)

    def close(self):
        self.running = False
        self.release_ctrl()
        try:
            if pygame is not None:
                pygame.quit()
        except Exception:
            pass
        self.root.destroy()

if __name__ == "__main__":
    if pygame is None:
        raise SystemExit("pygame is required")
    root = tk.Tk()
    app = SprintHelper(root)
    root.mainloop()
