import tkinter as tk
import subprocess
import sqlite3

# from plate_list import plate_list
# from create_plate import create_plate
# from create_puzzle import create_puzzle
# from puzzle_list import puzzle_list

from puzzle_list_admin import puzzle_list


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


def create_button(canvas, x1, y1, x2, y2, text, radius, command=None):
    btn = create_rounded_rectangle(canvas, x1, y1, x2, y2, radius, fill="#4CAF50", outline="#388E3C", width=2)
    text_id = canvas.create_text(
        (x1 + x2) / 2,
        (y1 + y2) / 2,
        text=text,
        font=("Helvetica", 14, "bold"),
        fill="white"
    )

    def on_click(event):
        if command:
            command()

    canvas.tag_bind(btn, "<Button-1>", on_click)
    canvas.tag_bind(text_id, "<Button-1>", on_click)


def save_price_to_db(price):
    with sqlite3.connect('db/database.db') as db:
        cursor = db.cursor()

        query = '''

                    UPDATE admin SET price=? WHERE name='puzzle'

                '''
        cursor.execute(query, (price,))


def get_price():
    with sqlite3.connect('db/database.db') as db:
        cursor = db.cursor()
        query = '''
            SELECT price FROM admin
        '''
        cursor.execute(query)
        data = cursor.fetchall()
    return list(data)[0][0]


window = tk.Tk()
window.title("Puzzler")
window.geometry('720x510')
window.resizable(False, False)

# Установка цвета самого заднего фона окна
window.configure(bg="#E0F2E1")  # Цвет совпадает с основным фоном Canvas

canvas = tk.Canvas(window, width=720, height=510, bg="#E0F2E1", highlightthickness=0)
canvas.pack()

create_rounded_rectangle(canvas, 5, 5, 715, 505, radius=30, fill="#E0F2E1", outline="#57B748", width=1)
canvas.create_text(360, 40, text="Меню", font=("Helvetica", 24, "bold"), fill="black")

# Добавление кнопок
button_width = 200
button_height = 40
button_spacing_y = 30
start_x = (720 - button_width) / 2
start_y = 150

create_button(canvas, start_x, start_y, start_x + button_width, start_y + button_height, "Список заказов", radius=15,
              command=puzzle_list)

# Добавление текста и поля ввода
price = get_price()
price_label = canvas.create_text(360, start_y + button_height + button_spacing_y + 50,
                                 text=f"Примерная цена на пазл: {price}", font=("Helvetica", 16),
                                 fill="black")

entry_frame = tk.Frame(window, bg="#E0F2E1")
entry_frame.place(relx=0.5, rely=0.6, anchor="center")

price_entry = tk.Entry(entry_frame, font=("Helvetica", 14), justify="center")
price_entry.insert(0, str(price))
price_entry.pack()


def validate_input(new_value):
    return new_value.isdigit() or new_value == ""


validate_command = window.register(validate_input)
price_entry.config(validate="key", validatecommand=(validate_command, "%P"))


def on_save_price():
    price = price_entry.get()
    if price.isdigit():
        save_price_to_db(price)
        # Обновляем текст с ценой
        canvas.itemconfig(price_label, text=f"Примерная цена на пазл: {price}")
        price_entry.delete(0, tk.END)  # Очищаем поле ввода


save_button_y = start_y + button_height + 5 * button_spacing_y
create_button(canvas, start_x, save_button_y, start_x + button_width, save_button_y + button_height, "Сохранить цену",
              radius=15, command=on_save_price)

window.mainloop()
