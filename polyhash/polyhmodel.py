#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Module de définition des structures de données de Poly#.
"""
from polyhutils import *
from tkinter.filedialog import *
#from polyhsolver import backboneGeneration_1 # TODO pour générer les backbones dans l'interface
#from polyhsolver import backboneGeneration_2


__all__ = ['Carte'] # ajouter dans cette liste tous les symboles 'importables'

class Carte:
    """
        Classe de définition d'une carte qu'il faudra recouvrir de routeurs.
    """

    def __init__(self, cheminCarte):
        """Initialisation des attributs de la carte à leur valeur par défaut."""
        self.cheminCarte = cheminCarte  # Chemin du fichier contenant la carte
        self.nomCarte = ""              # Nom de la carte
        self.nbCol = 0                  # Nombre de colonnes de la carte
        self.nbLig = 0                  # Nombre de lignes de la carte
        self.radius = 0                 # Rayon de portée du routeur
        self.backboneCost = 0           # Coût de la pose d'un backbone
        self.routerCost = 0             # Coût de la pose d'un routeur
        self.budget = 0                 # Budget total
        self.backboneInit = []          # Coordonnées du backbone initial
        self.map = []                   # Tableau contenant les différentes lignes de la map
        self.nbRouteur = 0              # Nombre de routeurs posés
        self.nbBackbone = 0             # Nombre de backbones posés
        self.nbCaseCouverte = 0         # Nombre de cases couvertes par les routeurs
        self.posJoueur = [0, 0]         # Coordonnées courante dans l'interface graphique
        self.posRouteurs = []           # Tableau contenant les coordonnées des routeurs posés
        self.cellCouverte = []          # Tableau contenant les coordonnées des cases couvertes
        self.posBackbones = []          # Tableau conteannt les coordonnées des backbones posés
        self._generationCarte()         # Initialisation des attributs en fonction des paramètres de la carte choisie
        self.posRouteursPop = []        # Tableau contenant les coordonnées des routeurs retirés
        self.mapCouvertures = []        # Tableau contenant les différentes lignes de la map de couverture (pour
                                        # chaque case, nombre potentiel de cases couvertes par un routeur posé dessus)

    def _generationCarte(self):
        """Traitement du fichier d'entrée pour affecter la valeur des différents
        paramètres de la carte choisie aux attributs de notre objet Carte.
        """
        fichier = open(self.cheminCarte, "r")

        ligne = " "
        nbLigne = 0

        # Parcours du fichier
        for ligne in fichier:
            ligne = ligne.rstrip('\n')
            if(nbLigne == 0):
                lst = ligne.split(" ")
                self.nbLig = int(lst[0])
                self.nbCol = int(lst[1])
                self.radius = int(lst[2])
            elif(nbLigne == 1):
                lst = ligne.split(" ")
                self.backboneCost = int(lst[0])
                self.routerCost = int(lst[1])
                self.budget = int(lst[2])
            elif(nbLigne == 2):
                lst = ligne.split(" ")
                lst = list(map(int, lst))
                self.backboneInit = lst
                self.posJoueur[0] = (lst[0] + 1)
                self.posJoueur[1] = (lst[1])
            else:
                self.map.append((list(map(str, ligne))))
            nbLigne += 1

        # Récupération du nom de la carte en fonction du nom du fichier d'entrée
        lst = self.cheminCarte.split("/")
        self.nomCarte = lst[len(lst) - 1].split(".")[0]
        fichier.close()

    def addBackbone(self, pos):
        """Ajout d'un backbone sur la carte.
        Args:
            pos [y,x]: coordonnées y et x du backbone ajouté.
        """
        if(not(pos in self.posBackbones) and not(pos == self.backboneInit)):
            self.posBackbones.append(pos)
            self.nbBackbone += 1

    def addCellCouverte(self, pos):
        """Prise en compte de la couverture d'une cellule.
        Args:
            pos [y, x]: coordonnées de la cellule couverte.
        """
        if(not(pos in self.cellCouverte)):
            self.cellCouverte.append(pos)
            self.nbCaseCouverte += 1

    def addDelRouteur(self):
        """Ajout ou suppression d'un routeur sur la carte via l'interface graphique."""
        lst = [0, 0]
        lst[0] = self.posJoueur[0]
        lst[1] = self.posJoueur[1]
        if(lst in self.posRouteurs):
            # Si un routeur a déjà été positionné ici, on le supprime
            self.posRouteurs.remove(lst)
            self.nbRouteur -= 1
        else:
            # Sinon, on ajoute le routeur à ces coordonnées
            self.posRouteurs.append(lst)
            self.nbRouteur += 1
            self.calculZoneCouverte(lst)

    def reset(self):
        """Réinitialisation des attributs de la carte liés à la pose des
        routeurs et des backbones."""
        self.posRouteurs = []
        self.cellCouverte = []
        self.nbRouteur = 0
        self.nbBackbone = 0
        self.nbCaseCouverte = 0
        self.posBackbones = []
        self.posBackbones = []


    def calculZoneCouverte(self, pos):
        """Calcul de la zone couverte par le routeur indiqué.
        Args :
            pos [y, x]: coordonnées du routeur.
        """
        posY = pos[0]
        posX = pos[1]

        c = self.radius + 1

        for i in range(-c + 1, c):
            for j in range(-c + 1, c):
                a = posX + i
                b = posY + j
                foundWall = False

                for k in range(min(a, posX), max(a, posX) + 1):
                    for l in range(min(b, posY), max(b, posY) + 1):
                        if(self.mur(l, k)):
                            foundWall = True

                if(not(foundWall) and not(self.mur(b, a))):
                    self.addCellCouverte([b, a])

    def couverture(self,pos,test=False,zone=[0,1,2,3],frag=False,dibool=False) :
        """Calcul de la zone couverte par le routeur indiqué.
        Args :
            pos [x, y]: coordonnées du routeur.
            test bool : mettre True si l'on désire l'affichage étape par étape du recouvrement du routeur
            zone list : indique quelles parties de la map on veut couvrir selon cette façon : ([0][1]
                                                                                               [3][2])
            frag bool : mettre True si l'on désire obtenir la couverture de manière fragmentée ([1][2][3]
                                                                                                [8][0][4]
                                                                                                [7][6][5]) 0 est le routeur
        """
        if(self.map[pos[1]][pos[0]]== "." or self.map[pos[1]][pos[0]]=="C") :  # On prend C, une selection dans la map d'un carré de demi-segment de longueur rad et de centre le routeur (C'est sur cette liste que l'on va travailler le couvrement)
            care,carePos=carre(self.map,pos,self.radius)

            if test :
                afficherMap(care)

            routeurPos = (pos[0]-carePos[0],pos[1]-carePos[1]) # Pos du routeur au sein du carré
            directions=[]
            if frag :
                HG,H,HD,D,BD,B,BG,G=[],[],[],[],[],[],[],[]
            else :
                final=[] # Liste finale des positions de couverture
            if care[routeurPos[1]][routeurPos[0]] == "." :
                if not frag :
                    final.append(pos) # Liste finale des positions de couvrement
            if test :
                care[pos[1]][pos[0]]="R"
                afficherMap(care)

             # On regarde depuis le routeur, dans les 4 directions (haut,droite,bas,gauche), la distance
             # séparant le routeur d'une case mur. Distances que l'on va mettre dans cette ordre
             # (haut,droite,bas,gauche) au sein de la liste D (et on recouvre par ailleurs les cases visitées sol)

            for i in range(4) :
                if (i == 0 and (0 in zone or 1 in zone)) or (i==1 and (1 in zone or 2 in zone)) or (i==2 and (2 in zone or 3 in zone)) or (i==3 and (3 in zone or 0 in zone)) :
                    k=1
                    direc=((i==1)-(i==3),(i==2)-(i==0))
                    val=0
                    courrantX=routeurPos[0]+direc[0]
                    courrantY=routeurPos[1]+direc[1]
                    while(k<=self.radius and (care[courrantY][courrantX] == "." or care[courrantY][courrantX] == "C" or care[courrantY][courrantX] == "R")) :
                        val=abs(direc[1-i%2])
                        if care[courrantY][courrantX] == "." :
                            if frag :
                                [H,D,B,G][i].append((pos[0]+direc[0],pos[1]+direc[1]))
                            else :
                                final.append((pos[0]+direc[0],pos[1]+direc[1]))
                        if test :
                            care[pos[1]+direc[1]][pos[0]+direc[0]]="C"
                            afficherMap(care)
                        k+=1
                        direc=(k*((i==1)-(i==3)),k*((i==2)-(i==0)))
                        courrantX=routeurPos[0]+direc[0]
                        courrantY=routeurPos[1]+direc[1]
                    directions.append(val)
                else :
                    directions.append(0)

            if dibool :
                return directions

            posHG=(routeurPos[0]-directions[3],routeurPos[1]-directions[0])           # Sélection de la partie de map utile pour le recouvrement
            tailleX=directions[1]+directions[3]+1
            tailleY=directions[2]+directions[0]+1
            select=selection(care,posHG,tailleX,tailleY)


            listes=[selection(select,(0,0),directions[3],directions[0]) if 0 in zone else None,                    # Fragmentation en 4 zones autour du routeur de la selection précédente
                selection(select,(directions[3]+1,0),directions[1],directions[0]) if 1 in zone else None,
                selection(select,(directions[3]+1,directions[0]+1),directions[1],directions[2]) if 2 in zone else None,
                selection(select,(0,directions[0]+1),directions[3],directions[2]) if 3 in zone else None]

            for i in zone :
                y=0
                k=directions[3] if (i==0 or i==3) else directions[1]
                for line in [[e for e in line[::(i==1)+(i==2)-(i==0)-(i==3)]] for line in listes[i][::(i==3)+(i==2)-(i==1)-(i==0)]] :
                    y+=1
                    x=0
                    for e in line[:k:] :
                        x+=1

                        if test :
                            afficherMap(care)

                        if e == "." :
                            newpos=(pos[0]+x*((i==1)+(i==2)-(i==3)-(i==0)),pos[1]+y*((i==3)+(i==2)-(i==1)-(i==0))) #Pos réel au sein de self.map de la zone à couvrir
                            if frag :
                                [HG,HD,BD,BG][i].append(newpos)
                            else :
                                final.append(newpos)
                            if test :
                                care[newpos[1]-carePos[1]][newpos[0]-carePos[0]]="C"

                        elif e == "#" :
                            k=x-1
                            break

            if test :
                afficherMap(care)
            if not test :
                if frag :
                    return [[pos],HG,H,HD,D,BD,B,BG,G]
                else :
                    return final
        else :
            return []

    def addBorne(self,pos) :
        """Ajout ou suppression d'un routeur sur la carte.
        Args :
            pos [y, x]: coordonnées de la cellule.
        """
        for e in self.couverture(pos) :
            self.nbCaseCouverte+=1
            self.map[e[1]][e[0]]="C"
        self.map[pos[1]][pos[0]]="R"
        self.nbRouteur+=1
        self.posRouteurs.append([pos[1],pos[0]])


    def _inMap(self, y, x):
        """Vérifie si les coordonnées sont correctes (dans les limites de la carte).
        Args :
            y entier: coordonnée y de la cellule.
            x entier: coordonnée x de la cellule.
        Return :
            True si les coordonnées sont correctes, False sinon.
        """
        return ((y > 0 and y < self.nbLig ) and (x > 0 and x < self.nbCol))

    def presBackbone(self, pos):
        """Vérifie si un backbone est présent dans la cellule indiquée par ses coordonnées.
        Args :
            pos [y, x]: coordonnées de la cellule.
        Return :
            True si un backbone est présent, False sinon.
        """
        return pos in self.posBackbones

    def presCellCouverte(self, pos):
        """Vérifie si la cellule indiquée par ses coordonnées est couverte ou non.
        Args :
            pos [y, x]: coordonnées de la cellule.
        Return :
            True si la cellule est couverte, False sinon.
        """
        return pos in self.cellCouverte

    def presRouteur(self, pos):
        """Vérifie si un routeur est présent dans la cellule indiquée par ses coordonnées.
        Args :
            pos [y, x]: coordonnées de la cellule.
        Return :
            True si un routeur est présent, False sinon.
        """
        return pos in self.posRouteurs

    def vide(self, posY, posX):
        """Vérifie si la cellule indiquée par ses coordonnées est vide ou non.
        Args :
            posY entier: coordonnée y de la cellule.
            posX entier: coordonnée x de la cellule.
        Return :
            True si la cellule est vide, False sinon.
        """
        return self.map[posY][posX] == "-"

    def mur(self, posY, posX):
        """Vérifie si un mur se trouve sur aux coordonnées indiquées.
        Args :
            posX entier: coordonnée x de la cellule.
            posY entier: coordonnée y de la cellule.
        Return :
            True si un mur est présent, False sinon.
        """
        return (self._inMap(posY, posX) and self.map[posY][posX] == "#")

    def setPosJoueur(self, y, x):
        """Modifie la position courante du pointeur (interface graphique).
        Args :
            posY entier: coordonnée y du pointeur.
            posX entier: coordonnée x du pointeur.
        """
        if(not(self.mur(self.posJoueur[0] + y, self.posJoueur[1] + x))):
            self.posJoueur[0] += y
            self.posJoueur[1] += x

    def pourcentageCaseCouverte(self):
        """Calcule le pourcentage de cellules couvertes sur la carte.
        Return :
            Un nombre décimal représentant le pourcentage de cellules couvertes.
        """
        return ((self.nbCaseCouverte * 100) / self.nbCaseCouvrable())

    def nbCaseCouvrable(self):
        """Calcule le nombre de cellules couvrables sur la carte.
        Return :
            Un nombre entier indiquant le nombre de cellules couvrables.
        """
        nbCase = 0
        for ligne in self.map:
            for element in ligne:
                if(element == "."):
                    nbCase += 1
        return nbCase

    def dansBudget(self):
        """Vérifie si le budget est respecté ou non suivant les dépenses effectuées.
        Return :
            True si le budget est respecté, False sinon.
        """
        return (self.budget - self.cout() >= 0)

    def cout(self):
        """Calcule le coût des équipements installés sur la carte.
        Return :
            Un nombre entier indiquant le coût total des installations.
        """
        return (self.nbBackbone * self.backboneCost + self.nbRouteur * self.routerCost)

    def score(self):
        """Calcule le score obtenu suivant les règles du Google HashCode.
        Return :
            Un nombre entier positif indiquant le score, -1 sinon.
        """
        if(self.dansBudget()):
            return (1000 * self.nbCaseCouverte + (self.budget - self.cout()))
        else:
            return -1



    def getMap(self):
        """Retourne l'affichage de la carte avec des symboles représentant
        les différents équipements installés :
            B : cellule contenant backbone initial,
            H : position courante du curseur,
            R : cellule contenant un routeur,
            * : cellule contenant un backbone,
            ° : cellule couverte par un routeur.
        Return :
            Une chaîne de caractères contenant l'ensemble des cellules de
            la carte et les équipements installés.
        """
        carte = ""
        y = 0
        for ligne in self.map:
            x = 0
            lig = ""
            for element in ligne:
                if(y == self.backboneInit[0] and x == self.backboneInit[1]):
                    lig += "B"
                elif(y == self.posJoueur[0] and x == self.posJoueur[1]):
                    lig += "H"
                elif(self.presRouteur([y, x])):
                    lig += "R"
                elif(self.presBackbone([y, x])):
                    lig += "*"
                elif(self.presCellCouverte([y, x])):
                    lig += "°"
                else:
                    lig += element
                x+= 1
            carte += lig + '\n'
            y += 1
        return carte

    def __str__(self):
        """Retourne l'affichage de la carte.
        Return :
            Une chaîne de caractères contenant l'ensemble des cellules de la carte.
        """
        string = ""
        for line in self.map :
            for e in line :
                string += str(e)
            string += '\n'
        return string


    def generationOUT(self):
        """Génère un fichier de sortie contenant le nombre et les coordonnées
        des équipements installés sur la carte. Le fichier prenant comme nom
        le nom de la carte traitée "nomCarte.out".
        """
        with open(self.nomCarte + ".out", 'w+') as file:
            file.write(str(self.nbBackbone) + '\n')
            for backbone in self.posBackbones:
                if(backbone != self.backboneInit):
                    file.write(str(backbone[0]) + " " + str(backbone[1]) + "\n")
            file.write(str(self.nbRouteur) + '\n')
            for routeur in self.posRouteurs:
                file.write(str(routeur[0]) + " "+ str(routeur[1]) + "\n")

    def generationIN(self):
        """ Charge un fichier de sortie et affecte aux différents attributs de la carte,
        les valeurs contenues dans ce fichier (nombre et position des routeurs et backbones).
        """
        self.reset()
        cheminFichier = askopenfilename(filetypes=[("Fichier de sortie", ".out")], title="Selection d'un fichier de sortie")
        if(not(cheminFichier)):
            return
        fichier = open(cheminFichier, "r")

        nbLigne = 0
        nbSoloNumber = 0
        nbElementAttendu = 0
        nbElement = 0

        for ligne in fichier:
            ligne = ligne.split()
            if(nbLigne == 0):
                if(len(ligne) == 1):
                    self.nbBackbone = int(ligne[0])
                    nbSoloNumber += 1
                else:
                    raise Exception("Il faut préciser le nombre de backbones.")
            else:
                if(len(ligne) == 2):
                    if(nbSoloNumber == 1):
                        self.posBackbones.append([int(ligne[0]), int(ligne[1])])
                    else:
                        self.posRouteurs.append([int(ligne[0]), int(ligne[1])])
                        #self.calculZoneCouverte([int(ligne[0]), int(ligne[1])])
                    nbElement += 1
                elif(len(ligne) == 1):
                    if(nbElement != self.nbBackbone):
                        raise Exception("Incohérence entre le nombre de backbones et le nombre de coordonnées de backbones.")
                    self.nbRouteur = int(ligne[0])
                    nbSoloNumber += 1
                    nbElement = 0
                else:
                    if(len(ligne) > 2):
                        raise Exception("Trop de coordonnées")
                    if(len(ligne) == 0):
                        raise Exception("Ligne vide")
            if(nbLigne % 100 == 0):
                print(nbLigne)
            nbLigne += 1

        fichier.close()

        if(nbSoloNumber > 2):
            raise Exception("Trop de chiffres tout seul")
        elif(nbSoloNumber == 1):
            raise Exception("Nombre de routeurs non défini")
        elif(nbSoloNumber == 2 and nbElement != self.nbRouteur):
            raise Exception("Incohérence entre le nombre de routeurs et le nombre de coordonnées de routeurs")


def clavier(event):
    """
    Permet de gérer les différentes actions que l'on peut effectuer sur la carte en mode graphique).
    Args :
        event : Evénement lié à la touche actionnée par l'utilisateur.
    """
    touche = event.keysym
    if(touche == "Up"):
        carte0.setPosJoueur(-1, 0)
    elif(touche == "Down"):
        carte0.setPosJoueur(1, 0)
    elif(touche == "Left"):
        carte0.setPosJoueur(0, -1)
    elif(touche == "Right"):
        carte0.setPosJoueur(0, 1)
    elif(touche == "space"):
        carte0.addDelRouteur()
    elif(touche == "b"):
        backboneGeneration_1(carte0)
    elif(touche == "x"):
        backboneGeneration_2(carte0)
    elif(touche == "r"):
        carte0.reset()
    elif(touche == "Return"):
        carte0.generationOUT()
    elif(touche == "o"):
        carte0.generationIN()
    srt.set(carte0.getMap())

if __name__ == "__main__":
    from tkinter import *
    from tkinter import ttk
    from tkinter.filedialog import *

    carte0 = Carte("../cartes/mapTest_1.in")
    """carte0 = Carte("charleston_road.in")
    carte2 = Carte("rue_de_londres.in")
    carte3 = Carte("opera.in")
    carte4 = Carte("lets_go_higher.in")
    """

    root = Tk()

    srt = StringVar()
    srt.set(carte0.getMap())

    frameExt = Frame(root)
    canvas = Canvas(frameExt, height=500, width=1000)
    frameInt = ttk.Frame(canvas)
    scrollY = ttk.Scrollbar(frameExt, orient='vertical', command=canvas.yview)
    scrollX = ttk.Scrollbar(frameExt, orient='horizontal', command=canvas.xview)
    canvas.configure(yscrollcommand=scrollY.set, xscrollcommand=scrollX.set)

    frameExt.grid(),
    canvas.grid(row=1, column=0, sticky='nesw')
    scrollY.grid(row=1, column=1, sticky='nes')
    scrollX.grid(row=2, sticky='esw')
    canvas.create_window(0, 0, window=frameInt, anchor='nw')
    ttk.Label(frameInt, textvariable=srt, font=("Courier New", 12)).grid(sticky='nesw')

    canvas.focus_set()
    canvas.bind("<Key>", clavier)

    root.mainloop()
