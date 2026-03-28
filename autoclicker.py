import pyautogui
import keyboard
import threading
import tkinter as tk
from tkinter import messagebox
import random
import time

# Настройки
pyautogui.MINIMUM_DURATION = 0
pyautogui.MINIMUM_SLEEP = 0
pyautogui.PAUSE = 0
DELAY = 0.001
CLICK_COUNT = 100

clicking = False
thread = None

def click_loop():
    global clicking
    while clicking:
        pyautogui.click()
        time.sleep(random.uniform(DELAY, DELAY * 1.5))

def toggle_clicking():
    global clicking, thread
    clicking = not clicking
    if clicking:
        thread = threading.Thread(target=click_loop, daemon=True)
        thread.start()
        status_label.config(text="Статус: Кликает (F6 для выкл)")
    else:
        status_label.config(text="Статус: Остановлен (F6 для вкл)")

def start_clicking():
    if not clicking:
        toggle_clicking()

def stop_clicking():
    global clicking
    if clicking:
        toggle_clicking()

def check_hotkey():
    while True:
        if keyboard.is_pressed('f6'):
            toggle_clicking()
            time.sleep(0.2)
        time.sleep(0.01)

root = tk.Tk()
root.title("Автокликер")
root.geometry("300x200")
root.configure(bg='black')

status_label = tk.Label(root, text="Статус: Остановлен (F6 для вкл)", bg='black', fg='white')
status_label.pack(pady=10)

start_btn = tk.Button(root, text="Старт", command=start_clicking, bg='green', fg='white')
start_btn.pack(pady=5)

stop_btn = tk.Button(root, text="Стоп", command=stop_clicking, bg='red', fg='white')
stop_btn.pack(pady=5)

exit_btn = tk.Button(root, text="Выход", command=root.quit, bg='gray', fg='white')
exit_btn.pack(pady=5)

hotkey_thread = threading.Thread(target=check_hotkey, daemon=True)
hotkey_thread.start()

try:
    root.mainloop()
except Exception as e:
    messagebox.showerror("Ошибка", f"ошибка: {str(e)}")