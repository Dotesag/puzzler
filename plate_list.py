import tkinter as tk
from tkinter import ttk
import sqlite3


def get_plane_list():
    data = []
    with sqlite3.connect('db/database.db') as db:
        cursor = db.cursor()
        query = '''
            SELECT * FROM planes
        '''
        cursor.execute(query)
        data = cursor.fetchall()
    return data


def plate_list():
    window = tk.Tk()
    window.title("Puzzler - список листов фанер")
    window.geometry('250x420')
    window.minsize(350, 420)
    window.resizable(False, False)

    # Фоновые цвета
    main_bg_color = '#E0F2E1'
    list_bg_color = '#F6FFF6'
    scrollbar_bg_color = '#D0E8D0'

    frame_title = tk.Frame(window, width=300, height=75, bg=main_bg_color)
    frame_menu = tk.Frame(window, width=300, height=500, bg=main_bg_color)

    frame_title.place(relx=0, rely=0, relwidth=1, relheight=0.15)
    frame_menu.place(relx=0, rely=0.15, relwidth=1, relheight=0.85)

    l_title = tk.Label(frame_title, text='Список фанерных листов', font='Helvetica 15 bold', bg=main_bg_color,
                       fg='#2D2D2D')
    l_title.pack(expand=True)

    plane_list = get_plane_list()
    redacted_plane_list = []
    for g in range(len(plane_list)):
        i = plane_list[g]
        redacted_plane_list.append(
            f'{g + 1}. Название: "{i[0]}"\n'
            f'{len(str(g + 1)) * " " + "  "}Древесина: {i[1]}\n'
            f'{len(str(g + 1)) * " " + "  "}Толщина: {i[2]} мм\n'
        )

    frame_list = tk.Frame(frame_menu, bg=main_bg_color)
    frame_list.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Стили для Text и Scrollbar
    text_widget = tk.Text(frame_list, wrap="word", height=20, bg=list_bg_color, font='Verdana 10', relief=tk.FLAT)
    text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    style = ttk.Style()
    style.configure("Vertical.TScrollbar", background=scrollbar_bg_color, troughcolor=main_bg_color,
                    bordercolor=main_bg_color)

    scrollbar = ttk.Scrollbar(frame_list, orient="vertical", command=text_widget.yview, style="Vertical.TScrollbar")
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    text_widget.config(yscrollcommand=scrollbar.set)

    text_widget.tag_configure("indent", lmargin1=5, lmargin2=5)
    for plane in redacted_plane_list:
        text_widget.insert("end", plane + "\n", 'indent')

    window.mainloop()


plate_list()
