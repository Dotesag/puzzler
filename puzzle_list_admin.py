import tkinter as tk
from tkinter import ttk
import sqlite3


def get_plane_list():
    data = []
    with sqlite3.connect('db/database.db') as db:
        cursor = db.cursor()
        query = '''
            SELECT * FROM puzzles
        '''
        cursor.execute(query)
        data = cursor.fetchall()
    return data


def view_puzzle(puzzle_id):
    # Функция для обработки клика по кнопке "Обзор"
    print(f"Обзор для паззла ID: {puzzle_id}")
    # Здесь можно вызывать другой файл или окно программы


def puzzle_list():
    window = tk.Toplevel()
    window.title("Puzzler - список пазлов")
    window.geometry('350x420')
    window.minsize(350, 420)
    window.resizable(False, False)

    # Фоновые цвета
    main_bg_color = '#E0F2E1'
    list_bg_color = '#F6FFF6'
    scrollbar_bg_color = '#D0E8D0'
    button_color = '#A5D6A7'

    frame_title = tk.Frame(window, width=300, height=75, bg=main_bg_color)
    frame_menu = tk.Frame(window, width=300, height=500, bg=main_bg_color)

    frame_title.place(relx=0, rely=0, relwidth=1, relheight=0.15)
    frame_menu.place(relx=0, rely=0.15, relwidth=1, relheight=0.85)

    l_title = tk.Label(frame_title, text='Список созданных пазлов', font='Helvetica 15 bold', bg=main_bg_color,
                       fg='#2D2D2D')
    l_title.pack(expand=True)

    plane_list = get_plane_list()
    print(plane_list)

    frame_list = tk.Frame(frame_menu, bg=main_bg_color)
    frame_list.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    canvas = tk.Canvas(frame_list, bg=list_bg_color, relief=tk.FLAT)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(frame_list, orient="vertical", command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)
    scrollable_frame = tk.Frame(canvas, bg=list_bg_color)
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    for g, i in enumerate(plane_list, start=1):
        puzzle_frame = tk.Frame(scrollable_frame, bg=list_bg_color, pady=5)
        puzzle_frame.pack(fill=tk.X, padx=5, pady=5)

        text_label = tk.Label(
            puzzle_frame,
            text=f'{g}. Название: "{i[0]}"\n  Размер: {i[1]}\n  Лист: {i[2]}',
            justify=tk.LEFT,
            bg=list_bg_color,
            font='Verdana 10'
        )
        text_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

    window.mainloop()


if __name__ == "__main__":
    puzzle_list()
