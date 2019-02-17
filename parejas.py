import threading
import time
from random import shuffle
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo

raiz = Tk()
raiz.configure(bg='black')
raiz.title('Memory Game')
raiz.resizable(0, 0)
raiz.config(bd="35")
raiz.config(relief="ridge")

Imagenes = []
buttons = []
buttonsSelected = []
trys = 0
ok = 0
level = 1


def image(url):
    return PhotoImage(file=url)


im0 = image("images/balon.png")
im1 = image("images/Cap.png")
im2 = image("images/Minnie.png")
im3 = image("images/Minnie2.png")
im4 = image("images/Mickey1.png")
im5 = image("images/Mickey2.png")
im6 = image("images/base.png")
jugar = image("images/jugar.png")


def getImages():
    global Imagenes

    if level == 3:
        Imagenes = []
        Imagenes.append(im0)
        Imagenes.append(im0)
        Imagenes.append(im0)
        Imagenes.append(im1)
        Imagenes.append(im1)
        Imagenes.append(im1)
        Imagenes.append(im2)
        Imagenes.append(im2)
        Imagenes.append(im2)
        Imagenes.append(im3)
        Imagenes.append(im3)
        Imagenes.append(im3)
        return Imagenes
    else:
        Imagenes = []
        Imagenes.append(im0)
        Imagenes.append(im1)
        Imagenes.append(im2)
        Imagenes.append(im3)
        Imagenes.append(im4)
        Imagenes.append(im5)
        Imagenes.append(im0)
        Imagenes.append(im1)
        Imagenes.append(im2)
        Imagenes.append(im3)
        Imagenes.append(im4)
        Imagenes.append(im5)
        return Imagenes


# random position images
shuffle(getImages())

boton2 = ttk.Button(raiz)
boton2.grid(row=0, column=4, ipadx=50, ipady=50, columnspan=1, padx=10, pady=10, rowspan="4")
boton2.config(image=getImages()[round(5)])


# create grid buttons
for i in range(3):
    for j in range(4):
        button = ttk.Button(raiz)
        button.config(cursor="pirate")
        button.grid(row=i, column=j, ipadx=10, ipady=10, padx=10, pady=10, sticky='')
        buttons.append(button)

# set images random
for index, botton in enumerate(buttons):
    botton.configure(image=Imagenes[index], command=lambda b=botton, i=index: Comparar(b, i), state=DISABLED)


# thread random images
def inicio():
    global level

    if level == 0:
        boton2.grid(row=0, column=4, ipadx=50, ipady=50, columnspan=1, padx=10, pady=10, rowspan="4")
        boton2.config(image=getImages()[round(5)])
        level = 1
        label.config(text="Nivel : " + str(level))

    threading \
        .Thread(target=Lanzar, args=[getImages()]) \
        .start()


# tarjet thread
def Lanzar(Imagenes):
    shuffle(Imagenes)

    if level == 1:
        for i in range(5):
            boton2.config(image=Imagenes[round(i)])
            time.sleep(0.1)

    for index, botton in enumerate(buttons):
        botton.configure(image=Imagenes[index], command=lambda b=botton, i=index: Comparar(b, i))

    time.sleep(2)
    for i in buttons:
        i.configure(image=im6)

    for b in buttons:
        b.configure(state=ACTIVE)


def Comparar(button, indexImage):
    global buttonsSelected, trys, ok, level, Imagenes

    button.configure(state=DISABLED)
    buttonsSelected.append(button)

    button.configure(image=Imagenes[indexImage])

    if level == 1:

        if button.cget("image")[0] == boton2.cget("image")[0]:
            if trys == 0:
                showinfo("window", "Excelente! Lo lograste a la primera!")
            else:
                showinfo("window", "Lo lograste en: " + str(trys) + " intentos!")

            showinfo("window", "Vamos con el nivel 2!")
            trys = 0
            level = 2
            esconder(buttonsSelected)
            buttonsSelected = []
            boton2.grid_remove()
            label.config(text="Nivel : " + str(level))

        else:

            esconder(buttonsSelected)
            trys += 1

        return

    elif len(buttonsSelected) == 2:

        # ok
        if buttonsSelected[0].cget("image")[0] == buttonsSelected[1].cget("image")[0]:
            if level == 2:
                for b in buttonsSelected:
                    b.configure(image=Imagenes[indexImage], state=DISABLED)
                ok += 1
        # fail
        else:
            esconder(buttonsSelected)

        if level == 2:
            buttonsSelected = []

        trys += 1

        if ok == 6 and level == 2:
            showinfo("window", "Lo lograste en: " + str(trys) + " intentos!")
            trys = 0
            ok = 0
            showinfo("window", "Vamos con el nivel 3!")
            level = 3
            label.config(text="Nivel : " + str(level))

            threading \
                .Thread(target=Lanzar, args=[getImages()]) \
                .start()

    elif len(buttonsSelected) == 3 and level == 3:

        # ok
        if buttonsSelected[0].cget("image")[0] == buttonsSelected[1].cget("image")[0] == \
                buttonsSelected[2].cget("image")[0]:
            for b in buttonsSelected:
                b.configure(image=Imagenes[indexImage], state=DISABLED)
            ok += 1
        # fail
        else:
            esconder(buttonsSelected)

        buttonsSelected = []
        trys += 1

        if ok == 4:
            showinfo("window", "Lo lograste en: " + str(trys) + " intentos!")
            trys = 0
            ok = 0
            label.config(text="Juego Terminado!")
            level = 0


def esconder(botones):
    threading\
        .Thread(target=wait, args=[botones, im6])\
        .start()


def wait(buttonSelected, imageBase):
    time.sleep(0.5)
    for b in buttonSelected:
        b.configure(image=imageBase, state="normal")


boton1 = ttk.Button(raiz, text="Inicio", command=inicio)
boton1.configure(image=jugar)
boton1.configure(cursor="circle")
boton1.grid(row=4, column=0, pady=20, columnspan=2)

label = Label(raiz, text="Nivel : " + str(1))
label.grid(row=4, column=2, ipadx=0, ipady=0, columnspan=2)
label.config(fg="red")
label.config(bg="black")
label.config(font=("Courier", 44))

raiz.mainloop()