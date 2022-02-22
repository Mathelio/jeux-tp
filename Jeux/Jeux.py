# On importe les bibliothèques nécessaires pour les jeux

from random import randint, shuffle, randrange
from tkinter import *
from PIL import Image, ImageTk
import tkinter as tk

#---------------------------- Memory ---------------------------

def Memory():

    # On définit nos variables de départ et les plus importantes
    images_dep = []         # liste comprenant les informations des images
    vignettes = []         # liste reliant les photos à une vignette
    vignettes_jouees = []  # liste comprenant les vignettes jouées
    points = 0
    resultat = [0]
    fin = False
    apteajouer = True
    nombre_lignes, nombre_colonnes = 4, 5


    # Cette fonction permet de créer un widget menu permettant de dérouler ce dernier
    def conception_menu(fenetre):
        position_menu = Menu(fenetre)
        fenetre.config(menu=position_menu)
        jeu = Menu(position_menu, tearoff=False) # Permet de ne pas détacher les sous-menus de la fenêtre principale et de s'ouvrir dans le menu déroulant
        position_menu.add_cascade(label='Option', menu=jeu) # Ajouter dans le menu un paramètre permettant l'execution plus tard d'une commande
        jeu.add_command(label='Quitter', command=fenetre.destroy)


    # Conception d'un canevas dans la fenêtre
    def conception_canevas(fenetre, colonne, ligne):
        return Canvas(fenetre, width=(108*colonne)+10, height=(108*ligne)+10, bg='white')


    # Conception de la fenetre du jeu
    fenetre = Tk()
    fenetre.title("Memory Projet")
    conception_menu(fenetre)
    scene_jeu = Frame(fenetre)
    scene_jeu.pack()
    canvas=conception_canevas(scene_jeu, nombre_colonnes, nombre_lignes)
    canvas.pack(side = TOP, padx = 1, pady = 1)
    points_ = Label(fenetre, text = "                                   Nombre de points : 0", font="Calibri 18")
    points_.pack(pady = 1, side = LEFT)



    # Cette partie permet de rechercher les images et permettre au programme de les utiliser
    def charger_images_dep():
        del images_dep[:]   # Cette partie va permettre de supprimer tous éléments de la liste
        nombre_images_dep = 21
        selection_vignettes = [] # liste qui va contenir les photos que les vignettes vont utiliser
        selection_vignettes.append(0)
        i=0
        while i < nombre_images_dep-1: # Mélange toutes les vignettes aléatoirement pour définir celles qui vont être utilisées
            x = randint(1, nombre_images_dep-1)
            if x not in selection_vignettes:
                selection_vignettes.append(x)
                i += 1
        for i in range(nombre_images_dep): # Cette partie va permettre d'aller chercher les images dans le dossier et les attribuer à la liste que l'on a définit au tout début
            nom = 'vignette-' + str(selection_vignettes[i]) + '.gif'
            image = PhotoImage(file = nom)
            images_dep.append(image)

    # Cette fonction permet beaucoup de choses : donner au joueur son nombre de points, gère le retournement des vignettes et l'affichage des vignettes pendant un lapse de temps pour permettre au joueur de se souvenir des combinaisons
    def gerer_tirage():
        global nombre_colonnes, nombre_lignes, vignettes_jouees
        global points, apteajouer
        if vignettes[vignettes_jouees[0]-1] == vignettes[vignettes_jouees[1]-1]: # Enlève les vignettes identiques si elles ont été trouvées par le joueur
            canvas.delete(vignettes_jouees[0])
            canvas.delete(vignettes_jouees[1])
            resultat[points] += 1
        else:
            canvas.itemconfig(vignettes_jouees[0], image = images_dep[0]) # Retourne les vignettes que le joueur a préalablement sélectionnées si elles sont différentes
            canvas.itemconfig(vignettes_jouees[1], image = images_dep[0])
        vignettes_jouees = []
        tnbpoints = '                                   Nombre de points : ' + str(resultat[0]*1)
        points_.config(text = tnbpoints)
        apteajouer = True # Actionne l'évènement : clic de la souris

    # Mélange des vignettes pour ensuite permettre de les placer dans le programme
    def met_en_desordre_vignettes():
        global nombre_colonnes, nombre_lignes, vignettes
        nombre_vignettes = 5 * 4
        vignettes=list(range(1,nombre_vignettes//2+1))*2
        shuffle(vignettes)

    # Cette fonction va permettre les actions qui vont se dérouler dans la scène du jeu
    def action_vignettes(event):
        global vignettes_jouees, apteajouer, scene_jeu, fin
        if len(vignettes_jouees) < 2:
            vignettes_selec = canvas.find_closest(event.x, event.y) # Attribuer les coordonnées du clic à celle de l'image y correspondant le plus
            vignette_info = vignettes_selec[0]
            if fin:
                fin = False
            else:
                canvas.itemconfig(vignette_info, image = images_dep[vignettes[vignette_info-1]]) # Fait apparaître la vignette face ouverte
                if len(vignettes_jouees) == 0:
                    vignettes_jouees.append(vignette_info)  # Permet de garder en mémoire la vignette étant utilisée
                elif vignette_info != vignettes_jouees[0]:    # Empêche le joueur de cliquer deux fois sur la même vignette
                    vignettes_jouees.append(vignette_info)
        if apteajouer and len(vignettes_jouees) == 2:
            apteajouer = False                  # Fait que l'élévènement clic devient inncactif
            scene_jeu.after(1000,gerer_tirage)    # Attente de 1 seconde pour pouvoir rejouer



    charger_images_dep()
    met_en_desordre_vignettes()
    for i in range(nombre_colonnes):     # Partie de programme permettant le clic et la détection de ce dernier provoquant le retournement des vignettes
        for j in range(nombre_lignes):
            canvas.create_image((108*i)+60, (108*j)+60, image = images_dep[0])

    canvas.bind("<Button-1>", action_vignettes)    # On va pouvoir à l'aide de cette ligne relever le clic de la souris

    frame.pack()


#---------------------------- PPC ---------------------------

def PPC(): # Création d'une fonction qui contient toutes les autres
    def augmenter_scores(mon_coup,ton_coup): # Fonction qui permet de donner les points en fonction du gagnant
        global mon_score, ton_score
        if mon_coup == 1 and ton_coup == 2:
            ton_score += 1
        elif mon_coup == 2 and ton_coup == 1:
            mon_score += 1
        elif mon_coup == 1 and ton_coup == 3:
            mon_score += 1
        elif mon_coup == 3 and ton_coup == 1:
            ton_score += 1
        elif mon_coup == 3 and ton_coup == 2:
            mon_score += 1
        elif mon_coup == 2 and ton_coup == 3:
            ton_score += 1

    def jouer(ton_coup):
        global mon_score, ton_score, score1, score2 # Appel les variables nécessaires
        mon_coup = randint(1,3)
        if mon_coup==1:
            lab3.configure(image=pierre)
        elif mon_coup==2:
            lab3.configure(image=papier)
        else:
            lab3.configure(image=ciseaux)
        augmenter_scores(mon_coup,ton_coup)
        score1.configure(text=str(ton_score))
        score2.configure(text=str(mon_score))

    def jouer_pierre():
        jouer(1)
        lab1.configure(image=pierre)

    def jouer_papier():
        jouer(2)
        lab1.configure(image=papier)

    def jouer_ciseaux():
        jouer(3)
        lab1.configure(image=ciseaux)

    def reinit():
        global mon_score,ton_score,score1,score2,lab1,lab3
        ton_score = 0
        mon_score = 0
        score1.configure(text=str(ton_score))
        score2.configure(text=str(mon_score))
        lab1.configure(image=rien)
        lab3.configure(image=rien)


    global mon_score,ton_score,score1,score2,lab1,lab3


    frame.pack()
    canvas.destroy()

    # variables globales
    ton_score = 0
    mon_score = 0

    #images
    rien = ImageTk.PhotoImage(Image.open("rien.gif"))
    versus = ImageTk.PhotoImage(Image.open("versus.gif"))
    pierre = ImageTk.PhotoImage(Image.open("pierre.gif"))
    papier = ImageTk.PhotoImage(Image.open("papier.gif"))
    ciseaux = ImageTk.PhotoImage(Image.open("ciseaux.gif"))

    # Label
    texte1 = Label(frame, text="Humain :", font=("Helvetica", 16))
    texte1.grid(row=0,column=0)

    texte2 = Label(frame, text="Machine :", font=("Helvetica", 16))
    texte2.grid(row=0,column=2)

    texte3 = Label(frame, text="Pour jouer, cliquez sur une des icones ci-dessous.")
    texte3.grid(row=3, columnspan =3, pady =5)

    score1 = Label(frame, text="0", font=("Helvetica", 16))
    score1.grid(row=1, column=0)

    score2 = Label(frame, text="0", font=("Helvetica", 16))
    score2.grid(row=1, column=2)

    lab1 = Label(frame, image=rien)
    lab1.grid(row =2, column =0)

    lab2 = Label(frame, image=versus)
    lab2.grid(row =2, column =1)

    lab3 = Label(frame, image=rien)
    lab3.grid(row =2, column =2)

    # boutons
    bouton1 = Button(frame,command=jouer_pierre)
    bouton1.configure(image=pierre)
    bouton1.grid(row =4, column =0)

    bouton2 = Button(frame,command=jouer_papier)
    bouton2.configure(image=papier)
    bouton2.grid(row =4, column =1,)

    bouton3 = Button(frame,command=jouer_ciseaux)
    bouton3.configure(image=ciseaux)
    bouton3.grid(row =4, column =2)

    bouton4 = Button(frame,text='Recommencer',command=reinit)
    bouton4.grid(row =5, column =0, pady =10, sticky=E)

    bouton5 = Button(frame,text='Quitter',command=fen.destroy)
    bouton5.grid(row =5, column =2, pady =10, sticky=W)

    frame.pack()


#---------------------------- Puzzles ---------------------------

listephoto=[]
vignettes_cliquees = []
partie_en_cours = 'aucune'


def gestion_cliques(event):
    global vignettes_cliquees, photorien
    print("position x :", event.x, "  , position y :", event.y)
    vignetteSel = canvas.find_closest(event.x, event.y) # methode qui donne l'ID de ce qu'il a aux coordonnees x, y
    print(vignetteSel)
    canvas.itemconfigure(vignetteSel[0], image = photorien)
    if len(vignettes_cliquees)==0 :
        vignettes_cliquees.append(vignetteSel[0])
    if len(vignettes_cliquees)==1 :
        if vignettes_cliquees[0] != vignetteSel[0]:
            vignettes_cliquees.append(vignetteSel[0])
    if len(vignettes_cliquees)==2 :
        print('les items des vignettes cliquees sont : ', vignettes_cliquees)
        canvas.after(200,affichage_permutation)


def affichage_permutation():
    global vignettes_cliquees, listephoto
    canvas.itemconfigure(vignettes_cliquees[0], image=listephoto[vignettes_cliquees[1]-1])
    canvas.itemconfigure(vignettes_cliquees[1], image=listephoto[vignettes_cliquees[0]-1])
    temporaire=listephoto[vignettes_cliquees[0]-1]
    listephoto[vignettes_cliquees[0]-1]=listephoto[vignettes_cliquees[1]-1]
    listephoto[vignettes_cliquees[1]-1]=temporaire
    del vignettes_cliquees[:]

def reinit_puzzle(ligne, colonne, listephoto, largeur_vignette, hauteur_vignette):
    global canvas

    for widgets in frame.winfo_children():
      widgets.destroy()

    canvas.destroy()
    canvas = Canvas(fen, width=colonne*largeur_vignette, height=ligne*hauteur_vignette, bg='yellow')
    canvas.pack(side = TOP, padx = 0, pady = 0)
    k=0
    for i in range(ligne):
        for j in range(colonne):
            canvas.create_image((j)*largeur_vignette, (i)*hauteur_vignette, anchor='nw', image = listephoto[k])
            k=k+1
            print('valeur de k = ',k)
    canvas.bind("<Button-1>", gestion_cliques)


def charge_donnees_puzzle_2x3():
    global listephoto, photorien, partie_en_cours
    partie_en_cours = '2x3'
    del listephoto[:]
    ligne, colonne = 2,3
    photorien = PhotoImage(file='chien0x0_rien.gif')
    photo1x1 = PhotoImage(file='chien1x1.gif')
    photo1x2 = PhotoImage(file='chien1x2.gif')
    photo1x3 = PhotoImage(file='chien1x3.gif')
    photo2x1 = PhotoImage(file='chien2x1.gif')
    photo2x2 = PhotoImage(file='chien2x2.gif')
    photo2x3 = PhotoImage(file='chien2x3.gif')
    listephoto = [photo1x1,photo1x2,photo1x3,photo2x1,photo2x2,photo2x3]
    shuffle(listephoto)
    vignette = Image.open('chien1x1.gif')
    largeur_vignette, hauteur_vignette = vignette.size
    reinit_puzzle(ligne, colonne, listephoto, largeur_vignette, hauteur_vignette)

def charge_donnees_puzzle_3x4():
    global listephoto, photorien, partie_en_cours
    partie_en_cours = '3x4'
    del listephoto[:]
    ligne, colonne = 3,4
    photorien = PhotoImage(file='0x0_rien.gif')
    photo1x1 = PhotoImage(file='1x1.gif')
    photo1x2 = PhotoImage(file='1x2.gif')
    photo1x3 = PhotoImage(file='1x3.gif')
    photo1x4 = PhotoImage(file='1x4.gif')
    photo2x1 = PhotoImage(file='2x1.gif')
    photo2x2 = PhotoImage(file='2x2.gif')
    photo2x3 = PhotoImage(file='2x3.gif')
    photo2x4 = PhotoImage(file='2x4.gif')
    photo3x1 = PhotoImage(file='3x1.gif')
    photo3x2 = PhotoImage(file='3x2.gif')
    photo3x3 = PhotoImage(file='3x3.gif')
    photo3x4 = PhotoImage(file='3x4.gif')
    listephoto = [photo1x1,photo1x2,photo1x3,photo1x4,photo2x1,photo2x2,photo2x3,photo2x4,photo3x1,photo3x2,photo3x3,photo3x4]
    shuffle(listephoto)
    vignette = Image.open('1x1.gif')
    largeur_vignette, hauteur_vignette = vignette.size
    reinit_puzzle(ligne, colonne, listephoto, largeur_vignette, hauteur_vignette)

def charge_donnees_puzzle_3x4_2():
    global listephoto, photorien, partie_en_cours
    partie_en_cours = '3x4_2'
    del listephoto[:]
    ligne, colonne = 3,4
    photorien = PhotoImage(file='velo_rien.gif')
    photo1x1 = PhotoImage(file='velo1x1.gif')
    photo1x2 = PhotoImage(file='velo1x2.gif')
    photo1x3 = PhotoImage(file='velo1x3.gif')
    photo1x4 = PhotoImage(file='velo1x4.gif')
    photo2x1 = PhotoImage(file='velo2x1.gif')
    photo2x2 = PhotoImage(file='velo2x2.gif')
    photo2x3 = PhotoImage(file='velo2x3.gif')
    photo2x4 = PhotoImage(file='velo2x4.gif')
    photo3x1 = PhotoImage(file='velo3x1.gif')
    photo3x2 = PhotoImage(file='velo3x2.gif')
    photo3x3 = PhotoImage(file='velo3x3.gif')
    photo3x4 = PhotoImage(file='velo3x4.gif')
    listephoto = [photo1x1,photo1x2,photo1x3,photo1x4,photo2x1,photo2x2,photo2x3,photo2x4,photo3x1,photo3x2,photo3x3,photo3x4]
    shuffle(listephoto)
    vignette = Image.open('velo1x1.gif')
    largeur_vignette, hauteur_vignette = vignette.size
    reinit_puzzle(ligne, colonne, listephoto, largeur_vignette, hauteur_vignette)


def charge_donnees_puzzle_3x6():
    global listephoto, photorien, partie_en_cours
    partie_en_cours = '3x6'
    del listephoto[:]
    ligne, colonne = 3,6
    photorien = PhotoImage(file='bb_yoda_rien.gif')
    photo1x1 = PhotoImage(file='bb_yoda_numero1.gif')
    photo1x2 = PhotoImage(file='bb_yoda_numero2.gif')
    photo1x3 = PhotoImage(file='bb_yoda_numero3.gif')
    photo1x4 = PhotoImage(file='bb_yoda_numero4.gif')
    photo1x5 = PhotoImage(file='bb_yoda_numero5.gif')
    photo1x6 = PhotoImage(file='bb_yoda_numero6.gif')
    photo2x1 = PhotoImage(file='bb_yoda_numero7.gif')
    photo2x2 = PhotoImage(file='bb_yoda_numero8.gif')
    photo2x3 = PhotoImage(file='bb_yoda_numero9.gif')
    photo2x4 = PhotoImage(file='bb_yoda_numero10.gif')
    photo2x5 = PhotoImage(file='bb_yoda_numero11.gif')
    photo2x6 = PhotoImage(file='bb_yoda_numero12.gif')
    photo3x1 = PhotoImage(file='bb_yoda_numero13.gif')
    photo3x2 = PhotoImage(file='bb_yoda_numero14.gif')
    photo3x3 = PhotoImage(file='bb_yoda_numero15.gif')
    photo3x4 = PhotoImage(file='bb_yoda_numero16.gif')
    photo3x5 = PhotoImage(file='bb_yoda_numero17.gif')
    photo3x6 = PhotoImage(file='bb_yoda_numero18.gif')
    listephoto = [photo1x1,photo1x2,photo1x3,photo1x4,photo1x5,photo1x6,photo2x1,photo2x2,photo2x3,photo2x4,photo2x5,photo2x6,photo3x1,photo3x2,photo3x3,photo3x4,photo3x5,photo3x6]
    shuffle(listephoto)
    vignette = Image.open('bb_yoda_numero1.gif')
    largeur_vignette, hauteur_vignette = vignette.size
    reinit_puzzle(ligne, colonne, listephoto, largeur_vignette, hauteur_vignette)

def charge_donnees_puzzle_4x6():
    global listephoto, photorien, partie_en_cours
    partie_en_cours = '4x6'
    del listephoto[:]
    ligne, colonne = 4,6
    photorien = PhotoImage(file='puce_rien.gif')
    photo1x1 = PhotoImage(file='puce1x1.gif')
    photo1x2 = PhotoImage(file='puce1x2.gif')
    photo1x3 = PhotoImage(file='puce1x3.gif')
    photo1x4 = PhotoImage(file='puce1x4.gif')
    photo1x5 = PhotoImage(file='puce1x5.gif')
    photo1x6 = PhotoImage(file='puce1x6.gif')
    photo2x1 = PhotoImage(file='puce2x1.gif')
    photo2x2 = PhotoImage(file='puce2x2.gif')
    photo2x3 = PhotoImage(file='puce2x3.gif')
    photo2x4 = PhotoImage(file='puce2x4.gif')
    photo2x5 = PhotoImage(file='puce2x5.gif')
    photo2x6 = PhotoImage(file='puce2x6.gif')
    photo3x1 = PhotoImage(file='puce3x1.gif')
    photo3x2 = PhotoImage(file='puce3x2.gif')
    photo3x3 = PhotoImage(file='puce3x3.gif')
    photo3x4 = PhotoImage(file='puce3x4.gif')
    photo3x5 = PhotoImage(file='puce3x5.gif')
    photo3x6 = PhotoImage(file='puce3x6.gif')
    photo4x1 = PhotoImage(file='puce4x1.gif')
    photo4x2 = PhotoImage(file='puce4x2.gif')
    photo4x3 = PhotoImage(file='puce4x3.gif')
    photo4x4 = PhotoImage(file='puce4x4.gif')
    photo4x5 = PhotoImage(file='puce4x5.gif')
    photo4x6 = PhotoImage(file='puce4x6.gif')
    listephoto = [photo1x1,photo1x2,photo1x3,photo1x4,photo1x5,photo1x6,photo2x1,photo2x2,photo2x3,photo2x4,photo2x5,photo2x6,photo3x1,photo3x2,photo3x3,photo3x4,photo3x5,photo3x6,photo4x1,photo4x2,photo4x3,photo4x4,photo4x5,photo4x6]
    shuffle(listephoto)
    vignette = Image.open('puce1x1.gif')
    largeur_vignette, hauteur_vignette = vignette.size
    reinit_puzzle(ligne, colonne, listephoto, largeur_vignette, hauteur_vignette)


def relance_partie():
    global partie_en_cours
    if partie_en_cours == '2x3':
        charge_donnees_puzzle_2x3()
    if partie_en_cours == '3x4':
        charge_donnees_puzzle_3x4()
    if partie_en_cours == '3x4_2':
        charge_donnees_puzzle_3x4_2()
    if partie_en_cours == '3x6':
        charge_donnees_puzzle_3x6()
    elif partie_en_cours == '4x6':
        charge_donnees_puzzle_4x6()

#-------------------------------------

def creer_menus(fen):
    top = Menu(fen)
    fen.config(menu=top)

    jeu = Menu(top, tearoff=False)
    top.add_cascade(label='Cliquez ici pour choisir votre jeu', menu=jeu)
    jeu.add_command(label='Nouvelle partie', command = relance_partie)

    submenu=Menu(jeu, tearoff=False)
    jeu.add_cascade(label='Dimensions', menu=submenu)
    submenu.add_command(label='2 x 3', command = charge_donnees_puzzle_2x3)
    submenu.add_command(label='3 x 4', command = charge_donnees_puzzle_3x4)
    submenu.add_command(label='3 x 4_2', command = charge_donnees_puzzle_3x4_2)
    submenu.add_command(label='3 x 6', command = charge_donnees_puzzle_3x6)
    submenu.add_command(label='4 x 6', command = charge_donnees_puzzle_4x6)

    submenu_games_choice=Menu(jeu, tearoff=False)
    jeu.add_cascade(label='Jeux', menu=submenu_games_choice)
    submenu_games_choice.add_command(label='PPC', command = PPC)
    submenu_games_choice.add_command(label='Memory', command = Memory)

    jeu.add_command(label='Quitter', command=fen.destroy)

def main():
    global fen

    fen = Tk()
    fen.title("Jeux")
    photorien = PhotoImage(file='chien0x0_rien.gif')

    global canvas
    canvas = Canvas(width = 900, height = 675, bg = 'white')
    canvas.pack(expand = YES, fill = BOTH)

    image = ImageTk.PhotoImage(file = "./menu.jpg")
    canvas.create_image(0, 0, image = image, anchor = NW)
    canvas.pack(side = TOP, padx = 0, pady = 0)


    global frame
    frame = Frame(fen)

    creer_menus(fen)

    fen.mainloop()

main()



