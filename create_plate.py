import tkinter as tk

window = tk.Tk()
window.title("Puzzler")

frame_title = tk.Frame(window, width=300, height=75, bg='#DCDCDC')
frame_menu = tk.Frame(window, width=300, height=500, bg='#E2E2E2')

frame_title.pack()
frame_menu.pack()

window.mainloop()
