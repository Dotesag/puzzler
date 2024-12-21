import tkinter as tk
import subprocess

from plate_list import plate_list
from create_plate import create_plate
from create_puzzle import create_puzzle
from puzzle_list import puzzle_list


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

    # Bind click events to the canvas
    def on_click(event):
        if command:
            command()

    canvas.tag_bind(btn, "<Button-1>", on_click)
    canvas.tag_bind(text_id, "<Button-1>", on_click)


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

# Adding buttons
button_width = 200
button_height = 40
button_spacing_x = 20
button_spacing_y = 30
start_x = (720 - (button_width * 2 + button_spacing_x)) / 2
start_y = 100

# Верхний ряд
create_button(canvas, start_x, start_y, start_x + button_width, start_y + button_height, "Создать лист", radius=15,
              command=create_plate)
create_button(canvas, start_x + button_width + button_spacing_x, start_y,
              start_x + button_width * 2 + button_spacing_x, start_y + button_height, "Создать пазл", radius=15,
              command=create_puzzle)

# Нижний ряд
create_button(canvas, start_x, start_y + button_height + button_spacing_y,
              start_x + button_width, start_y + button_height * 2 + button_spacing_y, "Список листов", radius=15,
              command=plate_list)
create_button(canvas, start_x + button_width + button_spacing_x,
              start_y + button_height + button_spacing_y,
              start_x + button_width * 2 + button_spacing_x,
              start_y + button_height * 2 + button_spacing_y, "Список пазлов", radius=15, command=puzzle_list)

window.mainloop()
