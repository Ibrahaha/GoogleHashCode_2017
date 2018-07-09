import time
class carteObj():
    def __init__(self, cheminCarte):
        self.cheminCarte = cheminCarte
        self.nomCarte = ""
        self.nbCol = 0
        self.nbLig = 0
        self.radius = 0
        self.backboneCost = 0
        self.routerCost = 0
        self.budget = 0
        self.backboneInit = []
        self.map = []
        self.nbRouteur = 0
        self.nbBackbone = 0
        self.nbCaseCouverte = 0
        self.posJoueur = [0, 0]
        self.posRouteurs = []
        self.cellCouverte = []
        self.posBackbones = []
        self._generationCarte()

    def backboneGeneration_2(self):
        if(self.posRouteurs == []):
            return
        posRouteurs = self._copy(self.posRouteurs)
        distRouteurBackboneInit = []

        for position in posRouteurs:
            dist = self._calculDistancePos(self.backboneInit, position)
            distRouteurBackboneInit.append(dist)

        self._triSelection(posRouteurs, distRouteurBackboneInit)

        for coordonnees in posRouteurs:
            self.positionnementBackbone(coordonnees)

    def _copy(self, lst):
        copyLst = []
        nbElement = 0
        for liste in lst:
            copyLst.append([])
            for element in liste:
                copyLst[nbElement].append(element)
            nbElement += 1

        return copyLst

    def _generationBackboneKruskalFirstRouteur(self):
        distance = float('inf')
        bestPos = []
        for position in self.posRouteurs:
            dist = self._calculDistancePos(self.backboneInit, position)
            if(dist < distance):
                distance = dist
                bestPos = position
        return [self.backboneInit, bestPos]

    def backboneGeneration_1(self):
        if(self.posRouteurs == []):
            return
        coupleRouteurs = []
        coupleRouteurs.append(self._generationBackboneKruskalFirstRouteur())
        matrice = self._generationMatriceGrapheK()
        lstAretePoids = []
        for i in range(self.nbRouteur + 1):
            for j in range(i+1, self.nbRouteur + 1):
                lstAretePoids.append([[i, j], matrice[i][j]])
        lstAretePoids = sorted(lstAretePoids, key=lambda x: x[1])     
        lst = self._kruskal(lstAretePoids)
        for element in lst:
            if(not(element in coupleRouteurs)):
                coupleRouteurs.append(element)
        self._algoPositionnementBackboneKruskal(coupleRouteurs)

    def _algoPositionnementBackboneKruskal(self, coupleRouteurs):
        lst = []
        index = 0
        self._rangementConnexion(self.backboneInit, coupleRouteurs, lst)
        for couple in lst:
            self._positionnementBackboneKruskal(couple[0], couple[1])

    def _rangementConnexion(self, noeud, coupleRouteurs, lst):
        index = 0
        for couple in coupleRouteurs:
            if(noeud in couple):
                if(noeud == couple[1]):
                    couple[0], couple[1] = couple[1], couple[0]
                lst.append(couple)
                noeudAVerif_1 = couple[1]
                noeudAVerif_2 = couple[0]
                del coupleRouteurs[index]
                self._rangementConnexion(noeudAVerif_1, coupleRouteurs, lst)
                self._rangementConnexion(noeudAVerif_2, coupleRouteurs, lst)
            index += 1

    def _triBackbones(self):
        lstBackbones = []
        backbonePrec = self.backboneInit
        backboneSuiv = []

        for pos in self.posBackbones:
            backboneSuiv = pos
            if(self._backboneSuivant(backbonePrec, backboneSuiv)):
               lstBackbones.append(backboneSuiv)
               backbonePrec = backboneSuiv
            else:
               break

    def _chercheurSuivant(self, backbonePrec):
        pass


    def _backboneSuivant(self, backbonePrec, backboneSuiv):
        return ((backboneSuiv[0] == backbonePrec[0]) or (backboneSuiv[0] == backbonePrec[0] - 1) or (backboneSuiv[0] == backbonePrec[0] + 1) and (backboneSuiv[1] == backbonePrec[1]) or (backboneSuiv[1] == backbonePrec[1] - 1) or (backboneSuiv[1] == backbonePrec[1] + 1))


    def _positionnementBackboneKruskal(self, posRouteur1, posRouteur2):

        posYRouteur_1 = posRouteur2[0]
        posXRouteur_1 = posRouteur2[1]

        posYRouteur_2 = posRouteur1[0]
        posXRouteur_2 = posRouteur1[1]

        a = posXRouteur_2
        b = posYRouteur_2

        while(a != posXRouteur_1 or b != posYRouteur_1):
            if(a == posXRouteur_1):
                a = a
            elif(a > posXRouteur_1):
                a = a - 1
            elif(a < posXRouteur_1):
                a = a + 1

            if(b == posYRouteur_1):
                b = b
            elif(b > posYRouteur_1):
                b = b - 1
            elif(b < posYRouteur_1):
                b = b + 1

            self.addBackbone([b, a])

    def _kruskal(self, lst):
        tableau = [i + 1 for i in range(self.nbRouteur + 1)]
        coupleRouteur = []
        for i in range(len(lst)):
            numero_1 = tableau[lst[i][0][0]]
            numero_2 = tableau[lst[i][0][1]]
            if(numero_1 != numero_2):
                newNumero = min(numero_1, numero_2)
                oldNumero = max(numero_1, numero_2)
                for j in range(len(tableau)):
                    if(tableau[j] == oldNumero):
                        tableau[j] = newNumero
                if(lst[i][0][0] == 0):
                    coupleRouteur.append([self.backboneInit, self.posRouteurs[lst[i][0][1] - 1]])
                elif(lst[i][0][1] == 0):
                    coupleRouteur.append([self.posRouteurs[lst[i][0][0] - 1], self.backboneInit])
                else:
                    coupleRouteur.append([self.posRouteurs[lst[i][0][0] - 1],  self.posRouteurs[lst[i][0][1] - 1]])
            if(self._endKruskal(tableau)):
                break
        return coupleRouteur

    def _endKruskal(self, tableau):
        numero = tableau[0]
        for element in tableau:
            if(element != numero):
                return False
        return True

    def _triSelection(self, aretes, poids):

        n = len(poids)
        for i in range(n-1):
            j = i
            for k in range(i+1,n):
                if(poids[k] < poids[j]):
                    j = k
            poids[i], poids[j] = poids[j], poids[i]
            aretes[i], aretes[j] = aretes[j], aretes[i]
        return aretes, poids

    def _generationMatriceGrapheK(self):
        matrice = [[0 for i in range(self.nbRouteur + 1)] for i in range(self.nbRouteur + 1)]
        backBonePos = self.backboneInit
        index = 1
        for element in self.posRouteurs:
            distance = self._calculDistancePos(backBonePos, element)
            matrice[index][0] = distance
            matrice[0][index] = distance
            index += 1

        for i in range(len(self.posRouteurs)):
            for j in range(i + 1, len(self.posRouteurs)):
                distance = self._calculDistancePos(self.posRouteurs[i], self.posRouteurs[j])
                matrice[i+1][j+1] = distance
                matrice[j+1][i+1] = distance
        return matrice

    def _printMatrice(self, matrice):
        for element in matrice:
            print(element)

    def _calculDistancePos(self, pos1, pos2):
        res = 0
        for i in range(len(pos1)):
            res += (pos2[i]- pos1[i])**2
        res = res**0.5
        return res

    def _rechercheBackbone(self, posRouteur):

        distance = float('inf')
        bestPos = []
        for position in self.posBackbones:
            dist = self._calculDistancePos(posRouteur, position)
            if(dist < distance):
                distance = dist
                bestPos = position
        return bestPos

    def positionnementBackbone(self, posRouteur):
        posYRouteur = posRouteur[0]
        posXRouteur = posRouteur[1]

        n = len(self.posBackbones)

        if(n == 0):
            posYBackbone = self.backboneInit[0]
            posXBackbone = self.backboneInit[1]
        else:
            pos = self._rechercheBackbone(posRouteur)
            posYBackbone = pos[0]
            posXBackbone = pos[1]

        a = posXBackbone
        b = posYBackbone

        while(a != posXRouteur or b != posYRouteur):
            if(a == posXRouteur):
                a = a
            elif(a > posXRouteur):
                a = a - 1
            elif(a < posXRouteur):
                a = a + 1

            if(b == posYRouteur):
                b = b
            elif(b > posYRouteur):
                b = b - 1
            elif(b < posYRouteur):
                b = b + 1

            self.addBackbone([b, a])

    def addBackbone(self, pos):
        if(not(pos in self.posBackbones) and not(pos == self.backboneInit)):
            self.posBackbones.append(pos)
            self.nbBackbone += 1

    def reset(self):
        self.posRouteurs = []
        self.cellCouverte = []
        self.nbRouteur = 0
        self.nbBackbone = 0
        self.nbCaseCouverte = 0
        self.posBackbones = []

    def addCellCouverte(self, pos):
        if(not(pos in self.cellCouverte)):
            self.cellCouverte.append(pos)
            self.nbCaseCouverte += 1

    def calculZoneCouverte(self, pos):
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

    def _inMap(self, y, x):
        return ((y > 0 and y < self.nbLig ) and (x > 0 and x < self.nbCol))

    def presBackbone(self, pos):
        return pos in self.posBackbones

    def presCellCouverte(self, pos):
        return pos in self.cellCouverte

    def presRouteur(self, pos):
        return pos in self.posRouteurs

    def addDelRouteur(self):
        lst = [0, 0]
        lst[0] = self.posJoueur[0]
        lst[1] = self.posJoueur[1]
        if(lst in self.posRouteurs):
            self.posRouteurs.remove(lst)
            self.nbRouteur -= 1
        else:
            self.posRouteurs.append(lst)
            self.nbRouteur += 1
            #self.calculZoneCouverte(lst)
            #self.positionnementBackbone(lst)

    def vide(self, posY, posX):
        return self.map[posY][posX] == "-"

    def mur(self, posY, posX):
        return (self._inMap(posY, posX) and self.map[posY][posX] == "#")

    def setPosJoueur(self, y, x):
        if(not(self.mur(self.posJoueur[0] + y, self.posJoueur[1] + x))):
            self.posJoueur[0] += y
            self.posJoueur[1] += x

    def _generationCarte(self):
        fichier = open(self.cheminCarte, "r")

        ligne = " "
        nbLigne = 0

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

        lst = self.cheminCarte.split("/")
        self.nomCarte = lst[len(lst) - 1].split(".")[0]
        fichier.close()

    def pourcentageCaseCouverte(self):
        return ((self.nbCaseCouverte * 100) / self.nbCaseCouvrable())

    def nbCaseCouvrable(self):
        nbCase = 0
        for ligne in self.map:
            for element in ligne:
                if(element == "."):
                    nbCase += 1
        return nbCase

    def dansBudget(self):
        return (self.budget - self.cout() >= 0)

    def cout(self):
        return (self.nbBackbone * self.backboneCost + self.nbRouteur * self.routerCost)

    def score(self):
        if(self.dansBudget()):
            return (1000 * self.nbCaseCouverte + (self.budget - self.cout()))
        else:
            return -1

    def printCarte(self):
        y = 1
        for ligne in self.map:
            x = 1
            lig = ""
            for element in ligne:
                lig += element
                x+= 1
            print(lig)
            y += 1

    def getMap(self):
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

    def generationOUT(self):
        with open(self.nomCarte + ".out", 'w+') as file:
            file.write(str(self.nbBackbone) + '\n')
            for backbone in self.posBackbones:
                if(backbone != self.backboneInit):
                    file.write(str(backbone[0]) + " " + str(backbone[1]) + "\n")
                else:
                    print("WTF")
            file.write(str(self.nbRouteur) + '\n')
            for routeur in self.posRouteurs:
                file.write(str(routeur[0]) + " "+ str(routeur[1]) + "\n")

    def generationIN(self):
        self.reset()
        cheminFichier = askopenfilename(filetypes=[("Fichier de sortie", ".out")], title="Selection d'un fichier de sortie")
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

            nbLigne += 1

        fichier.close()

        if(nbSoloNumber > 2):
            raise Exception("Trop de chiffres tout seul")
        elif(nbSoloNumber == 1):
            raise Exception("Nombre de routeurs non défini")
        elif(nbSoloNumber == 2 and nbElement != self.nbRouteur):
            raise Exception("Incohérence entre le nombre de routeurs et le nombre de coordonnées de routeurs")

carte1 = carteObj("../cartes/mapTest_2.in") #carteObj("mapTest_1.in")
carte0 = carteObj("../cartes/charleston_road.in")
carte2 = carteObj("../cartes/rue_de_londres.in")
carte3 = carteObj("../cartes/opera.in")
carte4 = carteObj("../cartes/lets_go_higher.in")
#carte1.printCarte()

def clavier(event):
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
        carte0.backboneGeneration_1()
    elif(touche == "x"):
        carte0.backboneGeneration_2()
    elif(touche == "r"):
        carte0.reset()
    elif(touche == "Return"):
        carte0.generationOUT()
    elif(touche == "o"):
        carte0.generationIN()
    srt.set(carte0.getMap())


from tkinter import *
from tkinter import ttk
from tkinter.filedialog import *

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
