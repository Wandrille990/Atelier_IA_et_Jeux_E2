import tkinter as tk
from tkinter import messagebox
import random
import numpy as np
import time 

###############################################################################
# création de la fenetre principale  - ne pas toucher

LARG = 300
HAUT = 300

Window = tk.Tk()
Window.geometry(str(LARG)+"x"+str(HAUT))   # taille de la fenetre
Window.title("ESIEE - Morpion")


# création de la frame principale stockant toutes les pages

F = tk.Frame(Window)
F.pack(side="top", fill="both", expand=True)
F.grid_rowconfigure(0, weight=1)
F.grid_columnconfigure(0, weight=1)

# gestion des différentes pages

ListePages  = {}
PageActive = 0

def CreerUnePage(id):
    Frame = tk.Frame(F)
    ListePages[id] = Frame
    Frame.grid(row=0, column=0, sticky="nsew")
    return Frame

def AfficherPage(id):
    global PageActive
    PageActive = id
    ListePages[id].tkraise()
    
Frame0 = CreerUnePage(0)

canvas = tk.Canvas(Frame0,width = LARG, height = HAUT, bg ="black" )
canvas.place(x=0,y=0)


#################################################################################
#
#  Parametres du jeu
 
Grille = [ [0,0,0], 
           [0,0,0], 
           [0,0,0] ]  # attention les lignes représentent les colonnes de la grille
           
Grille = np.array(Grille)
Grille = Grille.transpose()  # pour avoir x,y
           
winner = 0
Score = [0, 0, 0]

PartieGagnee = False
Relance = False 


###############################################################################

# gestion du joueur humain et de l'IA


def Partiefinie():
    for i in range(1, 3):
        for x in range(3):
            if(Grille[x][0] == i and Grille[x][1] == i and Grille[x][2] == i):
                return i
            if(Grille[0][x] == i and Grille[1][x] == i and Grille[2][x] == i):
                return i
                
        if(Grille[0][0] == i and Grille[1][1] == i and Grille[2][2] == i):
            return i
        if(Grille[2][0] == i and Grille[1][1] == i and Grille[0][2] == i):
            return i
    
    nbCoup = 0
    for x in range(3):
        for y in range(3):
            if(Grille[x][y] != 0):
                nbCoup += 1
    if(nbCoup >= 9): return 3
            
    return 0
        
    
def FinPartie(winner):
    global Score, PartieGagnee
    
    Score[winner-1] += 1
    print(Score)
    PartieGagnee = True


def IA():
    global Grille
    
    coupPossibles = CoupPossible()
    
    print(coupPossibles)
    print(len(coupPossibles))
    if(len(coupPossibles) != 0):
        coup = coupPossibles[random.randint(0, len(coupPossibles)-1)]
        Grille[coup[0]][coup[1]] = 2
    else: return
    
def CoupIA():
    global Grille
    
    Resultat = JoueurSimuleIA()
    coup = Resultat[1]
    Grille[coup[0]][coup[1]] = 2

def CoupPossible():
    global Grille
    
    coupPossibles = []
    
    for x in range(3):
        for y in range(3):
            if(Grille[x][y] == 0):
                coupPossibles.append((x, y))
    return coupPossibles


def JoueurSimuleIA():
    global Grille, winner
    
    winner = Partiefinie()
    if(winner != 0):
        return winner, None
    
    coupPossibles = CoupPossible()
    
    Resultats = []
    
    precedent_winner = 1
    for coup in coupPossibles:
        Grille[coup[0]][coup[1]] = 2
        R =  JoueurSimuleHumain()
        
        if(precedent_winner == 1):
            precedent_winner = R[0]
            Resultats.append((precedent_winner, coup))
        elif(precedent_winner == 3):
            if(R[0] == 2):
                precedent_winner = R[0]
                Resultats.append((precedent_winner, coup))
            
        Grille[coup[0]][coup[1]] = 0
    return Resultats[-1]


def JoueurSimuleHumain():
    global Grille, winner
    
    winner = Partiefinie()
    if(winner != 0):
        return winner, None
    
    coupPossibles = CoupPossible()
    
    Resultats = []
    precedent_winner = 2
    for coup in coupPossibles:
        Grille[coup[0]][coup[1]] = 1
        R =  JoueurSimuleIA()
        
        if(precedent_winner == 2):
            precedent_winner = R[0]
            Resultats.append((precedent_winner, coup))
        elif(precedent_winner == 3):
            if(R[0] == 1):
                precedent_winner = R[0]
                Resultats.append((precedent_winner, coup))
        Grille[coup[0]][coup[1]] = 0
    return Resultats[-1]

    
################################################################################
#    
# Dessine la grille de jeu

def Dessine(PartieGagnee = False, winner = 0):
        ## DOC canvas : http://tkinter.fdex.eu/doc/caw.html
        canvas.delete("all")
        
        if(not PartieGagnee):
            for i in range(4):
                canvas.create_line(i*100,0,i*100,300,fill="blue", width="4" )
                canvas.create_line(0,i*100,300,i*100,fill="blue", width="4" )
        if(PartieGagnee):
            if(winner == 1):
                for i in range(4):
                    canvas.create_line(i*100,0,i*100,300,fill="red", width="4" )
                    canvas.create_line(0,i*100,300,i*100,fill="red", width="4" )
            if(winner == 2):
                for i in range(4):
                    canvas.create_line(i*100,0,i*100,300,fill="yellow", width="4" )
                    canvas.create_line(0,i*100,300,i*100,fill="yellow", width="4" )
            if(winner == 3):
                for i in range(4):
                    canvas.create_line(i*100,0,i*100,300,fill="white", width="4" )
                    canvas.create_line(0,i*100,300,i*100,fill="white", width="4" )
        
        for x in range(3):
            for y in range(3):
                xc = x * 100 
                yc = y * 100 
                if ( Grille[x][y] == 1):
                    canvas.create_line(xc+10,yc+10,xc+90,yc+90,fill="red", width="4" )
                    canvas.create_line(xc+90,yc+10,xc+10,yc+90,fill="red", width="4" )
                if ( Grille[x][y] == 2):
                    canvas.create_oval(xc+10,yc+10,xc+90,yc+90,outline="yellow", width="4" )
                    
  
####################################################################################
#
#  fnt appelée par un clic souris sur la zone de dessin

def MouseClick(event):
    global PartieGagnee, winner, Grille, Score
    
    if(PartieGagnee):
        Grille = [[0 for i in range(3)] for j in range(3)]
        Dessine(PartieGagnee, winner)
        PartieGagnee = False
        return
    
    Window.focus_set()
    x = event.x // 100  # convertit une coordonée pixel écran en coord grille de jeu
    y = event.y // 100
    if ( (x<0) or (x>2) or (y<0) or (y>2) ) : return
    
    
    print("clicked at", x,y)
    
    if(Grille[x][y] != 0):
        return
    Grille[x][y] = 1
    winner = Partiefinie()
    Dessine(PartieGagnee, winner)
    
    winner = Partiefinie()
    if(winner != 0):
        FinPartie(winner)
    else:
        CoupIA()
        
        winner = Partiefinie()
        Dessine(PartieGagnee, winner)
        if(winner != 0):
            FinPartie(winner)
    
    Dessine(PartieGagnee, winner)
    
    
canvas.bind('<ButtonPress-1>',    MouseClick)

#####################################################################################
#
#  Mise en place de l'interface - ne pas toucher

AfficherPage(0)
Dessine()
Window.mainloop()
