from tkinter import *
from random import randint, shuffle


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
    nombre_vignettes = nombre_colonnes * nombre_lignes
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

fenetre.mainloop()
