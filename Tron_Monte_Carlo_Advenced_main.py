import tkinter as tk
from tkinter import *
import numpy as np
import copy
import time
from scipy import signal
from math import dist
from win32api import GetSystemMetrics
from tron_advenced_maps import choose_level

################################################################################

PROFONDEUR = 3                                # maps avec 3 étages

COMPARE = np.ones((5,5), dtype=np.int32)      # Grille de comparaison pour detection de bloc dans un radius de 5x5
DIST_SPAWN = 3                                # Constante pour gérer la distance entre entité pour le spawn


class Game:
    def __init__(self, Grille, X, Y, Z, Nb_Entity, Nb_Iterations):
        self.X = X
        self.Y = Y
        self.Z = Z
        self.Grille        = Grille
        self.Nb_Entity     = Nb_Entity
        self.Entity_Fini   = np.zeros(Nb_Entity)
        self.Score         = np.ones(Nb_Entity)
        self.Nb_Iterations = Nb_Iterations


    def copy(self):
        return copy.deepcopy(self)

# Fonction d'instanciation des valeurs du jeu. Utile pour relancer le jeu après une défaite.
def InstanciePartie(nb_iterations, Map, nbr_spawn):
    global LARGEUR, HAUTEUR, dir_humain, CurrentGame, pos_tp, canvas, CleanTP

    level = choose_level(Map-15)
    HAUTEUR = level[1]
    LARGEUR = level[2]

    Data = level[0]
    GInit  = np.array(Data,dtype=np.int8)
    GInit  = np.array([np.flip(GInit[0],0).transpose(), np.flip(GInit[1],0).transpose(), np.flip(GInit[2],0).transpose()])

    convolve = signal.convolve2d(GInit[1], COMPARE, mode='same')
    coords_spawn_rand = spawner(nbr_spawn, convolve)

    X = [X[0] for X in coords_spawn_rand]
    Y = [Y[1] for Y in coords_spawn_rand]
    Z = [1 for i in range(nbr_spawn)]

    dir_humain = 2

    GameInit = Game(GInit, X, Y, Z, nbr_spawn, nb_iterations)
    CurrentGame = GameInit.copy()

    pos_tp = []
    InitTP(CurrentGame.Grille, level)

    largeurPix = LARGEUR * PROFONDEUR * L
    hauteurPix = HAUTEUR * L

    Window.geometry(str(largeurPix) + "x" + str(hauteurPix))

    canvas = tk.Canvas(Game_Frame, width = largeurPix, height = hauteurPix, bg ="black" )
    canvas.place(x=0,y=0)

    CleanTP = 1

# Recherche de coordonnés de spawn possible pour le nombre d'entité choisi
def spawner(Nb_Spawn, convolve):
    coords_list = []
    arg = np.argwhere(convolve == 0)
    while len(coords_list) < Nb_Spawn:
        alea = np.random.randint(0, high=len(arg))
        test_x = arg[alea][0]
        test_y = arg[alea][1]

        if (verification_presence(coords_list, test_x, test_y)):
            coords = [test_x, test_y]
            coords_list.append(coords)

    return coords_list

# Vérifie que les coordonnés proposé sont suffisament éloigné d'un autre spawn
def verification_presence(coords_list, test_x, test_y):
    test_coords = [test_x, test_y]
    for coords in coords_list:
        if dist(coords, test_coords) <= DIST_SPAWN:
            return False
    return True

def InitTP(Grille, level): # récupétation de la position des télépoteurs
    for i in range(20, (20 + level[3])):
        pos_tp.append((
            np.where(Grille == i)[1][0],
            np.where(Grille == i)[2][0],
            np.where(Grille == i)[0][0]))

##############################################################

# Variable pour le menu
Game_Window = False
Menu_Window = True
txt_solo = "Mode Solo: Un seul joueur sur une carte avec étage pour faire le maximum de point possible"
txt_vs = "Mode Player VS IA: Faire le choix du nombre d'IA et de leurs nombres de simulations"
txt_royale = "Mode Battle Royale: Un joueur contre une IA immortelle. Le but est de faire le plus de points."

def exit_game(event):
    Window.destroy()

##############################################################
#   création de la fenetre principale  - NE PAS TOUCHER

L = 20  # largeur d'une case du jeu en pixel

Window = tk.Tk()
var_mode = IntVar()
var_ia = IntVar()
Window.title("TRON")

# création de la frame principale stockant toutes les pages

F = tk.Frame(Window)
F.pack(side="top", fill="both", expand=True)
F.grid_rowconfigure(0, weight=1)
F.grid_columnconfigure(0, weight=1)

# gestion des différentes pages
ListePages  = {}

def CreerUnePage(id):
    Frame = tk.Frame(F)
    ListePages[id] = Frame
    Frame.grid(row=0, column=0, sticky="nsew")
    return Frame

def AfficherPage(id):
    ListePages[id].tkraise()

Game_Frame = CreerUnePage(0)

Menu_Frame = CreerUnePage(1)
canvas2 = tk.Canvas(Menu_Frame, width = 1080, height = 480, bg ="black")
canvas2.place(x=0, y=0)

# Taille de la police en fonction des écran, test du 1440p sinon adapté pour du 1080p
if GetSystemMetrics(1) == 1440:
    FONT_10 = 10
    FONT_13 = 15
    FONT_16 = 16
    FONT_22 = 22
    FONT_50 = 60
    FIX_1 = 43
    FIX_2 = 26
    FIX_3 = 10
else:
    FONT_10 = 10
    FONT_13 = 13
    FONT_16 = 16
    FONT_22 = 22
    FONT_50 = 50
    FIX_1 = 55
    FIX_2 = 30
    FIX_3 = 0

#   Dessine le menu
def Affiche_Menu():
    Window.title('MENU')
    Window.geometry(str(1080) + "x" + str(480))
    H = canvas2.winfo_height()
    W = canvas2.winfo_width()
    AfficherPage(1)

    Nbr_spawn = 0

    def get_nbr_spawn():
        global Nbr_spawn
        return Nbr_spawn

    def set_nbr_spawn(n):
        global Nbr_spawn
        Nbr_spawn = n

    def start_game():
        global Menu_Window
        Menu_Window = False
        print("Nombre de simulation par IA : {}".format(w2.get()))
        InstanciePartie(w2.get(), w3.get(), get_nbr_spawn())

    def solo_mode():
        global ModeDeJeu
        set_nbr_spawn(1)
        ModeDeJeu = 0
        start_btn.config(state = 'normal')
        R4.config(state = 'disable')
        R5.config(state = 'disable')
        R6.config(state = 'disable')
        canvas2.delete("id_txt_vs")
        canvas2.delete("id_txt_royale")
        canvas2.delete("id_txt_solo")
        canvas2.create_text(W/2, H*(91/100), text=txt_solo, font=("Helvetica", FONT_13), fill="white", tag="id_txt_solo")

    def player_vs_ia_mode():
        global ModeDeJeu
        ModeDeJeu = 0
        start_btn.config(state = 'normal')
        R4.config(state = 'normal')
        R5.config(state = 'normal')
        R6.config(state = 'normal')
        canvas2.delete("id_txt_solo")
        canvas2.delete("id_txt_vs")
        canvas2.delete("id_txt_royale")
        canvas2.create_text(W/2, H*(91/100), text=txt_vs, font=("Helvetica", FONT_13), fill="white", tag="id_txt_vs")

    def battle_royale_mode():
        global ModeDeJeu
        set_nbr_spawn(2)
        ModeDeJeu = 1
        start_btn.config(state = 'normal')
        R4.config(state = 'disable')
        R5.config(state = 'disable')
        R6.config(state = 'disable')
        canvas2.delete("id_txt_solo")
        canvas2.delete("id_txt_vs")
        canvas2.delete("id_txt_royale")
        canvas2.create_text(W/2, H*(91/100), text=txt_royale, font=("Helvetica", FONT_13), fill="white", tag="id_txt_royale")

    def aleatoire():
        global ModeDeJeu
        start_btn.config(state = 'normal')
        R4.config(state = 'disable')
        R5.config(state = 'disable')
        R6.config(state = 'disable')
        canvas2.delete("id_txt_solo")
        canvas2.delete("id_txt_vs")
        canvas2.delete("id_txt_royale")
        w3.set(np.random.randint(15, 22))

        ModeDeJeu = np.random.randint(2)

        if ModeDeJeu == 1:
            canvas2.create_text(W/2, H*(91/100), text=txt_royale, font=("Helvetica", FONT_13), fill="white", tag="id_txt_royale")
            set_nbr_spawn(2)
        else:
            set_nbr_spawn(np.random.randint(1, 4))
            if get_nbr_spawn() == 1:
                canvas2.create_text(W/2, H*(91/100), text=txt_solo, font=("Helvetica", FONT_13), fill="white", tag="id_txt_solo")
            else:
                canvas2.create_text(W/2, H*(91/100), text=txt_vs, font=("Helvetica", FONT_13), fill="white", tag="id_txt_vs")


    canvas2.create_text(W/2, H*(15/100), text="Tron Advanced", font=("Helvetica", FONT_50), fill="Yellow")
    canvas2.create_text(W*(90/100), H*(15/100), text="Contrôles : \nHAUT = Z\nBAS = S\nGAUCHE = Q\nDROITE = D", font=("Helvetica", FONT_13), fill="yellow")

    start_btn = tk.Button(Window, text="Start", font=("Helvetica", FONT_22), command = lambda:start_game())
    start_btn.config(state = 'disable')
    exit_btn = tk.Button(Window, text="Exit", font=("Helvetica", FONT_16))

    canvas2.create_window(W*(85/100), H*(50/100)+FIX_1, anchor="s", window=start_btn)
    canvas2.create_window(W*(95/100)+FIX_3, H*(96/100), anchor="s", window=exit_btn)

    R1 = tk.Radiobutton(canvas2, text="Solo", font=("Helvetica", FONT_10), anchor="s", variable=var_mode, value=1, command = lambda:solo_mode())
    R1.place(x=W*(10/100), y=H*(35/100))

    R2 = tk.Radiobutton(canvas2, text="Player VS IA", font=("Helvetica", FONT_10), anchor="s", variable=var_mode, value=2, command = lambda:player_vs_ia_mode())
    R2.place(x=W*(10/100), y=H*(46/100))
    R2.select()

    R3 = tk.Radiobutton(canvas2, text="Battle Royale", font=("Helvetica", FONT_10), anchor="s", variable=var_mode, value=3, command = lambda:battle_royale_mode())
    R3.place(x=W*(10/100), y=H*(57/100))

    R7 = tk.Radiobutton(canvas2, text="Aleatoire", font=("Helvetica", FONT_10), anchor="s", variable=var_mode, value=4, command = lambda:aleatoire())
    R7.place(x=W*(10/100), y=H*(68/100))

    R4 = tk.Radiobutton(canvas2, text="1 IA", font=("Helvetica", FONT_10), anchor="s", variable=var_ia, value=1, command = lambda:set_nbr_spawn(2))
    R4.place(x=W*(43/100)-FIX_2, y=H*(35/100))
    R4.select()

    R5 = tk.Radiobutton(canvas2, text="2 IA", font=("Helvetica", FONT_10), anchor="s", variable=var_ia, value=2, command = lambda:set_nbr_spawn(3))
    R5.place(x=W*(50/100)-FIX_2, y=H*(35/100))

    R6 = tk.Radiobutton(canvas2, text="3 IA", font=("Helvetica", FONT_10), anchor="s", variable=var_ia, value=3, command = lambda:set_nbr_spawn(4))
    R6.place(x=W*(57/100)-FIX_2, y=H*(35/100))

    w2 = Scale(canvas2, from_=100, to=10000, resolution=100, length=W*(45/100), tickinterval=1000, orient=HORIZONTAL, label ="Simulations par tour d'IA", font=("Helvetica", FONT_10))
    w2.set(1000)
    w2.place(x=((W/2)-W*(45/100)/2), y=H*(44/100))

    w3 = Scale(canvas2, from_=15, to=21, resolution=1, length=W*(45/100), tickinterval=1, orient=HORIZONTAL, label ="Taille de la Map", font=("Helvetica", FONT_10))
    w3.set(18)
    w3.place(x=((W/2)-W*(45/100)/2), y=H*(66/100))
    w3.config(state='normal')

    R2.invoke()
    R4.invoke()

    exit_btn.bind("<Button-1>", exit_game)


#  Dessine la grille de jeu - ne pas toucher

Couleur = ["red","yellow","magenta","orange"]

def Affiche_Game(Game):
    F.focus_force()
    canvas.delete("all")
    canvas2.delete("all")
    AfficherPage(0)
    H = canvas.winfo_height()

    def DrawCase(x,y,coul):
        x *= L
        y *= L
        canvas.create_rectangle(x, H-y, x+L, H-y-L, fill=coul)

    # dessin des murs
    for z in range(PROFONDEUR):
        for x in range(LARGEUR):
            for y in range (HAUTEUR):
                if Game.Grille[z,x,y] == 1  : DrawCase(x+LARGEUR*z, y, "gray")
                if Game.Grille[z,x,y] == 2  : DrawCase(x+LARGEUR*z, y, "cyan")
                if Game.Grille[z,x,y] == 3  : DrawCase(x+LARGEUR*z, y, "green")
                if Game.Grille[z,x,y] == 4  : DrawCase(x+LARGEUR*z, y, "green")
                if Game.Grille[z,x,y] == 5  : DrawCase(x+LARGEUR*z, y, "green")
                if Game.Grille[z,x,y] == 10 : DrawCase(x+LARGEUR*z, y, "white")

                if Game.Grille[z,x,y] == 20 or Game.Grille[z,x,y] == 21: DrawCase(x+LARGEUR*z, y, "purple")
                if Game.Grille[z,x,y] == 22 or Game.Grille[z,x,y] == 23: DrawCase(x+LARGEUR*z, y, "pink")
                if Game.Grille[z,x,y] == 24 or Game.Grille[z,x,y] == 25: DrawCase(x+LARGEUR*z, y, "blue")

    # dessin de la moto
    for i in range(Game.Nb_Entity):
        DrawCase(int(Game.X[i])+LARGEUR*int(Game.Z[i]), int(Game.Y[i]), Couleur[i])

def AfficheScore(Game):
    str_score = ""
    for i in range(Game.Nb_Entity):
        str_score += (Couleur[i].upper() + " : " + str(int(Game.Score[i])) + "   ")
    canvas.create_text(LARGEUR*20*3/2, 15, font='Helvetica 12 bold', fill="yellow", text = str_score)

###########################################################

# Liste des directions :
# 0 : sur place   1: à gauche  2 : en haut   3: à droite    4: en bas

dx = np.array([0, -1, 0,  1,  0],dtype=np.int32)
dy = np.array([0,  0, 1,  0, -1],dtype=np.int32)

# scores associés à chaque déplacement
ds = np.array([0,  1,  1,  1,  1],dtype=np.int32)


def keydown(e):  # récupération de la direction du joueur
    global dir_humain
    if e.char == 'z' or e.char == 'Z' :
        dir_humain = 2
        return
    elif e.char == 's' or e.char == 'S':
        dir_humain = 4
        return
    elif e.char == 'q' or e.char == 'Q':
        dir_humain = 1
        return
    elif e.char == 'd' or e.char == 'D':
        dir_humain = 3
        return

Window.bind("<KeyPress>", keydown)  # activé à chaque fois qu'une touche est pressé


def Play(Game):

    nb_entity = Game.Nb_Entity
    X = np.zeros(nb_entity)
    Y = np.zeros(nb_entity)
    Z = np.zeros(nb_entity)
    dep = [0 for i in range(nb_entity)]
    V = np.zeros(nb_entity)

    for i in range(nb_entity):
        X[i] = Game.X[i]
        Y[i] = Game.Y[i]
        Z[i] = Game.Z[i]
        Game.Grille[int(Z[i]), int(X[i]), int(Y[i])] = i+2  # place les traces des motos

    ReplaceTP(Game.Grille)

    for i in range(nb_entity):
        if(Game.Entity_Fini[i] == 0):  # on vérifie si l'agent n'est pas mort avant de le faire jouer
            if(i == 0):  # joueur humain ?
                X[i] += dx[dir_humain]
                Y[i] += dy[dir_humain]
                V[i] = Game.Grille[int(Z[i]), int(X[i]), int(Y[i])]
            else:
                dep[i] = MeilleurCoup(Game, i)
                if(dep[i] == (0,0)):  # si son meilleur coup est de rester sur place, il meurt
                    Game.Entity_Fini[i] = 1
                X[i] += dep[i][0]
                Y[i] += dep[i][1]
                V[i] = Game.Grille[int(Z[i]), int(X[i]), int(Y[i])]

        if(1 <= V[i] <= Game.Nb_Entity+1 or V[i] == 10):  # détection de collision
            Game.Entity_Fini[i] = 1  # agent i mort

    if np.sum(Game.Entity_Fini) == nb_entity: return True #arrêt quand tout les agents sont mort
    # if Game.Entity_Fini[0] == 1: return True  #arrêt quand tout le joueur humain meurt

    for i in range(nb_entity):
        for j in range(nb_entity):
            if(i != j):
                if((X[i] == X[j]) and (Y[i] == Y[j]) and Z[i] == Z[j]):
                    Game.Entity_Fini[i] = 1
                    Game.Entity_Fini[j] = 1
                    Game.Grille[int(Z[i]), int(X[i]), int(Y[i])] = 10
        if(Game.Entity_Fini[i] == 0):
            Game.X[i] = X[i]  # valide le déplacement
            Game.Y[i] = Y[i]  # valide le déplacement
            Game.Score[i] += 1
            Teleportation(Game, i)
        for k in range(nb_entity):
            if(i != k):
                if((X[i] == X[k]) and (Y[i] == Y[k]) and (Z[i] == Z[k])):
                    Game.Entity_Fini[i] = 1
                    Game.Entity_Fini[k] = 1

    return False  # la partie continue


def MeilleurCoup(Game, entity_n):
    score_dep = []
    dep = DeplacementPossible(Game, entity_n)

    # pour chaque coup, fait une copie du jeu, fait une simulation sur cette copie et apprend l'espérence moyenne de ce coup
    for i in range(len(dep)):
        Game2=Game.copy()
        Game2.X[entity_n] += dep[i][0]
        Game2.Y[entity_n] += dep[i][1]
        score_dep.append(MonteCarlo(Game2, entity_n))
    if(len(dep) == 0):
        return (0,0)
    else:
        return dep[score_dep.index(max(score_dep))] # retourne le déplacement associé au plus haut score

def DeplacementPossible(Game, entity_n):
    x,y,z = int(Game.X[entity_n]), int(Game.Y[entity_n]), int(Game.Z[entity_n])
    dep = []

    # déplacement possible si case vide ou si c'est un télépoteur [20, 25]
    if (Game.Grille[z][x  ][y-1] == 0 or 20 <= Game.Grille[z][x  ][y-1] <= 25):
        dep.append((0,-1))
    if (Game.Grille[z][x  ][y+1] == 0 or 20 <= Game.Grille[z][x  ][y+1] <= 25):
        dep.append((0, 1))
    if (Game.Grille[z][x+1][y  ] == 0 or 20 <= Game.Grille[z][x+1][y  ] <= 25):
        dep.append(( 1,0))
    if (Game.Grille[z][x-1][y  ] == 0 or 20 <= Game.Grille[z][x-1][y  ] <= 25):
        dep.append((-1,0))
    return dep

def MonteCarlo(Game, entity_n):
    G_depmap = Game.Grille.copy()

    for z in range(Game.Grille.shape[0]):  # simplification de Grille en une "depmap" pour les calcules, 0 = mouvement impossible, 1 = mouvement possible
        for x in range(Game.Grille.shape[1]):
            for y in range(Game.Grille.shape[2]):
                if(1 <= Game.Grille[z, x, y] <= Game.Nb_Entity+1 or Game.Grille[z, x, y] == 10):
                    G_depmap[z, x, y] = 0
                else: G_depmap[z, x, y] = 1

    score_moyen = SimulationPartie(Game, G_depmap, entity_n)
    return score_moyen

def SimulationPartie(Game, depmap, entity_n):
    # on copie les datas de départ pour créer plusieurs parties en //
    nb     = Game.Nb_Iterations
    G      = np.tile(Game.Grille, (nb,1,1,1))
    depmap = np.tile(depmap, (nb,1,1,1))
    X      = np.tile(int(Game.X[entity_n]), nb)
    Y      = np.tile(int(Game.Y[entity_n]), nb)
    Z      = np.tile(int(Game.Z[entity_n]), nb)
    S      = np.tile(int(Game.Score[entity_n]), nb)
    I      = np.arange(nb)  # 0,1,2,3,4,5...

    SimulationFinie = False
    while(not SimulationFinie):

        depmap[I, Z, X, Y] = 0  # marque le passage de la moto
        ReplaceTP_Simulation(depmap, I)

        # vérifie la possibilité de se deplacer dans chaque direction
        Vgauche = (np.equal(depmap[I, Z, X-1, Y  ], 1)) * 1
        Vhaut   = (np.equal(depmap[I, Z, X  , Y+1], 1)) * 1
        Vdroite = (np.equal(depmap[I, Z, X+1, Y  ], 1)) * 1
        Vbas    = (np.equal(depmap[I, Z, X  , Y-1], 1)) * 1

        LPossibles =  np.zeros((nb,4),dtype=np.int32)
        Tailles = np.zeros(nb,dtype=np.int32)

        LPossibles[I, Tailles] = Vgauche*1
        Tailles += Vgauche

        LPossibles[I, Tailles] = Vhaut*2
        Tailles += Vhaut

        LPossibles[I, Tailles] = Vdroite*3
        Tailles += Vdroite

        LPossibles[I, Tailles] = Vbas*4
        Tailles += Vbas

        Tailles[Tailles == 0] = 1

        R = LPossibles[I, np.random.randint(Tailles)]  # vecteur des déplacements

        # DEPLACEMENT
        DX = dx[R]  # vecteur des déplacements en x
        DY = dy[R]  # vecteur des déplacements en y
        X += DX
        Y += DY
        X, Y, Z = TP_Simultation(G, I, X, Y, Z)
        S += ds[R]  # vecteur des scores
        if(np.sum(R) == 0): SimulationFinie = True  # quand toutes les simulations ne peuvent plus bouger, on arrête
    return np.mean(S)


# téléporte les agents dans la partie, les cases 20+n et 20+n+1 sont des téléporteurs liés entre eux
# déplace directement les agents à leurs nouvelles coordonnées
def Teleportation(Game, entity_n):
    x,y,z = int(Game.X[entity_n]), int(Game.Y[entity_n]), int(Game.Z[entity_n])

    for i in range(20, len(pos_tp)+20, 2):
        if(Game.Grille[z,x,y] == i):
            Game.X[entity_n] = pos_tp[i-19][0]
            Game.Y[entity_n] = pos_tp[i-19][1]
            Game.Z[entity_n] = pos_tp[i-19][2]

        if(Game.Grille[z,x,y] == i+1):
            Game.X[entity_n] = pos_tp[i-20][0]
            Game.Y[entity_n] = pos_tp[i-20][1]
            Game.Z[entity_n] = pos_tp[i-20][2]

# téléporte les IA dans la simulation, les cases 20+n et 20+n+1 sont des téléporteurs liés entre eux
def TP_Simultation(G ,I, X, Y, Z):
    for i in range(20, len(pos_tp)+20, 2):
        tpi = np.equal(G[I, Z, X, Y], i)
        X[tpi] = pos_tp[i-19][0]
        Y[tpi] = pos_tp[i-19][1]
        Z[tpi] = pos_tp[i-19][2]

        tpip1 = np.equal(G[I, Z, X, Y], i+1)
        X[tpip1] = pos_tp[i-20][0]
        Y[tpip1] = pos_tp[i-20][1]
        Z[tpip1] = pos_tp[i-20][2]
    return X, Y, Z  # retourne les nouvelles coordonnées

# replace les cases de teleportation après le marquage de la trace dans la partie
def ReplaceTP(Grille):
    for i in range(len(pos_tp)):
        Grille[pos_tp[i][2]][pos_tp[i][0]][pos_tp[i][1]] = i+20

# replace les cases de teleportation visible comme des cases accessible après le marquage de la trace dans la simulation
def ReplaceTP_Simulation(Grille, I):
    for i in range(len(pos_tp)):
        Grille[I, pos_tp[i][2], pos_tp[i][0], pos_tp[i][1]] = 1

################################################################################

#  presque duplication de code pour le mode de jeu "BattleRoyal"

def PlayBattleRoyal(Game):
    global CleanTP

    nb_entity = Game.Nb_Entity
    X = np.zeros(nb_entity)
    Y = np.zeros(nb_entity)
    Z = np.zeros(nb_entity)
    dep = [0 for i in range(nb_entity)]
    V = np.zeros(nb_entity)

    if(CleanTP == 1):
        ResetCase(Game)
        CleanTP = 0

    for i in range(nb_entity):
        X[i] = Game.X[i]
        Y[i] = Game.Y[i]
        Z[i] = Game.Z[i]
        Game.Grille[int(Z[i]), int(X[i]), int(Y[i])] = i+2

    for i in range(nb_entity):
        if(Game.Entity_Fini[i] == 0):
            if(i == 0):
                X[i] += dx[dir_humain]
                Y[i] += dy[dir_humain]
                V[i] = Game.Grille[int(Z[i]), int(X[i]), int(Y[i])]
            else:
                dep[i] = MeilleurCoupRoyal(Game, i)
                if(dep[i] == (0,0)):
                    Game.Entity_Fini[i] = 1
                X[i] += dep[i][0]
                Y[i] += dep[i][1]
                V[i] = Game.Grille[int(Z[i]), int(X[i]), int(Y[i])]
        if(1 <= V[i] <= Game.Nb_Entity+1 or V[i] == 10):
            Game.Entity_Fini[i] = 1

    for i in range(1, nb_entity):
        if(Game.Entity_Fini[i] == 1):
            ResetCase(Game)
            X[i] = 10
            Y[i] = 10
            Z[i] = 1
            Game.Entity_Fini[i] = 0

    if(Game.Entity_Fini[0] == 1):
        return True

    for i in range(nb_entity):
        for j in range(nb_entity):
            if(i != j):
                if((X[i] == X[j]) and (Y[i] == Y[j]) and Z[i] == Z[j]):
                    Game.Entity_Fini[i] = 1
                    Game.Entity_Fini[j] = 1
                    Game.Grille[int(Z[i]), int(X[i]), int(Y[i])] = 10
        if(Game.Entity_Fini[i] == 0):
            Game.X[i] = X[i]
            Game.Y[i] = Y[i]
            Game.Score[i] += 1
        for k in range(nb_entity):
            if(i != k):
                if((X[i] == X[k]) and (Y[i] == Y[k]) and (Z[i] == Z[k])):
                    Game.Entity_Fini[i] = 1
                    Game.Entity_Fini[k] = 1
    return False

def MeilleurCoupRoyal(Game, entity_n):
    score_dep = []
    dep = DeplacementPossibleRoyal(Game, entity_n)
    for i in range(len(dep)):
        Game2=Game.copy()
        Game2.X[entity_n] += dep[i][0]
        Game2.Y[entity_n] += dep[i][1]
        score_dep.append(MonteCarloRoyal(Game2, entity_n))
    if(len(dep) == 0):
        return (0,0)
    else:
        return dep[score_dep.index(max(score_dep))]

def DeplacementPossibleRoyal(Game, entity_n):
    x,y,z = int(Game.X[entity_n]), int(Game.Y[entity_n]), int(Game.Z[entity_n])
    dep = []
    if (Game.Grille[z][x  ][y-1] == 0 or 20 <= Game.Grille[z][x  ][y-1] <= 25):
        dep.append((0,-1))
    if (Game.Grille[z][x  ][y+1] == 0 or 20 <= Game.Grille[z][x  ][y+1] <= 25):
        dep.append((0, 1))
    if (Game.Grille[z][x+1][y  ] == 0 or 20 <= Game.Grille[z][x+1][y  ] <= 25):
        dep.append(( 1,0))
    if (Game.Grille[z][x-1][y  ] == 0 or 20 <= Game.Grille[z][x-1][y  ] <= 25):
        dep.append((-1,0))
    return dep

def MonteCarloRoyal(Game, entity_n):
    G_depmap = Game.Grille.copy()
    for z in range(Game.Grille.shape[0]):
        for x in range(Game.Grille.shape[1]):
            for y in range(Game.Grille.shape[2]):
                if(1 <= Game.Grille[z, x, y] <= 3 or Game.Grille[z, x, y] == 10):
                    G_depmap[z, x, y] = 0
                else: G_depmap[z, x, y] = 1
    score_moyen = SimulationPartieRoyal(Game, G_depmap, entity_n)
    return score_moyen

def SimulationPartieRoyal(Game, depmap, entity_n):
    nb     = Game.Nb_Iterations
    G      = np.tile(Game.Grille,(nb,1,1,1))
    depmap = np.tile(depmap,(nb,1,1,1))
    X      = np.tile(int(Game.X[entity_n]),nb)
    Y      = np.tile(int(Game.Y[entity_n]),nb)
    Z      = np.tile(int(Game.Z[entity_n]),nb)
    S      = np.tile(int(Game.Score[entity_n]),nb)
    I      = np.arange(nb)

    SimulationFinie = False
    while(not SimulationFinie):
        depmap[I, Z, X, Y] = 0

        Vgauche = (np.equal(depmap[I, Z, X-1, Y], 1)) * 1
        Vhaut = (np.equal(depmap[I, Z, X, Y+1], 1)) * 1
        Vdroite = (np.equal(depmap[I, Z, X+1, Y], 1)) * 1
        Vbas = (np.equal(depmap[I, Z, X, Y-1], 1)) * 1

        LPossibles =  np.zeros((nb,4),dtype=np.int32)
        Tailles = np.zeros(nb,dtype=np.int32)

        LPossibles[I, Tailles] = Vgauche*1
        Tailles += Vgauche
        LPossibles[I, Tailles] = Vhaut*2
        Tailles += Vhaut
        LPossibles[I, Tailles] = Vdroite*3
        Tailles += Vdroite
        LPossibles[I, Tailles] = Vbas*4
        Tailles += Vbas

        Tailles[Tailles == 0] = 1
        R = LPossibles[I, np.random.randint(Tailles)]

        DX = dx[R]
        DY = dy[R]
        X += DX
        Y += DY
        S += ds[R]
        if(np.sum(R) == 0): SimulationFinie = True
    return np.mean(S)

def ResetCase(Game):
    for z in range(PROFONDEUR):
        for x in range(LARGEUR):
            for y in range (HAUTEUR):
                if(Game.Grille[z,x,y] != 1):
                    Game.Grille[z,x,y] = 0
                if(z != 1):
                    Game.Grille[z,x,y] = 1

################################################################################

def menu():
    Affiche_Menu()
    Window.after(100, Partie)

def Partie():
    global Menu_Window

    if Menu_Window: #  tant qu'on a pas cliqué sur Start, Menu_Window reste à True
        Window.after(100, Partie)
    else:
        Tstart = time.time()
        if(ModeDeJeu == 0):
            PartieTermine = Play(CurrentGame)
        else:
            PartieTermine = PlayBattleRoyal(CurrentGame)

        if not PartieTermine:
            print("Temps du tour : {}".format(time.time() - Tstart))
            Affiche_Game(CurrentGame)
            Window.after(500, Partie)
        else:
            AfficheScore(CurrentGame)
            Menu_Window = True
            Window.after(3000, menu)

################################################################################

#  Mise en place de l'interface - ne pas toucher

Window.after(500, menu)
Window.mainloop()
