from tkinter import *
from tkinter import ttk     # подключаем пакет ttk
from logic import *

root = Tk() # создаем корневой объект - окно
root.title("СапёрБот") # устанавливаем заголовок окна
root.geometry("300x250+600+200") # устанавливаем размеры окна
root.resizable(False, False)    #Запрет на изменения размера окна

label = ttk.Label(text="Выберите уровень сложности:")
buttonEasy = ttk.Button(text="Новичок 9х9 клеток ", command= lambda difLevel = 1 :start(difLevel + 10*enabled.get()))
buttonMedium = ttk.Button(text="Любитель 16х16 клеток", command= lambda difLevel = 2 :start(difLevel + 10*enabled.get()))
buttonHard = ttk.Button(text="Профессионал 16х30 клеток", command= lambda difLevel = 3 :start(difLevel + 10*enabled.get()))
enabled = IntVar()
checkbox = ttk.Checkbutton(text="Включить режим без угадывания?", variable=enabled)


label.pack(pady = 10)
buttonEasy.pack(pady = 15)
buttonMedium.pack(pady = 15)
buttonHard.pack(pady = 15)
checkbox.pack(pady= 10)

root.mainloop()



