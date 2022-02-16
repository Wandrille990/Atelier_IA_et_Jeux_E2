import random
import tkinter as tk
from tkinter import font  as tkfont
import numpy as np
 

##########################################################################
#
#   Partie I : variables du jeu  -  placez votre code dans cette section
#
#########################################################################
 
# Plan du labyrinthe

# 0 vide
# 1 mur
# 2 maison des fantomes (ils peuvent circuler mais pas pacman)

def CreateArray(L):
   T = np.array(L,dtype=np.int32)
   T = T.transpose()  ## ainsi, on peut écrire TBL[x][y]
   return T

TBL = CreateArray([
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,3,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,3,1],
        [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
        [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
        [1,0,1,0,1,1,0,1,1,2,2,1,1,0,1,1,0,1,0,1],
        [1,0,0,0,0,0,0,1,2,2,2,2,1,0,0,0,0,0,0,1],
        [1,0,1,0,1,1,0,1,1,1,1,1,1,0,1,1,0,1,0,1],
        [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
        [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
        [1,3,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,3,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]);

        
HAUTEUR = TBL.shape [1]      
LARGEUR = TBL.shape [0]  

# placements des pacgums et des fantomes

def PlacementsGUM():  # placements des pacgums
   GUM = np.zeros(TBL.shape,dtype=np.int32)
   
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if ( TBL[x][y] == 0):
            GUM[x][y] = 1
         elif(TBL[x][y] == 3):
            GUM[x][y] = 2
   return GUM
            
GUM = PlacementsGUM()   

PacManPos = [5,5]

Ghosts  = []
Ghosts.append([LARGEUR//2, HAUTEUR // 2,"pink"  , (0, 0)])
Ghosts.append([LARGEUR//2, HAUTEUR // 2,"orange", (0, 0)])
Ghosts.append([LARGEUR//2, HAUTEUR // 2,"cyan"  , (0, 0)])
Ghosts.append([LARGEUR//2, HAUTEUR // 2,"red"   , (0, 0)])    

score = 0   
end = 0
chasseFantome = 0

def PlacementsDistGum():  # placements des Distanceaux Gums
   TabDistGum = np.zeros(TBL.shape,dtype=np.int32)

   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if(TBL[x][y] == 1 or TBL[x][y] == 2):
            TabDistGum[x][y] = 999
         elif(GUM[x][y] == 1 or GUM[x][y] == 2):
            TabDistGum[x][y] = 0
            #TabDistGum[x][y] = LARGEUR*HAUTEUR
   return TabDistGum

TabDistGum = PlacementsDistGum()

#print(TabDistGum.transpose())
#print(TabDistGum)
#print(" ")


def PlacementsDistGhosts():  # placements des Distanceaux Gums
   TabDistGhosts = np.zeros(TBL.shape,dtype=np.int32)

   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if(TBL[x][y] == 1 or TBL[x][y] == 2):
            TabDistGhosts[x][y] = 999
         elif(TabDistGhosts[x][y] == 0):
            TabDistGhosts[x][y] = LARGEUR*HAUTEUR
         for F in Ghosts: 
            if((x, y) == (F[0], F[1])):
               TabDistGhosts[x][y] = 0
         
   return TabDistGhosts

TabDistGhosts = PlacementsDistGhosts()

#print(TabDistGhosts)

##############################################################################
#
#   Partie II :  AFFICHAGE -- NE PAS MODIFIER  jusqu'à la prochaine section
#
##############################################################################

 

ZOOM = 40   # taille d'une case en pixels
EPAISS = 8  # epaisseur des murs bleus en pixels

screeenWidth = (LARGEUR+1) * ZOOM
screenHeight = (HAUTEUR+2) * ZOOM

Window = tk.Tk()
Window.geometry(str(screeenWidth)+"x"+str(screenHeight)) # taille de la fenetre
Window.title("ESIEE - PACMAN")

# gestion de la pause

PAUSE_FLAG = False 

def keydown(e):
   global PAUSE_FLAG
   if e.char == ' ' : 
      PAUSE_FLAG = not PAUSE_FLAG 

Window.bind("<KeyPress>", keydown)
 

# création de la frame principale stockant plusieurs pages

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
    

def WindowAnim():
    MainLoop()
    Window.after(200,WindowAnim)

Window.after(100,WindowAnim)

# Ressources

PoliceTexte = tkfont.Font(family='Arial', size=22, weight="bold", slant="italic")

# création de la zone de dessin

Frame1 = CreerUnePage(0)

canvas = tk.Canvas( Frame1, width = screeenWidth, height = screenHeight )
canvas.place(x=0,y=0)
canvas.configure(background='black')
 
 
#  FNT AFFICHAGE


def To(coord):
   return coord * ZOOM + ZOOM 
   
# dessine l'ensemble des éléments du jeu par dessus le décor

anim_bouche = 0
animPacman = [ 5,10,15,10,5]


def Affiche(PacmanColor,message,data1,data2, data3):
   global anim_bouche
   
   def CreateCircle(x,y,r,coul):
      canvas.create_oval(x-r,y-r,x+r,y+r, fill=coul, width  = 0)
   
   canvas.delete("all")
      
      
   # murs
   for x in range(LARGEUR-1):
      for y in range(HAUTEUR):
         if ( TBL[x][y] == 1 and TBL[x+1][y] == 1 ):
            xx = To(x)
            xxx = To(x+1)
            yy = To(y)
            canvas.create_line(xx,yy,xxx,yy,width = EPAISS,fill="blue")

   for x in range(LARGEUR):
      for y in range(HAUTEUR-1):
         if ( TBL[x][y] == 1 and TBL[x][y+1] == 1 ):
            xx = To(x) 
            yy = To(y)
            yyy = To(y+1)
            canvas.create_line(xx,yy,xx,yyy,width = EPAISS,fill="blue")
            
   # pacgum
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if ( GUM[x][y] == 1):
            xx = To(x) 
            yy = To(y)
            e = 5
            canvas.create_oval(xx-e,yy-e,xx+e,yy+e,fill="orange")
         if ( GUM[x][y] == 2):
            xx = To(x) 
            yy = To(y)
            e = 6
            canvas.create_oval(xx-e,yy-e,xx+e,yy+e,fill="red")
            
   #extra info
   #for x in range(LARGEUR):
   #   for y in range(HAUTEUR):
   #      xx = To(x) 
   #      yy = To(y) - 11
   #      txt = data1[x][y]
   #      canvas.create_text(xx,yy, text = txt, fill ="white", font=("Purisa", 8)) 
         
   #extra info 2
   #for x in range(LARGEUR):
   #   for y in range(HAUTEUR):
   #      xx = To(x) + 10
   #      yy = To(y) 
   #      txt = data2[x][y]
   #      canvas.create_text(xx,yy, text = txt, fill ="yellow", font=("Purisa", 8)) 
         
   #info distances
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         xx = To(x)
         yy = To(y) + 12
         if(data2[x][y] == 999):
            txt = ""
         else:
            txt = "{}/{}".format(data2[x][y], data3[x][y])
         canvas.create_text(xx,yy, text = txt, fill ="white", font=("Purisa", 8))
         
  
   # dessine pacman
   xx = To(PacManPos[0]) 
   yy = To(PacManPos[1])
   e = 20
   anim_bouche = (anim_bouche+1)%len(animPacman)
   ouv_bouche = animPacman[anim_bouche] 
   tour = 360 - 2 * ouv_bouche
   canvas.create_oval(xx-e,yy-e, xx+e,yy+e, fill = PacmanColor)
   canvas.create_polygon(xx,yy,xx+e,yy+ouv_bouche,xx+e,yy-ouv_bouche, fill="black")  # bouche
   
  
   #dessine les fantomes
   dec = -3
   for P in Ghosts:
      xx = To(P[0]) 
      yy = To(P[1])
      e = 16
      
      coul = P[2]
      # corps du fantome
      CreateCircle(dec+xx,dec+yy-e+6,e,coul)
      canvas.create_rectangle(dec+xx-e,dec+yy-e,dec+xx+e+1,dec+yy+e, fill=coul, width  = 0)
      
      # oeil gauche
      CreateCircle(dec+xx-7,dec+yy-8,5,"white")
      CreateCircle(dec+xx-7,dec+yy-8,3,"black")
       
      # oeil droit
      CreateCircle(dec+xx+7,dec+yy-8,5,"white")
      CreateCircle(dec+xx+7,dec+yy-8,3,"black")
      
      dec += 3
      
   # texte  
   
   canvas.create_text(screeenWidth // 2, screenHeight- 50 , text = "PAUSE : PRESS SPACE", fill ="yellow", font = PoliceTexte)
   canvas.create_text(screeenWidth // 2, screenHeight- 20 , text = message, fill ="yellow", font = PoliceTexte)
   
 
AfficherPage(0)
            
#########################################################################
#
#  Partie III :   Gestion de partie   -   placez votre code dans cette section
#
#########################################################################

def PacManPossibleMove():
   global TabDistGum, TabDistGhosts, PacManPos, chasseFantome, TBL
   
   L = []
   x,y = PacManPos
   
   if(chasseFantome != 0):
      chasseFantome -= 1
      print(chasseFantome)
      distmin3 = min(TabDistGhosts[x+1, y], TabDistGhosts[x-1, y], TabDistGhosts[x, y+1], TabDistGhosts[x ,y-1])
      if  (TabDistGhosts[x+1, y] == distmin3 and TBL[x+1][y] != 2) : return (1,0)
      elif(TabDistGhosts[x-1, y] == distmin3 and TBL[x-1][y] != 2) : return (-1,0)
      elif(TabDistGhosts[x, y+1] == distmin3 and TBL[x][y+1] != 2) : return (0,1)
      elif(TabDistGhosts[x, y-1] == distmin3 and TBL[x][y-1] != 2) : return (0,-1)
         
   
   elif(TabDistGhosts[x, y] > 3):
      distmin = min(TabDistGum[x+1, y], TabDistGum[x-1, y], TabDistGum[x, y+1], TabDistGum[x ,y-1])
      if  (TabDistGum[x+1, y] == distmin) : return (1,0)
      elif(TabDistGum[x-1, y] == distmin) : return (-1,0)
      elif(TabDistGum[x, y+1] == distmin) : return (0,1)
      elif(TabDistGum[x, y-1] == distmin) : return (0,-1)
      
   else :
      distmin2 = max(list(filter(lambda x: x != 999, 
         [TabDistGhosts[x+1,y], TabDistGhosts[x-1,y], TabDistGhosts[x,y+1], TabDistGhosts[x,y-1]])))
      if  (TabDistGhosts[x+1, y] == distmin2 ) : return (1,0)
      elif(TabDistGhosts[x-1, y] == distmin2 ) : return (-1,0)
      elif(TabDistGhosts[x, y+1] == distmin2 ) : return (0,1)
      elif(TabDistGhosts[x, y-1] == distmin2 ) : return (0,-1)
   return(0,0)
   
def GhostsPossibleMove(x,y, prevDep):
   
   if((TBL[x+1][y  ] == 1 and TBL[x-1][y  ] == 1) and ((TBL[x][y+1] == 0 and TBL[x][y-1] == 0) or (TBL[x][y+1] == 3 and TBL[x][y-1] == 3))):
      return [prevDep] 
      
   if((TBL[x  ][y+1] == 1 and TBL[x  ][y-1] == 1) and ((TBL[x+1][y] == 0 and TBL[x-1][y] == 0) or (TBL[x+1][y] == 3 and TBL[x-1][y] == 3))):
      return [prevDep]
   
   L = []
   if ( TBL[x  ][y-1] != 1): L.append((0,-1))
   if ( TBL[x  ][y+1] != 1): L.append((0, 1))
   if ( TBL[x+1][y  ] != 1): L.append(( 1,0))
   if ( TBL[x-1][y  ] != 1): L.append((-1,0))
   return L
   
def IA():
   global PacManPos, Ghosts, score, end, chasseFantome
   
   CalculDistanceGum()
   
   if(end != 1):
      #deplacement PacMan
      L = PacManPossibleMove()
      PacManPos[0] += L[0]
      PacManPos[1] += L[1]
      if(GUM[PacManPos[0], PacManPos[1]] == 1):
         GUM[PacManPos[0], PacManPos[1]] = 0
         score += 100
      elif(GUM[PacManPos[0], PacManPos[1]] == 2):
         GUM[PacManPos[0], PacManPos[1]] = 0
         score += 100
         chasseFantome = 16
      Colision()
   
      #deplacement Fantome
      for F in Ghosts:
         L = GhostsPossibleMove(F[0],F[1], F[3])
         choix = random.randrange(len(L))
         F[0] += L[choix][0]
         F[1] += L[choix][1]
         F[3] = L[choix][0], L[choix][1]   
         CalculDistanceGhosts()
         Colision()
         

def CalculDistanceGum():
   global TabDistGum
   
   for i in range(4):
      for x in range(1,LARGEUR-1):
         for y in range(1,HAUTEUR-1):
            if(GUM[x][y] == 1 or GUM[x][y] == 2):
               TabDistGum[x][y] = 0 
            elif(TabDistGum[x][y] != 999):
               comp = [TabDistGum[x-1][y], TabDistGum[x+1][y], TabDistGum[x][y+1], TabDistGum[x][y-1]]
               TabDistGum[x][y] = min(comp)+1 
   
   #print(TabDistGum.transpose())
   #print(TabDistGum)
   #print("")
   
def CalculDistanceGhosts():
   global TabDistGhosts, TBL
   
   
   for x in range(1,LARGEUR-1):
      for y in range(1,HAUTEUR-1):
         if(TBL[x][y] == 1 or TBL[x][y] == 2):
            TabDistGhosts[x][y] = 999
         else: TabDistGhosts[x][y] = HAUTEUR*LARGEUR
   
   for F in Ghosts:
      #if(TBL[F[0]][F[1]] != 2):
      TabDistGhosts[F[0]][F[1]] = 0
      for i in range(8):
         for x in range(1,LARGEUR-1):
            for y in range(1,HAUTEUR-1):
               if(TabDistGhosts[x][y] != 999 and TabDistGhosts[x][y] != 0):
                  comp = [TabDistGhosts[x-1][y], TabDistGhosts[x+1][y], TabDistGhosts[x][y+1], TabDistGhosts[x][y-1]]
                  TabDistGhosts[x][y] = min(comp)+1 
   
   #print(TabDistGhosts.transpose())
   #print(TabDistGhosts)
   #print("")
   
def Colision():
   global PacManPos, Ghosts, end, LARGEUR, HAUTEUR, score
   
   for F in Ghosts:
      if(PacManPos == [F[0],F[1]]):
         if(chasseFantome != 0):
            F[0] = LARGEUR//2
            F[1] = HAUTEUR//2
            score += 2000
         else:
            print("STOP !")
            end = 1
   

 
#  Boucle principale de votre jeu appelée toutes les 500ms

def MainLoop():
   if not PAUSE_FLAG : IA()
   color = "yellow"
   if(chasseFantome%2 == 0):
      color = "yellow"
   else:
      color = "red"

   Affiche(PacmanColor = color, message = "Score : {}".format(score), 
          data1=TBL, data2=TabDistGum, data3=TabDistGhosts) 
 
 
###########################################:
#  demarrage de la fenetre - ne pas toucher

Window.mainloop()

 
   
   
    
   
   
