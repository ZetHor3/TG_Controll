import os
import subprocess
import customtkinter as ctk
from tkinter import filedialog
import time
import autoit
from screeninfo import get_monitors

# Словарь для хранения PIDs запущенных процессов
pids = {}

# Параметры окна Telegram
window_width = 380  # Ширина окна Telegram
window_height = 500  # Высота окна Telegram
margin_x = 1  # Горизонтальный отступ между окнами
margin_y = 1  # Вертикальный отступ между окнами

# Путь к папке с Telegram по умолчанию
base_path = r"C:\Users\geni1\AppData\Roaming\telegrams"

def get_screen_size():
    monitor = get_monitors()[0]
    return monitor.width, monitor.height

def launch_telegram(start_folder, end_folder):
    screen_width, screen_height = get_screen_size()
    max_windows_in_row = 6  # Максимальное количество окон в ряд
    max_windows_in_column = 2  # Максимальное количество строк
    current_column = 0
    current_row = 0

    for i in range(start_folder, end_folder + 1):
        telegram_path = os.path.join(base_path, f"Telegram_{i}", "Telegram.exe")
        if os.path.exists(telegram_path):
            try:
                process = subprocess.Popen(telegram_path)
                pids[f"Telegram_{i}"] = process.pid
                
                time.sleep(2)
                
                window_title = "Telegram"
                autoit.win_wait(window_title, 2)
                autoit.win_set_title(window_title, f"Telegram_{i}")

                posX = current_column * (window_width + margin_x)
                posY = current_row * (window_height + margin_y)
                
                autoit.win_move(f"Telegram_{i}", posX, posY)
                
                current_column += 1
                if current_column >= max_windows_in_row:
                    current_column = 0
                    current_row += 1
                if current_row >= max_windows_in_column:  # Если две строки заполнены
                    current_row = 0  # Сбросим на начало
                    current_column = 0  # Сбросим на начало
                if current_row >= max_windows_in_column and current_column >= max_windows_in_row:
                    break  # Прекращаем запуск, если оба ряда заполнены

            except Exception as e:
                pass  # Убираем сообщения об ошибках
        else:
            pass  # Убираем предупреждения, если файл не найден




def close_telegram():
    for name, pid in pids.items():
        try:
            os.kill(pid, 9)
        except Exception as e:
            pass  # Убираем сообщения об ошибках при закрытии
    pids.clear()

def run():
    try:
        start = int(start_entry.get())
        end = int(end_entry.get())
        launch_telegram(start, end)
    except ValueError:
        pass  # Убираем сообщения об ошибках ввода

# Функция для выбора новой папки
def choose_directory():
    global base_path
    new_path = filedialog.askdirectory(initialdir=base_path, title="Выберите папку Telegram")
    if new_path:
        base_path = new_path
        path_label.configure(text=base_path)

# Создание интерфейса с CustomTkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Запуск Telegram")
root.geometry("300x180")
root.iconbitmap("LogoBase.ico")

# Ввод для начала и конца в одной строке
input_frame = ctk.CTkFrame(root)
input_frame.pack(pady=(20, 10))

ctk.CTkLabel(input_frame, text="С:").grid(row=0, column=0, padx=5)
start_entry = ctk.CTkEntry(input_frame, width=50)
start_entry.grid(row=0, column=1, padx=5)

ctk.CTkLabel(input_frame, text="По:").grid(row=0, column=2, padx=5)
end_entry = ctk.CTkEntry(input_frame, width=50)
end_entry.grid(row=0, column=3, padx=5)

# Кнопка "Запустить Telegram"
launch_button = ctk.CTkButton(root, text="Запустить Telegram", command=run)
launch_button.pack(pady=(10, 5))

# Кнопка "Закрыть Telegram"
close_button = ctk.CTkButton(root, text="Закрыть Telegram", command=close_telegram, fg_color="red")
close_button.pack(pady=(5, 10))

# Кнопка для настроек
def open_settings():
    settings_window = ctk.CTkToplevel(root)
    settings_window.title("Настройки")
    settings_window.geometry("400x150")

    # Путь к папке Telegram
    ctk.CTkLabel(settings_window, text="Путь к папке Telegram:").pack(pady=(10, 5))
    
    global path_label
    path_label = ctk.CTkLabel(settings_window, text=base_path)
    path_label.pack(pady=(5, 10))
    
    # Кнопка "Обзор" для выбора пути
    browse_button = ctk.CTkButton(settings_window, text="Обзор", command=choose_directory)
    browse_button.pack(pady=(5, 10))

# Кнопка для открытия настроек
settings_button = ctk.CTkButton(root, text="⚙️", width=20, command=open_settings)
settings_button.place(x=270, y=10)

root.mainloop()
