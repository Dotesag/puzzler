from tkinter import *

def finish():
    root.destroy()  # ручное закрытие окна и всего приложения
    print("Закрытие приложения")

root = Tk()
root.geometry("500x400+730+300")
root.minsize(500,400) 

icon = PhotoImage(file = "ico.png")
root.iconphoto(True, icon)
root.title("Puzzler")


root.protocol("WM_DELETE_WINDOW", finish)

root.mainloop()