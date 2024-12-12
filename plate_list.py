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


window = tk.Tk()
window.title("Puzzler - список листов фанер")
window.geometry('250x420')
window.minsize(350, 420)
window.resizable(False, False)

frame_title = tk.Frame(window, width=300, height=75, bg='#DCDCDC')
frame_menu = tk.Frame(window, width=300, height=500, bg='#E2E2E2')

frame_title.place(relx=0, rely=0, relwidth=1, relheight=0.15)
frame_menu.place(relx=0, rely=0.15, relwidth=1, relheight=0.85)

l_title = tk.Label(frame_title, text='Список фанерных листов', font='Helvetica 15 bold', bg='#DCDCDC', fg='#2D2D2D')
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

frame_list = tk.Frame(frame_menu, bg='#E2E2E2')
frame_list.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

text_widget = tk.Text(frame_list, wrap="word", height=20, bg="#FFFFFF", font='Verdana 10')
text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

scrollbar = ttk.Scrollbar(frame_list, orient="vertical", command=text_widget.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
text_widget.config(yscrollcommand=scrollbar.set)

text_widget.tag_configure("indent", lmargin1=5, lmargin2=5)
for plane in redacted_plane_list:
    text_widget.insert("end", plane + "\n", 'indent')

window.mainloop()
