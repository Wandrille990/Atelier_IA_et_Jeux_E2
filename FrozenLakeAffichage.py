import tkinter as tk
import random
from random import randint
import numpy as np
import copy
import time
import math

# voici les 4 touches utilisées pour les déplacements  gauche/haut/droite/bas

Keys =  ['q','z','d','s']

#################################################################################
#
#   Données de partie
#
#################################################################################


Data = [   [0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,1,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,1,0,0],
           [0,0,0,1,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,1,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,1,0,0,0,0,0,1,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,1,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,1,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,1,0,0,0,0,0,0],
           [0,1,0,0,0,0,0,0,0,0,0,8,8],
           [0,0,0,0,0,0,0,0,0,1,0,8,8]]

# Data = [   [0,0,0,0,0,0,0,0,0,0,0,0,0],
#            [0,0,0,0,0,0,0,0,0,0,0,0,0],
#            [0,0,0,0,0,0,1,0,0,0,0,0,0],
#            [0,0,0,0,0,0,0,0,0,0,1,0,0],
#            [0,0,0,0,0,0,0,0,0,0,0,0,0],
#            [0,0,0,0,0,0,0,0,0,0,0,0,0],
#            [0,0,0,0,0,0,0,0,0,1,0,0,0],
#            [0,0,0,0,0,0,0,0,0,0,0,0,0],
#            [0,1,0,0,0,0,0,0,0,0,0,0,0],
#            [0,0,0,0,0,0,0,0,0,0,0,0,0],
#            [0,0,0,0,0,0,0,0,0,0,0,0,0],
#            [0,0,1,0,0,0,0,0,0,0,0,0,0],
#            [0,0,0,0,0,0,0,0,0,0,0,0,0],
#            [0,0,0,0,0,0,0,0,0,0,0,0,0],
#            [0,0,0,0,0,0,1,0,0,0,8,8,8],
#            [0,1,0,0,0,0,0,0,0,0,8,8,8],
#            [0,0,0,0,0,0,0,0,0,0,8,8,8]]


GInit  = np.array(Data,dtype=np.int8)
GInit  = np.flip(GInit,0).transpose()

LARGEUR = 13
HAUTEUR = 17


#################################################################################
#
#   création de la fenetre principale  - NE PAS TOUCHER
#
#################################################################################


L = 20  # largeur d'une case du jeu en pixel
largeurPix = LARGEUR * L
hauteurPix = (HAUTEUR+1) * L


Window = tk.Tk()
Window.geometry(str(largeurPix)+"x"+str(hauteurPix+3))   # taille de la fenetre
Window.title("Frozen Lake")

# gestion du clavier

LastKey = '0'


def keydown(e):
    global LastKey
    if hasattr(e,'char') and e.char in Keys:
        LastKey = e.char


# création de la frame principale stockant toutes les pages

F = tk.Frame(Window)
F.bind("<KeyPress>", keydown)
F.pack(side="top", fill="both", expand=True)
F.grid_rowconfigure(0, weight=1)
F.grid_columnconfigure(0, weight=1)
F.focus_set()

# gestion des pages

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

canvas = tk.Canvas(Frame0,width = largeurPix, height = hauteurPix, bg ="black" )
canvas.place(x=0,y=0)

#   Dessine la grille de jeu - ne pas toucher


def Affiche(Game):
    canvas.delete("all")
    H = canvas.winfo_height()-2

    def MSG(coul,txt):

        canvas.create_rectangle(0,0,largeurPix,20,fill="black")
        canvas.create_text(largeurPix//2, 10,  font='Helvetica 12 bold', fill=coul, text=txt )

    def DrawCase(x,y,coul):
        x *= L
        y *= L
        canvas.create_rectangle(x,H-y,x+L,H-y-L,fill=coul)

    # dessin du décors

    for x in range (LARGEUR):
       for y in range (HAUTEUR):
           if Game.Grille[x,y] == 0  : DrawCase(x,y,"cyan" )
           if Game.Grille[x,y] == 1  : DrawCase(x,y,"blue" )
           if Game.Grille[x,y] == 8  : DrawCase(x,y,"pink" )

    DrawCase(Game.PlayerPos[0],Game.PlayerPos[1],"yellow" )

    MSG("yellow",str(Game.Score))

################################################################################
#
#                          Gestionnaire de partie
#
################################################################################


class Game:

    def __init__(self):
        self.Grille = GInit
        self.Score = 0
        self.Reset()


    def Reset(self):
        self.PlayerPos = [0,HAUTEUR-1]
        return self.PlayerPos[1]*13+self.PlayerPos[0]

    def is_finished(self):# fin de la partie quand l'agent va sur la valeur -1
        xP,yP = self.PlayerPos
        return self.Grille[xP][yP] == 1 or self.Grille[xP][yP] == 8



    def Doo(self, action):
        #  annulation des déplacements vers un mur
        if self.PlayerPos[0] == 0          and action == 0:  return self.PlayerPos[1]*13+self.PlayerPos[0], -10
        if self.PlayerPos[0] == LARGEUR-1  and action == 2:  return self.PlayerPos[1]*13+self.PlayerPos[0], -10

        if self.PlayerPos[1] == 0          and action == 3:  return self.PlayerPos[1]*13+self.PlayerPos[0], -10
        if self.PlayerPos[1] == HAUTEUR-1  and action == 1:  return self.PlayerPos[1]*13+self.PlayerPos[0], -10


        # 0: left, 2: up, 4: right, 6: down
        P = [ 0 ] * 8
        v = 200
        P[(action * 2 - 1) % 8] = v
        P[ action * 2         ] = v
        P[(action * 2 + 1) % 8] = v
        #print("P : {}".format(P))


        # plus on se rapproche de l'objectif, plus ca glisse
        for i in range(8) : P[i] += LARGEUR-self.PlayerPos[0] + (HAUTEUR-self.PlayerPos[1])
        #print("P : {}".format(P))

        # gestion des murs
        if self.PlayerPos[0] == 0 :           P[7] = P[0] = P[1] = 0 # mur gauche
        if self.PlayerPos[0] == LARGEUR-1 :   P[3] = P[4] = P[5] = 0 # mur droit

        if self.PlayerPos[1] == 0 :           P[5] = P[6] = P[7] = 0 # mur bas
        if self.PlayerPos[1] == HAUTEUR-1 :   P[1] = P[2] = P[3] = 0 # mur haut

        #tirage aléa
        totProb = sum(P)
        rd = random.randrange(0,totProb)+1

        choix = 0
        while P[choix] < rd :
            rd -= P[choix]
            choix += 1
        #print("rd : {}".format(rd))
        #print("choix : {}".format(choix))

        #traduction 0-7 => déplacement
        if choix in [7,0,1] : self.PlayerPos[0] -= 1
        if choix in [3,4,5] : self.PlayerPos[0] += 1
        if choix in [1,2,3] : self.PlayerPos[1] += 1
        if choix in [5,6,7] : self.PlayerPos[1] -= 1

        # gestion des collisions

        xP,yP = self.PlayerPos
        if self.Grille[xP][yP] == 1 :   # DEAD
            #self.Reset()
            return self.PlayerPos[1]*13+self.PlayerPos[0], -100

        if self.Grille[xP][yP] == 8 :   # WIN
            #self.Reset()
            return self.PlayerPos[1]*13+self.PlayerPos[0], 100

        return self.PlayerPos[1]*13+self.PlayerPos[0]   , 0


    def Do(self,action):
        reward = self.Doo(action)
        self.Score += reward
        return reward


###########################################################
#
#   découvrez le jeu en jouant au clavier
#
###########################################################

#G = Game()

def JeuClavier():
    F.focus_force()

    global LastKey

    r = 0 # reward
    if LastKey != '0' :
        if LastKey == Keys[0] : G.Do(0)
        if LastKey == Keys[1] : G.Do(1)
        if LastKey == Keys[2] : G.Do(2)
        if LastKey == Keys[3] : G.Do(3)

    Affiche(G)
    LastKey = '0'
    Window.after(500,JeuClavier)


###########################################################
#
#  simulateur de partie aléatoire
#
###########################################################

def SimulGame():   # il n y a pas de notion de "fin de partie"
    G = Game()
    reward = 0
    for i in range(100):
       action = random.randrange(0,4)
       reward += G.Do(action)
    return reward


###########################################################
#
#  Q-learning
#
###########################################################


def take_action(spt, Q, eps):

    if random.uniform(0, 1) < eps:  # Action aléatoire ?
        action = randint(0, 3)
    else:  # Action qui maximise l'espérance
        if np.argmax(Q[spt]) == 0:  # Si elle est nulle, on favorise l'exploration dans un état peu connu
            action = randint(0, 3)
        else:
            softmax = []
            for i in range(4):
                softmax.append(math.exp(Q[spt][i])/
                (math.exp(Q[spt][0]) + math.exp(Q[spt][1]) + math.exp(Q[spt][2]) + math.exp(Q[spt][3])))
            #print(softmax)
            #time.sleep(0.3)
            action = np.random.choice(np.arange(0, 4), p=softmax)
            #action = np.argmax(Q[spt])
    return action  # return at


def JustePourQueLaffichageMarche():
    global G, spt, Q, epsilon, rep, nb, go

    if nb <= rep:
        at = take_action(spt, Q, epsilon)

        sptp1, r = G.Doo(at)
        #F.focus_force()
        #Affiche(G)

        # Update Q function
        atp1 = take_action(sptp1, Q, 0.0)
        Q[spt][at] = Q[spt][at] + 0.1*(r + 0.9*Q[sptp1][atp1] - Q[spt][at])
        # 0.1 : learning rate  /  0.9 : gamma (moins d'importance aux actions lointaines)

        spt = sptp1  # mise à jour de l'état

        if nb > rep - 101:
            F.focus_force()
            Affiche(G)
            G.Score += r


    if G.is_finished():
        #if G.Grille[G.PlayerPos[0]][G.PlayerPos[1]] == 8:
        #    print("WIN")
        #print("{} = {}".format("Epsilon", epsilon))

        if (nb) % 1000 == 0 or nb > rep-2:
            print("{} sur {}".format(nb, rep))  # avancement de l'entraînement
            print("{} = {}".format("Epsilon", epsilon))  # évolution d'epsilon
            if nb == rep:
                for i in range(LARGEUR*HAUTEUR-13, -1, -13):
                    aff = Q[i:i+13]
                    print(aff)

        #epsilon = max(epsilon * (1 - 1 / (rep / 3)), 0.01)
        # Décroissant logarithmiquement, plus lent mais meilleur score
        epsilon = max(epsilon - (1 / (rep/1.1)), 0.01)
        # Décroissant linéairement, plus rapide mais légèrement moins bon score
        # Rapport score/temps meilleurs avec une décroissance linéaire

        G.Reset()
        nb += 1

        if nb == rep - 100:
            test = str(input("Lancer l'exploitation ? : "))
            if(test != None):
                go = True

    if go:
        Window.after(50,JustePourQueLaffichageMarche)
    else:
        Window.after(1,JustePourQueLaffichageMarche)


#####################################################################################
#
#  Mise en place de l'interface - ne pas toucher

G = Game()

rep = 10000  # nombre de parties d'entraînement (10 000 conseillé même si plus long)
nb = 0
epsilon = 1  # probabilité que l'agent prenne une action aléatoirement
go = False

Q = [[0, 0, 0, 0] for y in range(LARGEUR*HAUTEUR+1)]
#for i in range(LARGEUR*HAUTEUR-13, -1, -13):
#    aff = Q[i:i+13]
#    print(aff)

spt = G.Reset()

AfficherPage(0)

#Window.after(500,JeuClavier)
#Window.after(500,SimulGame)
Window.after(1, JustePourQueLaffichageMarche)
Window.mainloop()













# Data = [   [0,0,0,0,0,0,0,0,0,0,0,0,0],
#            [0,0,0,0,0,0,0,0,0,0,0,0,0],
#            [0,0,0,0,0,0,1,0,0,0,0,0,0],
#            [0,0,0,0,0,0,0,0,0,0,1,0,0],
#            [0,0,0,0,0,0,0,0,0,0,0,0,0],
#            [0,0,0,0,0,0,0,0,0,0,0,0,0],
#            [0,0,0,0,0,0,0,0,0,1,0,0,0],
#            [0,0,0,0,0,0,0,0,0,0,0,0,0],
#            [0,1,0,0,0,0,0,0,0,0,0,0,0],
#            [0,0,0,0,0,0,0,0,0,0,0,0,0],
#            [0,0,0,0,0,0,0,0,0,0,0,0,0],
#            [0,0,1,0,0,0,0,0,0,0,0,0,0],
#            [0,0,0,0,0,0,0,0,0,0,0,0,0],
#            [0,0,0,0,0,0,0,0,0,0,0,0,0],
#            [0,0,0,0,0,0,1,0,0,0,8,8,8],
#            [0,1,0,0,0,0,0,0,0,0,8,8,8],
#            [0,0,0,0,0,0,0,0,0,0,8,8,8]]
#
#
# LARGEUR = 13
# HAUTEUR = 17
#
# #GInit  = np.array(Data)
# #GInit  = np.flip(GInit,0).transpose()
#
# Q = [[y, y, y, y] for y in range(LARGEUR*HAUTEUR)]
#
# print("-")
# print(Q)
# print("-")
#
# print("")
#
# #for y in range(HAUTEUR):
# #  print("")
# #  for x in range(LARGEUR):
# #    print("Q[{}] = {}".format(y*13+x, Data[y][x]))
#
#
# #for i in range(LARGEUR):
# #  aff = Q[i::17]
# #  print(aff)
#
# for i in range(LARGEUR*HAUTEUR-13, -1, -13):
#   aff = Q[i:i+13]
#   print(aff)
#
# print("oui")

