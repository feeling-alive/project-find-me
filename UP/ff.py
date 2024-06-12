from tkinter import *
from PIL import Image, ImageDraw
from random import randint
from tkinter import colorchooser, messagebox


def open_new_window():
    close_button.destroy()
    open_button.destroy()
    settings.grid(row=0, column=0, padx=6)
    choose_color.grid(row=0, column=1, padx=6)
    color_lab.grid(row=0, column=2, padx=6)
    choose_scale.grid(row=0, column=3, padx=6)

    doings.grid(row=1, column=0, padx=6)
    zalivka.grid(row=1, column=1)
    clear.grid(row=1, column=2)
    save.grid(row=1, column=3)

    canvas.grid(row=2, column=0, columnspan=7, padx=0, pady=0, sticky=E + W + S + N)
    # рисуем хвост - сегмент окружности
    canvas.create_arc(220, 454, 400, 180, fill="#FFFFFF", outline="#313939", width=3, start=-48, extent=90)
    # фигура кота из многоугольника
    canvas.create_polygon(120, 420, 170, 50, 220, 130, 270, 130, 320, 50, 370, 420, outline="#313939", width=3,
                          fill='#FFFFFF')
    # глаза - белые круги
    canvas.create_oval(175, 160, 245, 230, fill="#FFFFFF", outline="#313939", width=3)
    canvas.create_oval(245, 160, 315, 230, fill="#FFFFFF", outline="#313939", width=3)
    # глаза - зрачки
    canvas.create_oval(213, 192, 223, 202, fill="#000")
    canvas.create_oval(264, 192, 274, 202, fill="#000")
    # нос
    canvas.create_oval(235, 212, 255, 232, fill="#FFFFFF", outline="#313939", width=3)
    # линия от носа ко рту
    canvas.create_line(245, 232, 245, 285, width=3)
    # улыбка
    canvas.create_arc(210, 285, 280, 245, start=-10, extent=-160, style=ARC, width=3)
    # лапы
    canvas.create_oval(185, 390, 245, 430, fill='#FFFFFF', outline="#313939", width=3)
    canvas.create_oval(245, 390, 305, 430, fill='#FFFFFF', outline="#313939", width=3)
    # таблица
    canvas.create_rectangle(180, 320, 310, 370, fill="#FFFFFF", outline="#313939", width=3)
    # текст на таблице
    canvas.create_text(247, 348, text="МУР-МЯУ", font=('Courier', 18))
    # веревочки от таблички
    canvas.create_line(132, 320, 180, 345, width=3)
    canvas.create_line(310, 345, 358, 320, width=3)


def draw(event):
    x1, y1 = (event.x - brush_size), (event.y - brush_size)
    x2, y2 = (event.x + brush_size), (event.y + brush_size)
    canvas.create_oval(x1, y1, x2, y2, fill=color, width=0)
    draw_img.ellipse((x1, y1, x2, y2), fill=color, width=0)


def chooseColor():
    global color
    (rgb, hx) = colorchooser.askcolor()
    color = hx
    color_lab['bg'] = hx


def select(value):
    global brush_size
    brush_size = int(value)


def pour():
    canvas.delete('all')
    canvas['bg'] = color
    draw_img.rectangle((0, 0, 1280, 720), width=0, fill=color)


def clear_canvas():
    canvas.delete('all')
    canvas['bg'] = 'white'
    draw_img.rectangele((0, 0, 1280, 720), width=0, fill='while')


def save_img():
    filename = f'image_{randint(0, 10000)}.png'
    image1.save(filename)
    messagebox.showinfo('Сохранение', 'Сохранение под названием %s' % filename)


def popup(event):
    global x, y
    x = event.x
    y = event.y
    menu.post(event.x_poot, event.y_root)


x = 0
y = 0


win = Tk()
win.title('Раскраска')
win.geometry('1280x720')
win.resizable(0,0)

brush_size = 10
color = 'black'

canvas = Canvas(win, width = 1280, height = 720, bg='white')


canvas.bind('<B1-Motion>', draw)


image1 = Image.new('RGB', (1280, 640), 'white')
draw_img = ImageDraw.Draw(image1)


settings = Label(win, text='Параметры: ')

choose_color = Button(win, text=' Выбрать цвет', width=11, command=chooseColor)

color_lab = Label(win, bg=color, width=10)


v = IntVar(value=10)
choose_scale = Scale(win, variable=v, from_=1, to=100, orient=HORIZONTAL, command=select)

doings = Label(win, text='Действия: ')

zalivka = Button(win, text='Заливка: ', width=10, command=pour)

clear = Button(win, text='Очистить: ', width=10, command=clear_canvas)

save = Button(win, text='Сохранить: ', width=10, command=save_img)



open_button = Button(win, text = "Раскрасить", command=open_new_window,width=30, height=5,font='arial 15')
open_button.place(relx=.5, rely=.3, anchor="c")

close_button = Button(win, text = "Выход", command=win.quit,width=30, height=5,font='arial 15')
close_button.place(relx=.5, rely=.5, anchor="c")

win.mainloop()