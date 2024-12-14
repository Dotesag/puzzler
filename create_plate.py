import tkinter as tk
import sqlite3
from tkinter import ttk
from tkinter import messagebox


# Пример данных из базы данных (можно заменить на реальный запрос к БД)
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


def save_plate(n, t, w):
    with sqlite3.connect('db/database.db') as db:
        cursor = db.cursor()

        query = '''

                    INSERT INTO planes (name, wood_type, width) VALUES (?, ?, ?)    

                '''
        cursor.execute(query, (n, w, t))


def get_plane_list():
    data = []
    with sqlite3.connect('db/database.db') as db:
        cursor = db.cursor()
        query = '''
            SELECT name FROM planes
        '''
        cursor.execute(query)
        data = cursor.fetchall()
    list = [i[0] for i in data]
    return list


# Функция для создания закругленных прямоугольников
def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius, **kwargs):
    points = [
        x1 + radius, y1,
        x1 + radius, y1,
        x2 - radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y1 + radius,
        x2, y1 + radius,
        x2, y2 - radius,
        x2, y2 - radius,
        x2, y2,
        x2 - radius, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1 + radius,
        x1, y1,
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)


# Функция для создания кнопки
def create_button(canvas, text, radius, command=None):
    button_width = 170
    button_height = 40

    # Определение центра Canvas
    canvas_width = int(canvas['width'])
    canvas_height = int(canvas['height'])

    x1 = (canvas_width - button_width) / 2
    y1 = (canvas_height - button_height) / 2
    x2 = x1 + button_width
    y2 = y1 + button_height

    btn = create_rounded_rectangle(canvas, x1, y1, x2, y2, radius, fill="#4CAF50", outline="#388E3C", width=2)
    text_id = canvas.create_text(
        (x1 + x2) / 2,
        (y1 + y2) / 2,
        text=text,
        font=("Helvetica", 14, "bold"),
        fill="white"
    )

    # Bind click events to the canvas
    def on_click(event):
        if command:
            command()

    canvas.tag_bind(btn, "<Button-1>", on_click)
    canvas.tag_bind(text_id, "<Button-1>", on_click)


# Функция для окна создания листа
def create_plate():
    window = tk.Tk()
    window.title("Puzzler - создать лист фанеры")
    window.geometry('350x420')
    window.minsize(350, 420)
    window.resizable(False, False)

    main_bg_color = '#E0F2E1'
    window.configure(bg=main_bg_color)

    frame_title = tk.Frame(window, width=300, height=75, bg=main_bg_color)
    frame_menu = tk.Frame(window, width=300, height=500, bg=main_bg_color)

    frame_title.place(relx=0, rely=0, relwidth=1, relheight=0.15)
    frame_menu.place(relx=0, rely=0.15, relwidth=1, relheight=0.85)

    l_title = tk.Label(frame_title, text='Создать фанерный лист', font='Helvetica 15 bold', bg=main_bg_color,
                       fg='#2D2D2D')
    l_title.pack(expand=True)

    # Поля для ввода характеристик
    tk.Label(frame_menu, text="Название листа:", bg=main_bg_color, font='Helvetica 11').grid(row=0, column=0, padx=10,
                                                                                             pady=5, sticky='w')
    entry_name = tk.Entry(frame_menu, width=23, font='Helvetica 11', relief='groove', highlightthickness=0, bd=1)
    entry_name.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(frame_menu, text="Толщина (мм):", bg=main_bg_color, font='Helvetica 11').grid(row=1, column=0, padx=10,
                                                                                           pady=5, sticky='w')
    entry_thickness = tk.Entry(frame_menu, width=23, font='Helvetica 11', relief='groove', highlightthickness=0, bd=1)
    entry_thickness.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(frame_menu, text="Вид древесины:", bg=main_bg_color, font='Helvetica 11').grid(row=2, column=0, padx=10,
                                                                                            pady=5, sticky='w')

    # Получение данных из базы данных
    wood_types = get_wood_types()

    selected_wood = tk.StringVar(value=wood_types[0])
    wood_menu = ttk.OptionMenu(frame_menu, selected_wood, wood_types[0], *wood_types)
    wood_menu.config(width=18)
    wood_menu.grid(row=2, column=1, padx=10, pady=5, sticky='w')

    # Кнопка сохранения
    def save_characteristics():
        name = entry_name.get()
        thickness = entry_thickness.get()
        wood_type = selected_wood.get()

        try:
            thickness_value = float(thickness)  # Проверяем, что толщина — число
            if thickness_value <= 0:
                raise ValueError("Толщина должна быть положительным числом.")

            if name in get_plane_list():
                raise NameError("Такое название листа уже есть")
            save_plate(name, thickness, wood_type)

            messagebox.showinfo("Успех", "Данные успешно сохранены!")
            # window.destroy()
        except ValueError as e:
            print(e)
            messagebox.showerror("Ошибка", f"Некорректное значение толщины {thickness}")
        except NameError:
            messagebox.showerror('Ошибка', f'Название {name} уже есть в списке')

    # Canvas для кнопки
    canvas = tk.Canvas(frame_menu, width=300, height=80, bg=main_bg_color, highlightthickness=0)
    canvas.grid(row=3, column=0, columnspan=2, pady=35)

    # Создаем закругленную кнопку
    create_button(canvas, text="Сохранить", radius=15, command=save_characteristics)

    window.mainloop()


# create_plate()
