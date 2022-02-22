# On importe les bibliothèques nécessaires pour le jeu

from tkinter import *
import tkinter as tk
from random import randrange

def move():
    global x,fenetre
    global y,pX,pY
    global Serpent
    can.delete('all')
    i=len(Serpent)-1
    j=0
    while i > 0:
        Serpent[i][0]=Serpent[i-1][0]
        Serpent[i][1]=Serpent[i-1][1]
        can.create_oval(Serpent[i][0], Serpent[i][1], Serpent[i][0] +10, Serpent[i][1]+10,outline='green', fill='black')
        i=i-1

    can.create_rectangle(pX, pY, pX+9, pY+9, outline='red', fill='black')

    if direction  == 'gauche':
        Serpent[0][0]  = Serpent[0][0] - dx
        if Serpent[0][0] < 0:
            Serpent[0][0] = 493
    elif direction  == 'droite':
        Serpent[0][0]  = Serpent[0][0] + dx
        if Serpent[0][0] > 493:
            Serpent[0][0] = 0
    elif direction  == 'haut':
        Serpent[0][1]  = Serpent[0][1] - dy
        if Serpent[0][1] < 0:
            Serpent[0][1] = 493
    elif direction  == 'bas':
        Serpent[0][1]  = Serpent[0][1] + dy
        if Serpent[0][1] > 493:
            Serpent[0][1] = 0

    can.create_oval(Serpent[0][0], Serpent[0][1], Serpent[0][0]+10, Serpent[0][1]+10,outline='green', fill='green')
    test()
    test()

    if flag != 0:
        fen.after(60, move)

def newGame():
    global pX,pY
    global flag
    if flag == 0:
        flag = 1
    move()

def left(event):
    global direction
    direction = 'gauche'

def right(event):
    global direction
    direction = 'droite'

def up(event):
    global direction
    direction = 'haut'

def down(event):
    global direction
    direction = 'bas'

mange = 0

def update_counter():
    global mange
    return mange

def test():
    global pomme, mange
    global x,y,pX,pY
    global Serpent
    if Serpent[1][0]>pX-7 and  Serpent[1][0]<pX+7:
        if Serpent[1][1]>pY-7 and Serpent[1][1]<pY+7:
            pX = randrange(5, 495)
            pY = randrange(5, 495)
            can.coords(pomme,pX, pY, pX+5, pY+5)
            Serpent.append([0,0])
            mange=mange+1
            update_counter()
            print(mange)

            count.set(mange)


x = 245
y = 24
dx, dy = 10, 10
flag = 0
direction = 'haut'
Serpent=[[x,y],[x+2.5,y+2.5],[x+5,y+5],[0,0]]

pX = randrange(5, 495)
pY = randrange(5, 495)


fen = Tk()
can = Canvas(fen, width=500, height=500, bg='black')
can.pack(side=TOP, padx=5, pady=5)


oval1=can.create_oval(Serpent[1][0], Serpent[1][1], Serpent[1][0] +10, Serpent[1][1]+10, outline='green', fill='black')

oval = can.create_oval(Serpent[0][0], Serpent[0][1], Serpent[0][0]+10, Serpent[0][1]+10, outline='green', fill='green')

pomme = can.create_rectangle(pX, pY, pX+9, pY+9, outline='red', fill='black')

b1 = Button(fen, text='Lancer', command=newGame, bg='black' , fg='white')
b1.pack(side=LEFT, padx=5, pady=5)

b2 = Button(fen, text='Quitter', command=fen.destroy, bg='black' , fg='white')
b2.pack(side=RIGHT, padx=5, pady =5)

tex1 = Label(fen, text="Cliquez sur 'Lancer' ", bg='black' , fg='white')
tex1.pack(padx=0, pady=11)

count = StringVar()
text_point = Label(fen, textvariable=count,bg='black', fg='white')
text_point.pack(padx=0,pady=5)

fen.bind('<d>', right)
fen.bind('<q>', left)
fen.bind('<z>' , up)
fen.bind('<s>', down)

fen.mainloop()


