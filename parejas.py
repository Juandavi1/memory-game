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

#
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


# retornar el array de imagenes dependiendo el nivel
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

# revolver imagenes dentro del array
shuffle(getImages())

# boton de primer nivel que se posiciona fuera de la matriz para mostrar la imagen que debe buscar. esto en el nivel 1.
boton2 = ttk.Button(raiz)
boton2.grid(row=0, column=4, ipadx=50, ipady=50, columnspan=1, padx=10, pady=10, rowspan="4")
boton2.config(image=getImages()[round(5)]) # escoger una imagen cualquier dentro del array de images

# crear la matriz de botones
for i in range(3):
    for j in range(4):
        button = ttk.Button(raiz)
        button.config(cursor="pirate")
        button.grid(row=i, column=j, ipadx=10, ipady=10, padx=10, pady=10, sticky='')
        buttons.append(button)

# asignar evento 'Comparar' a todos los botones y establecer la configuracion inicial. images y estado.
for index, botton in enumerate(buttons):
    botton.configure(image=Imagenes[index], command=lambda b=botton, i=index: Comparar(b, i), state=DISABLED)


# mostrar boton de primer nivel y lanzar un thread(hilo) para iniciar el juego
def inicio():
    global level

    if level == 0:
        boton2.grid(row=0, column=4, ipadx=50, ipady=50, columnspan=1, padx=10, pady=10, rowspan="4")
        boton2.config(image=getImages()[round(5)])
        level = 1
        label.config(text="Nivel : " + str(level))

    reset()
    threading \
        .Thread(target=Lanzar, args=[getImages()]) \
        .start()


#inicio de juego
def Lanzar(Imagenes):

    #revolver imagenes
    shuffle(Imagenes)

    # selecciona una imagen aleatoria con la que jugar el primer nivel.
    if level == 1:
        for i in range(5):
            boton2.config(image=Imagenes[round(i)])
            time.sleep(0.1)

    # asignar configuracion inicial de los botones
    for index, botton in enumerate(buttons):
        botton.configure(image=Imagenes[index], command=lambda b=botton, i=index: Comparar(b, i))

    # esperar dos segundos y setear todos los botones con imagen por defecto
    time.sleep(2)
    for i in buttons:
        i.configure(image=im6)

    # activar todos los botones
    for b in buttons:
        b.configure(state=ACTIVE)


# retornar el nombre de la imagen dentro de un boton
def imageName(button):
    return button.cget("image")[0]


# inicializar los contadores
def reset():
    global buttonsSelected, trys, ok
    buttonsSelected = []
    trys = 0
    ok = 0



def Comparar(button, indexImage):
    global buttonsSelected, trys, ok, level, Imagenes

    button.configure(state=DISABLED)
    buttonsSelected.append(button)

    button.configure(image=Imagenes[indexImage])

    if level == 1:
        # si las imagenes coinciden
        if imageName(button) == imageName(boton2):
            if trys == 0:
              showinfo("window", "Excelente! Lo lograste a la primera!")
        # si no coinciden
            else:
                showinfo("window", "Lo lograste en: " + str(trys) + " intentos!")

            showinfo("window", "Vamos con el nivel 2!")
            level = 2
            esconder(buttonsSelected)
            boton2.grid_remove()
            label.config(text="Nivel : " + str(level))
            reset()

        else:
            esconder(buttonsSelected)

        trys += 1

        return

    elif len(buttonsSelected) == 2:

        # si son iguales
        if imageName(buttonsSelected[0]) == imageName(buttonsSelected[1]):
            if level == 2:
                for b in buttonsSelected:
                    b.configure(image=Imagenes[indexImage], state=DISABLED)
                ok += 1
        # no son iguales
        else:
            esconder(buttonsSelected)

        if level == 2:
            buttonsSelected = []

        trys += 1

        if ok == 6 and level == 2:
            showinfo("window", "Lo lograste en: " + str(trys) + " intentos!")
            showinfo("window", "Vamos con el nivel 3!")
            level = 3
            label.config(text="Nivel : " + str(level))
            reset()

            threading \
                .Thread(target=Lanzar, args=[getImages()]) \
                .start()

    elif len(buttonsSelected) == 3 and level == 3:

        # ok
        if imageName(buttonsSelected[0]) == imageName(buttonsSelected[1]) == imageName(buttonsSelected[2]):
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
            label.config(text="Juego Terminado!")
            level = 0
            reset()

# aisngar a todos los botones la imagen por defecto
def esconder(botones):
    threading\
        .Thread(target=wait, args=[botones, im6])\
        .start()

# poner a los botones pasados por parametro, la image base
def wait(buttonSelected, imageBase):
    time.sleep(0.5)
    for b in buttonSelected:
        b.configure(image=imageBase, state="normal")


# configuracion boton Jugan!
boton1 = ttk.Button(raiz, text="Inicio", command=inicio)
boton1.configure(image=jugar)
boton1.configure(cursor="circle")
boton1.grid(row=4, column=0, pady=20, columnspan=2)

# configuracion Label que indica los niveles
label = Label(raiz, text="Nivel : " + str(1))
label.grid(row=4, column=2, ipadx=0, ipady=0, columnspan=2)
label.config(fg="red")
label.config(bg="black")
label.config(font=("Courier", 44))

#ejecutar interfaz !
raiz.mainloop()