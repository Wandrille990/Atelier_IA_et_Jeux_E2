import tkinter as tk
import random
import numpy as np
import copy
import random
import time

#################################################################################
#
#   Données de partie

Data = [   [1,1,1,1,1,1,1,1,1,1,1,1,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,2,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,3,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,1,1,1,1,1,1,1,1,1,1,1,1] ]

GInit  = np.array(Data,dtype=np.int8)
GInit  = np.flip(GInit,0).transpose()

LARGEUR = 13
HAUTEUR = 17

# container pour passer efficacement toutes les données de la partie

class Game:
    def __init__(self, Grille, PlayerX, PlayerY, Score=0):
        self.PlayerX = PlayerX
        self.PlayerY = PlayerY
        self.Score   = Score
        self.Grille  = Grille

    def copy(self):
        return copy.deepcopy(self)

GameInit = Game(GInit,3,5)

##############################################################
#
#   création de la fenetre principale  - NE PAS TOUCHER

L = 20  # largeur d'une case du jeu en pixel
largeurPix = LARGEUR * L
hauteurPix = HAUTEUR * L


Window = tk.Tk()
Window.geometry(str(largeurPix)+"x"+str(hauteurPix))   # taille de la fenetre
Window.title("TRON")


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

canvas = tk.Canvas(Frame0,width = largeurPix, height = hauteurPix, bg ="black" )
canvas.place(x=0,y=0)

#   Dessine la grille de jeu - ne pas toucher


def Affiche(Game):
    canvas.delete("all")
    H = canvas.winfo_height()

    def DrawCase(x,y,coul):
        x *= L
        y *= L
        canvas.create_rectangle(x,H-y,x+L,H-y-L,fill=coul)

    # dessin des murs

    for x in range (LARGEUR):
       for y in range (HAUTEUR):
           if Game.Grille[x,y] == 1  : DrawCase(x,y,"gray" )
           if Game.Grille[x,y] == 2  : DrawCase(x,y,"cyan" )


    # dessin de la moto
    DrawCase(Game.PlayerX,Game.PlayerY,"red" )

def AfficheScore(Game):
   info = "SCORE : " + str(Game.Score)
   canvas.create_text(80, 13,   font='Helvetica 12 bold', fill="yellow", text=info)


###########################################################
#
# gestion du joueur IA

# VOTRE CODE ICI

# Liste des directions :
# 0 : sur place   1: à gauche  2 : en haut   3: à droite    4: en bas

dx = np.array([0, -1, 0,  1,  0],dtype=np.int32)
dy = np.array([0,  0, 1,  0, -1],dtype=np.int32)

# scores associés à chaque déplacement
ds = np.array([0,  1,  1,  1,  1],dtype=np.int32)

Debug = False
nb = 100 # nb de parties


def Play(Game):

    x,y = Game.PlayerX, Game.PlayerY
    print(x,y)

    Game.Grille[x,y] = 2  # laisse la trace de la moto

    dep = MeilleurCoup(Game)
    if(dep == None): return True

    #dep = DeplacementPossible(Game)
    #choix = random.randrange(len(dep))
    x += dep[0]
    y += dep[1]

    v = Game.Grille[x,y]

    if v > 0 :
        # collision détectée
        return True # partie terminée
    else :
       Game.PlayerX = x  # valide le déplacement
       Game.PlayerY = y  # valide le déplacement
       Game.Score += 1
       return False   # la partie continue

def Teleportation():
    x,y = Game.PlayerX, Game.PlayerY

    if(Game.Grille[x][y] == 2): Game.PlayerX =


def DeplacementPossible(Game):
    x,y = Game.PlayerX, Game.PlayerY
    dep = []

    if (Game.Grille[x  ][y-1] == 0): dep.append((0,-1))
    if (Game.Grille[x  ][y+1] == 0): dep.append((0, 1))
    if (Game.Grille[x+1][y  ] == 0): dep.append(( 1,0))
    if (Game.Grille[x-1][y  ] == 0): dep.append((-1,0))
    return dep

def SimulationPartie(Game, nb):

    # on copie les datas de départ pour créer plusieurs parties en //
    G      = np.tile(Game.Grille,(nb,1,1))
    X      = np.tile(Game.PlayerX,nb)
    Y      = np.tile(Game.PlayerY,nb)
    S      = np.tile(Game.Score,nb)
    I      = np.arange(nb)  # 0,1,2,3,4,5...

    boucle = True

    while(boucle) :
        if Debug :print("X : ",X)
        if Debug :print("Y : ",Y)
        if Debug :print("S : ",S)

        # marque le passage de la moto
        G[I, X, Y] = 2


        LPossibles =  np.zeros((nb,4),dtype=np.int32)
        Tailles = np.zeros(nb,dtype=np.int32)

        Vgauche = (G[I, X-1, Y] == 0) * 1
        Vhaut   = (G[I, X, Y+1] == 0) * 1
        Vdroite = (G[I, X+1, Y] == 0) * 1
        Vbas    = (G[I, X, Y-1] == 0) * 1

        if Debug :print(Vgauche)
        if Debug :print(Vhaut)
        if Debug :print(Vdroite)
        if Debug :print(Vbas)

        LPossibles[I, Tailles] = Vgauche*1
        Tailles += Vgauche

        LPossibles[I, Tailles] = Vhaut*2
        Tailles += Vhaut

        LPossibles[I, Tailles] = Vdroite*3
        Tailles += Vdroite

        LPossibles[I, Tailles] = Vbas*4
        Tailles += Vbas

        Tailles[Tailles == 0] = 1

        if Debug :print(Tailles)
        if Debug :print(LPossibles)

        R = LPossibles[I, np.random.randint(Tailles)]
        if Debug :print(R)


        #DEPLACEMENT
        DX = dx[R]
        DY = dy[R]
        if Debug : print("DX : ", DX)
        if Debug : print("DY : ", DY)
        X += DX
        Y += DY
        S += ds[R]

        if(np.sum(R) == 0): boucle = False
    return np.mean(S)

def MonteCarlo(G, nombreParties):
    Game2 = G.copy()
    Total = SimulationPartie(Game2, nombreParties)
    return Total

def MeilleurCoup(Game):
    result = []

    dep = DeplacementPossible(Game)
    #print(dep)

    for i in range(len(dep)):
        Game2=Game.copy()
        Game2.PlayerX += dep[i][0]
        Game2.PlayerY += dep[i][1]
        result.append(MonteCarlo(Game2,1000))
    if(len(dep) == 0):
        print("Score : {}".format(Game.Score))
        return None
    else:
        #print(dep[result.index(max(result))])
        return dep[result.index(max(result))]

################################################################################

CurrentGame = GameInit.copy()


def Partie():

        Tstart = time.time()
        PartieTermine = Play(CurrentGame)

        if not PartieTermine :
            print(time.time() - Tstart)
            Affiche(CurrentGame)
            # rappelle la fonction Partie() dans 30ms
            # entre temps laisse l'OS réafficher l'interface
            Window.after(100,Partie)
        else :
            AfficheScore(CurrentGame)


#####################################################################################
#
#  Mise en place de l'interface - ne pas toucher

AfficherPage(0)
Window.after(100,Partie)
Window.mainloop()








