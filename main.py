import tkinter as tk

window = tk.Tk()
window.title("Puzzler")
window.geometry('720x510')
window.minsize(200, 350)

frame_title = tk.Frame(window, width=720, height=75, bg='#DCDCDC')
frame_menu = tk.Frame(window, width=720, height=500, bg='green')

frame_title.place(relx=0, rely=0, relwidth=1, relheight=0.15)
frame_menu.place(relx=0, rely=0.15, relwidth=1, relheight=0.85)

window.mainloop()
