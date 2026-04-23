import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime
import os

# --- Имя файла для хранения данных ---
DATA_FILE = "trainings.json"

# --- Функции работы с JSON ---
def load_trainings():
    """Загружает список тренировок из JSON-файла"""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_trainings(trainings):
    """Сохраняет список тренировок в JSON-файл"""
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(trainings, file, ensure_ascii=False, indent=4)

# --- Функции обновления интерфейса ---
def update_table(trainings_list=None):
    """Обновляет таблицу (дерево) с тренировками"""
    # Очищаем таблицу
    for row in tree.get_children():
        tree.delete(row)
    
    # Если список не передан, берём все данные
    if trainings_list is None:
        trainings_list = trainings
    
    # Заполняем таблицу
    for t in trainings_list:
        tree.insert("", tk.END, values=(t["date"], t["type"], t["duration"]))

def apply_filter():
    """Применяет фильтры и обновляет таблицу"""
    filter_type = type_filter.get()
    filter_date = date_filter.get()
    
    filtered = []
    for t in trainings:
        # Фильтр по типу
        if filter_type and filter_type != "Все" and t["type"] != filter_type:
            continue
        # Фильтр по дате
        if filter_date and t["date"] != filter_date:
            continue
        filtered.append(t)
    
    update_table(filtered)

def reset_filter():
    """Сбрасывает фильтры и показывает все тренировки"""
    type_filter.set("Все")
    date_filter.set("")
    update_table()

# --- Функция добавления тренировки ---
def add_training():
    date = entry_date.get().strip()
    training_type = entry_type.get().strip()
    duration = entry_duration.get().strip()
    
    # Проверка корректности ввода
    if not date or not training_type or not duration:
        messagebox.showwarning("Предупреждение", "Заполните все поля!")
        return
    
    # Проверка формата даты (DD.MM.YYYY)
    try:
        datetime.strptime(date, "%d.%m.%Y")
    except ValueError:
        messagebox.showerror("Ошибка", "Неверный формат даты!\nИспользуйте ДД.ММ.ГГГГ (например, 15.05.2026)")
        return
    
    # Проверка длительности (положительное число)
    try:
        duration_value = float(duration)
        if duration_value <= 0:
            messagebox.showerror("Ошибка", "Длительность должна быть положительным числом!")
            return
    except ValueError:
        messagebox.showerror("Ошибка", "Длительность должна быть числом (например, 45.5)")
        return
    
    # Добавляем тренировку
    new_training = {
        "date": date,
        "type": training_type,
        "duration": duration_value
    }
    trainings.append(new_training)
    save_trainings(trainings)
    
    # Очищаем поля ввода
    entry_date.delete(0, tk.END)
    entry_type.delete(0, tk.END)
    entry_duration.delete(0, tk.END)
    
    # Обновляем таблицу и фильтры
    update_table()
    update_type_filter_options()
    update_date_filter_options()
    
    messagebox.showinfo("Успех", "Тренировка добавлена!")

def update_type_filter_options():
    """Обновляет выпадающий список типов тренировок для фильтра"""
    types = sorted(set(t["type"] for t in trainings))
    type_menu["values"] = ["Все"] + types
    if type_filter.get() not in types and type_filter.get() != "Все":
        type_filter.set("Все")

def update_date_filter_options():
    """Обновляет выпадающий список дат для фильтра"""
    dates = sorted(set(t["date"] for t in trainings))
    date_menu["values"] = dates
    if date_filter.get() and date_filter.get() not in dates:
        date_filter.set("")

# --- Создание главного окна ---
window = tk.Tk()
window.title("Training Planner")
window.geometry("800x500")
window.resizable(False, False)

# Загружаем данные
trainings = load_trainings()

# --- Фрейм для ввода данных ---
input_frame = tk.LabelFrame(window, text="Добавление тренировки", font=("Arial", 10, "bold"))
input_frame.pack(pady=10, padx=10, fill="x")

# Дата
tk.Label(input_frame, text="Дата (ДД.ММ.ГГГГ):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_date = tk.Entry(input_frame, width=15)
entry_date.grid(row=0, column=1, padx=5, pady=5)

# Тип тренировки
tk.Label(input_frame, text="Тип тренировки:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
entry_type = tk.Entry(input_frame, width=20)
entry_type.grid(row=0, column=3, padx=5, pady=5)

# Длительность
tk.Label(input_frame, text="Длительность (мин):").grid(row=0, column=4, padx=5, pady=5, sticky="e")
entry_duration = tk.Entry(input_frame, width=10)
entry_duration.grid(row=0, column=5, padx=5, pady=5)

# Кнопка добавления
btn_add = tk.Button(input_frame, text="➕ Добавить тренировку", command=add_training, bg="#4CAF50", fg="white")
btn_add.grid(row=0, column=6, padx=15, pady=5)

# --- Фрейм для фильтрации ---
filter_frame = tk.LabelFrame(window, text="Фильтрация", font=("Arial", 10, "bold"))
filter_frame.pack(pady=5, padx=10, fill="x")

# Фильтр по типу
tk.Label(filter_frame, text="Тип тренировки:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
type_filter = tk.StringVar(value="Все")
types = sorted(set(t["type"] for t in trainings))
type_menu = ttk.Combobox(filter_frame, textvariable=type_filter, values=["Все"] + types, width=20, state="readonly")
type_menu.grid(row=0, column=1, padx=5, pady=5)

# Фильтр по дате
tk.Label(filter_frame, text="Дата (ДД.ММ.ГГГГ):").grid(row=0, column=2, padx=5, pady=5, sticky="e")
date_filter = tk.StringVar(value="")
dates = sorted(set(t["date"] for t in trainings))
date_menu = ttk.Combobox(filter_frame, textvariable=date_filter, values=dates, width=15)
date_menu.grid(row=0, column=3, padx=5, pady=5)

# Кнопки фильтрации
btn_apply = tk.Button(filter_frame, text="🔍 Применить фильтр", command=apply_filter, bg="#2196F3", fg="white")
btn_apply.grid(row=0, column=4, padx=5, pady=5)

btn_reset = tk.Button(filter_frame, text="🗑️ Сбросить фильтр", command=reset_filter, bg="#FF9800", fg="white")
btn_reset.grid(row=0, column=5, padx=5, pady=5)

# --- Таблица для отображения тренировок ---
tree_frame = tk.Frame(window)
tree_frame.pack(pady=10, padx=10, fill="both", expand=True)

# Создаём скроллбар
scrollbar = tk.Scrollbar(tree_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Создаём таблицу (Treeview)
columns = ("date", "type", "duration")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings", yscrollcommand=scrollbar.set)
scrollbar.config(command=tree.yview)

tree.heading("date", text="Дата")
tree.heading("type", text="Тип тренировки")
tree.heading("duration", text="Длительность (мин)")

tree.column("date", width=120, anchor="center")
tree.column("type", width=250, anchor="center")
tree.column("duration", width=150, anchor="center")

tree.pack(fill="both", expand=True)

# Заполняем таблицу
update_table()

# --- Информационная строка ---
info_label = tk.Label(window, text="Данные автоматически сохраняются в trainings.json", font=("Arial", 8), fg="gray")
info_label.pack(side=tk.BOTTOM, pady=5)

# --- Запуск программы ---
window.mainloop()
