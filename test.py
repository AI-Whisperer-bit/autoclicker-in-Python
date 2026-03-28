import tkinter as tk
from tkinter import messagebox
import threading
import time

class ClickCounterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Тест скорости кликов")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        
        self.click_count = 0
        self.is_testing = False
        self.selected_time = tk.IntVar(value=1)
        
        self.setup_ui()
        
    def setup_ui(self):
        title = tk.Label(self.root, text="Тест скорости кликов (CPS)", 
                         font=("Arial", 16, "bold"))
        title.pack(pady=10)
        
        time_frame = tk.LabelFrame(self.root, text="Выберите время теста", padx=10, pady=10)
        time_frame.pack(pady=10, padx=20, fill="x")
        
        buttons_frame = tk.Frame(time_frame)
        buttons_frame.pack()
        
        for i in range(1, 6):
            btn = tk.Button(buttons_frame, text=f"{i} сек", width=6,
                           command=lambda x=i: self.selected_time.set(x))
            btn.grid(row=0, column=i-1, padx=2, pady=2)
        
        buttons_frame2 = tk.Frame(time_frame)
        buttons_frame2.pack(pady=5)
        
        for i in range(6, 11):
            btn = tk.Button(buttons_frame2, text=f"{i} сек", width=6,
                           command=lambda x=i: self.selected_time.set(x))
            btn.grid(row=0, column=i-6, padx=2, pady=2)
        
        self.time_label = tk.Label(time_frame, text="Выбрано: 1 секунда", 
                                   font=("Arial", 10), fg="blue")
        self.time_label.pack(pady=5)
        
        self.main_btn = tk.Button(self.root, text="СТАРТ", 
                                   font=("Arial", 20, "bold"),
                                   bg="green", fg="white",
                                   width=15, height=3,
                                   command=self.on_button_click)
        self.main_btn.pack(pady=30)
        
        result_frame = tk.LabelFrame(self.root, text="Результаты", padx=10, pady=10)
        result_frame.pack(pady=10, padx=20, fill="x")
        
        self.clicks_label = tk.Label(result_frame, text="Кликов: 0", 
                                     font=("Arial", 14))
        self.clicks_label.pack()
        
        self.cps_label = tk.Label(result_frame, text="CPS: 0.00", 
                                  font=("Arial", 14, "bold"))
        self.cps_label.pack()
        
        self.timer_label = tk.Label(result_frame, text="", 
                                    font=("Arial", 12), fg="red")
        self.timer_label.pack(pady=5)
        
        instruction = tk.Label(self.root, 
                               text="Инструкция:\n1. Выберите время теста\n2. Нажмите СТАРТ\n3. БЫСТРО ТАПАЙТЕ по этой же кнопке\n4. После окончания увидите результат",
                               font=("Arial", 9), fg="gray", justify="left")
        instruction.pack(pady=10)
        
        self.update_time_display()
    
    def update_time_display(self):
        """Обновляет текст с выбранным временем"""
        if not self.is_testing:
            self.time_label.config(text=f"Выбрано: {self.selected_time.get()} секунд")
        self.root.after(100, self.update_time_display)
    
    def on_button_click(self):
        """Обработчик клика по главной кнопке"""
        if not self.is_testing:
            self.start_test()
        else:
            self.click_count += 1
            self.clicks_label.config(text=f"Кликов: {self.click_count}")
            
            elapsed = self.selected_time.get() - self.remaining_time
            if elapsed > 0:
                current_cps = self.click_count / elapsed
                self.cps_label.config(text=f"CPS: {current_cps:.2f}")
    
    def start_test(self):
        self.click_count = 0
        self.remaining_time = self.selected_time.get()
        
        self.clicks_label.config(text="Кликов: 0")
        self.cps_label.config(text="CPS: 0.00")
        
        self.is_testing = True
        
        self.main_btn.config(text="ТАПАЙ!", bg="orange")
        
        self.update_timer()
    
    def update_timer(self):
        if not self.is_testing:
            return
        
        if self.remaining_time > 0:
            self.timer_label.config(text=f"Осталось: {self.remaining_time} сек")
            self.remaining_time -= 1
            self.root.after(1000, self.update_timer)
        else:
            self.end_test()
    
    def end_test(self):
        self.is_testing = False
        duration = self.selected_time.get()
        cps = self.click_count / duration
        
        self.main_btn.config(text="СТАРТ", bg="green")
        self.timer_label.config(text="Тест завершён!")
        
        self.cps_label.config(text=f"CPS: {cps:.2f}")
        
        messagebox.showinfo("Результат", 
                           f"Тест завершён!\n\n"
                           f"Время: {duration} сек\n"
                           f"Кликов: {self.click_count}\n"
                           f"Скорость: {cps:.2f} кликов/сек")

if __name__ == "__main__":
    root = tk.Tk()
    app = ClickCounterApp(root)
    root.mainloop()