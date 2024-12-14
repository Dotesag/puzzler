import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from create_photo import create_photo
from tkinter import messagebox

import sqlite3
"""

    ЭТО ВСПОМОГАТЕЛЬНЫЙ ФАЙЛ. ОСНОВНОЙ ВСТАВЛЕН В main ПОТОМУ ЧТО ГРЕБАНЫЙ СБОРЩИК МУСОРА УБИВАЕТ КАРТИНКУ


    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!





"""

def get_wood_types():
    data = []
    with sqlite3.connect('db/database.db') as db:
        cursor = db.cursor()
        query = '''
                SELECT name, short_description FROM wood
            '''
        cursor.execute(query)
        data = cursor.fetchall()
    return data


def save_puzzle(n, d, p):
    with sqlite3.connect('db/database.db') as db:
        cursor = db.cursor()

        query = '''
                    INSERT INTO puzzles (name, details, plane) VALUES (?, ?, ?)
                '''
        cursor.execute(query, (n, d, p))
        db.commit()

def get_puzzle_list():
    data = []
    with sqlite3.connect('db/database.db') as db:
        cursor = db.cursor()
        query = '''
            SELECT name FROM puzzles
        '''
        cursor.execute(query)
        data = cursor.fetchall()
    list = [i[0] for i in data]
    return list

def create_puzzle():
    def validate_positive_integer(value):
        """Проверяет, является ли введенное значение положительным целым числом."""
        if value.isdigit() and int(value) > 0:
            update_puzzle_image(int(value))
            return True
        elif value == "":
            return True
        return False

    def update_puzzle_image(pieces):
        """Обновляет изображение пазла на основе количества деталей в ряду."""
        create_photo("asset/template.png", pieces, "output.png")
        img = Image.open("output.png")
        img_resized = img.resize((300, 300), Image.Resampling.LANCZOS)
        tk_img = ImageTk.PhotoImage(img_resized)
        img_label.config(image=tk_img)
        img_label.image = tk_img

    def save_to_db():
        """Сохраняет данные в базу данных."""
        name = entry_name.get().strip()
        pieces = entry_pieces.get().strip()
        sheet = combobox_sheet.get().strip()

        if not name:
            messagebox.showerror("Ошибка", "Введите название пазла.")
            return

        if not pieces or not pieces.isdigit() or int(pieces) <= 0:
            messagebox.showerror("Ошибка", "Введите корректное количество деталей в ряду.")
            return

        if not sheet:
            tk.messagebox.showerror("Ошибка", "Выберите фанерный лист.")
            return

        if name in get_puzzle_list():
            tk.messagebox.showerror("Ошибка", "Такое название пазла уже есть")
            return

        # Сохраняем данные в базу данных
        save_puzzle(name, f"{pieces}x{pieces}", sheet)
        tk.messagebox.showinfo("Успех", "Пазл успешно сохранен в базу данных!")

    # Создаем главное окно
    window = tk.Toplevel()
    window.title("Создать новый пазл")
    window.geometry('800x600')
    window.resizable(False, False)
    window.configure(bg="#E0F2E1")

    # Заголовок
    title_label = tk.Label(window, text="Создать новый пазл", font=("Helvetica", 24, "bold"), bg="#E0F2E1", fg="black")
    title_label.pack(pady=10)

    # Блок "Изменить характеристики"
    characteristics_frame = tk.Frame(window, bg="#F6FFF6", bd=0, relief="solid", highlightbackground="#57B748",
                                     highlightthickness=2)
    characteristics_frame.place(x=50, y=150, width=350, height=300)

    characteristics_title = tk.Label(characteristics_frame, text="Изменить характеристики",
                                     font=("Helvetica", 16, "bold"), bg="#F6FFF6", fg="black")
    characteristics_title.pack(pady=10)

    # Форма ввода для названия пазла
    label_name = tk.Label(characteristics_frame, text="Название пазла:", font=("Helvetica", 12), bg="#F6FFF6")
    label_name.pack(anchor="w", padx=10, pady=5)
    entry_name = tk.Entry(characteristics_frame, font=("Helvetica", 12), width=30)
    entry_name.pack(padx=10, pady=5)

    # Форма ввода для количества деталей в ряду
    label_pieces = tk.Label(characteristics_frame, text="Деталей в ряду:", font=("Helvetica", 12), bg="#F6FFF6")
    label_pieces.pack(anchor="w", padx=10, pady=5)

    vcmd = (window.register(validate_positive_integer), "%P")
    entry_pieces = tk.Entry(characteristics_frame, font=("Helvetica", 12), width=30, validate="key",
                            validatecommand=vcmd)
    entry_pieces.pack(padx=10, pady=5)

    # Форма выбора фанерного листа из списка
    label_sheet = tk.Label(characteristics_frame, text="Фанерный лист:", font=("Helvetica", 12), bg="#F6FFF6")
    label_sheet.pack(anchor="w", padx=10, pady=5)

    sheet_options = get_wood_types()
    combobox_sheet = ttk.Combobox(characteristics_frame, values=sheet_options, font=("Helvetica", 12), state="readonly")
    combobox_sheet.pack(padx=10, pady=5)

    # Загрузка и отображение изображения
    placeholder_frame = tk.Frame(window, bg="#F0F0F0", bd=0, relief="solid", highlightbackground="#57B748",
                                 highlightthickness=2)
    placeholder_frame.place(x=450, y=150, width=300, height=300)

    # Инициализация изображения пазла
    create_photo("asset/template.png", 4, "output.png")  # По умолчанию 4 детали
    img = Image.open("output.png")
    img = img.resize((300, 300), Image.Resampling.LANCZOS)
    tk_img = ImageTk.PhotoImage(img)

    img_label = tk.Label(placeholder_frame, image=tk_img, bg="#F0F0F0")
    img_label.image = tk_img
    img_label.place(relx=0.5, rely=0.5, anchor="center")

    # Кнопка для создания пазла
    btn_create = tk.Button(window, text="Создать пазл", font=("Helvetica", 14), bg="#4CAF50", fg="white", width=15,
                           command=save_to_db)
    btn_create.place(x=320, y=500)

    window.mainloop()


# create_puzzle()