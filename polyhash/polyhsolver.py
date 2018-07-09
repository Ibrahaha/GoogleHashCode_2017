#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Module de résolution du problème de placement de bornes wifi
    posé par le projet Poly#.
    Usage:

    >>> from polyhash import solve
    >>> solve(nomDuFichierEntre) # Fichier contenu dans le dossier cartes à la racine du projet
"""


__all__ = ['creationMapPuissance', 'backboneGeneration_1', 'backboneGeneration_2', 'solve']  # ajouter dans cette liste tous les symboles 'importables'


from polyhutils import *
from polyhmodel import Carte
import time
import csv
import os
import shutil
import threading
import statistics
import sys

#NOMBRE_THREADS peut être modifié mais ne doit jamais être supérieur au nombre de routeurs sur la map
NOMBRE_THREADS = 10
sys.setrecursionlimit(10000)

#--------------------------fonction sur le nombre de routeurs sans les classes------------------------------------------------------------------------------------------------------
def Nbre_routeur(budget,cout_routeur,cout_backbone):
    return(budget//(cout_routeur+cout_backbone)) #on suppose que pour chaque routeur, on a un backbone


#-------------------------foncton de verification-----------------------------------------------------------------------------------------------------------------------------------
def verif_coord(liste_points, point):
    "fonction verifiant si un point existe dans la liste des points liste_points"
    n=len(liste_points)
    if liste_points==[]: #si la liste est vide alors c'est vrai
        return False
    else:
        for i in range(n):
            if liste_points[i][0]!=point[0]: #on verifie d'abord si l'abscisse est la meme
                 return False  #alors le point n'est pas dans la liste
            elif liste_points[i][0]==point[0] :

                 if liste_points[i][1]==point[1]: # on verifie l' ordonnées est la meme
                     return True
                 else:      #cas ou l'ordonnée n est pas la meme donc ce n'est pas le
                    return False

#-------------- Verifie que le routeur ne va pas couvrir la couverture d'un autre routeur de la liste des routeurs ------------------------------------------------------------------
def estTropPretAutreRouteur(x,y,listeRouteurs,mapfile, radius):
    """
        x,y : coordoonnées du routeur à poser
        listeRouteurs : la liste des routeurs déja posés
        mapfile : la map de la carte
        radius : rayon de couverture d'un routeur
        return True s'il couvre la couverture d'une autre routeur, False sinon
    """
    result= False
    for i in range (listeRouteurs.len()):
        if x+(2*radius) >= listeRouteurs[i][0] or x-(2*radius) <= listeRouteurs[i][0] or y+(2*radius) >= listeRouteurs[i][1] or y-(2*radius) <= listeRouteurs[i][1]:
            result=True
    return result #WORK IN PROGRESS, FONCTION NON TESTEE




#---------------------------------Fonction de placement de routeur aleatoirement sur une map-----------------------------------------------------------------------------------------
def genere_coord(larg_map,long_map,carte):
    "Fonction generant un couple de coordonnées compris dans la map"
    "Je suppose que l'axe des abscisses est celui suivant la largeur de la map et celui des ordonnées est suivant la longueur de la map"

    liste_coord=[]
    nbre_routeur=Nbre_routeur(budget,cout_routeur,cout_backbone) #il faut connaitre le nombre des routeurs à placer
    cpt=0 #compteur


    while cpt!=nbre_routeur:

        x=random.randint(0,larg_map) #on utilise des coordonnées entieres car la carte est un plan discret
        y=random.randint(0,long_map)
        point=[x,y]
        if carte[x][y]==".":       #on verifie bien qu'on tombe sur un espace vide et pas sur un mur ou en dehors du batiment
            if  verif_coord(liste_coord, point)==False: #on verifie que le point n'est deja dans la liste des coordonnées

                 liste_coord.append([x,y])
                 cpt+=1
            else:
                pass
        else:
            pass

    return liste_coord


#----------------------------------calcul du nombre de routeurs avec les  classes si plutard on veut rajouter des methodes liés au placement de routeurs--------------------------------------------------------------------
class Nrouteurs:
    "Class sur le nombre de routeurs par budget et par map en supposant que chaque routeur est relié par un backbone"

    def __init__(self,budget,cout_routeur,cout_backbone):
        self.budget=budget
        self.cout_routeur=cout_routeur
        self.cout_backbone=cout_backbone


    def Nbre_routeur(self):

        nbre=(self.budget//(self.cout_routeur+self.cout_backbone))
        return nbre


#---------------------------------------------------------------------------------------------------------------------------------------

def creationMapCouvertures(carte,test=False) :
    """Fonction qui retourne une liste de liste calquant la map donnée mais avec
     sur chaque case, le nombre de cases qu'on couvrirait si on mettait une borne(routeur) dessus
     Arg :
        carte : liste de liste de caractère représentant la carte que l'on souhaite avoir en tant que map de couvertures
        time : bool que l'on met True si l'on souhaite avoir le temps d'éxécution (qui peut être long) de cette fonction
    """
    if test :
        debut = time.time()
    M=[]
    for y in range(len(carte.map)) :
        M.append([])
        for x in range(len(carte.map[y])) :
            if carte.map[y][x]=="." :
                M[y].append(len(carte.couverture((x,y))))
            else :
                M[y].append(0)
    if test :
        fin = time.time()
        print("Temps :",fin-debut)
    return M


def updateMapCouvertures(carte,mapCouvertures,pos) :
    """Fonction retournant la map de couvertures données en la mettant à jour selon si l'on mettant un routeur en position pos
    Args :
        mapCouvertures : liste de liste de int correspondant à la map de couvertures
        pos : (x,y) représentant la position du routeur que l'on souhaite rajouté dans la map initiale
    Return :
        VOID mapCouvertures mise à jour
    """
    updateZone,uPos=carre(mapCouvertures,pos,2*carte.radius)
    #afficherMap(updateZone)
    for y in range(len(updateZone)) :
        for x in range(len(updateZone[0])) :
            if updateZone[y][x] != 0 :
                mapCouvertures[uPos[1]+y][uPos[0]+x] = len(carte.couverture((uPos[0]+x,uPos[1]+y)))

def backboneGeneration(carte, numero = 0):
    """Generation des backbones.
    Args :
        carte : objet Carte.
        numero : Indique si le bugdet va etre depasse (0-->budget va etre depasse sinon 1)
    """
    if(numero == 0):
        lst = backboneGeneration_1(carte)
        carte.posBackbones = lst
        carte.nbBackbone = len(carte.posBackbones)
        print("ALGO KRUSKAL", len(carte.posBackbones))
    else:
        # Initialisation des variables
        nbBackbone_1 = -1
        nbBackbone_2 = -2
        backboneCommun = True
        nbRouteur = carte.nbRouteur
        posRouteurs = copy(carte.posRouteurs)
        lstBackboneCommun = []
        lstBackbone_1 = []
        lstBackbone_2 = []
        lstBackbone_1_final = []
        lstBackbone_2_final = []

        lstBackbone_2 = backboneGeneration_2(carte)
        nbBackbone_2 = len(lstBackbone_2)

        # Boucle de comparaison des algorithme
        while(nbBackbone_1 != nbBackbone_2 and backboneCommun):
            backboneCommun = False
            del lstBackbone_1
            t = time.time()
            lstBackbone_1 = backboneGeneration_1(carte)
            elapsed_time = time.time() - t
            print("ALGO KRUSKAL", elapsed_time, len(lstBackbone_1))

            if(len(lstBackbone_1) < len(lstBackbone_1_final) or len(lstBackbone_1_final) == 0):
                lstBackbone_1_final = lstBackbone_1
                print("Nb backbones =", len(lstBackbone_1_final))
                ajoutRouteur = False

                # Ajout des routeurs retirés si c'est possible
                while((carte.budget - ((nbRouteur + 1)*carte.routerCost + (len(lstBackbone_1_final) + len(lstBackbone_1_final)//nbRouteur) * carte.backboneCost) > 0) and len(carte.posRouteursPop) > 0):
                    newRouteur = carte.posRouteursPop.pop()
                    print(newRouteur)
                    nbRouteur += 1
                    carte.nbRouteur += 1
                    posRouteurs.append(newRouteur)
                    carte.posRouteurs.append(newRouteur)
                    ajoutRouteur = True
                if(ajoutRouteur):
                    lstBackbone_1_final = []
                    lstBackbone_2 = backboneGeneration_2(carte)
                    nbBackbone_2 = len(lstBackbone_2)

            nbBackbone_1 = len(lstBackbone_1)

            t = time.time()
            # Recherche des backbones en commun
            for element in lstBackbone_2:
                meilleur = False
                if(element in lstBackbone_1 and not(element in carte.posRouteurs)):
                    if(not(meilleur) and not(element in carte.posRouteurs)):
                        carte.posRouteurs.append(element)
                        carte.nbRouteur += 1
                        backboneCommun = True
                    if(not(element in lstBackboneCommun)):
                        lstBackboneCommun.append(element)
            elapsed_time = time.time() - t
            print("BOUCLE FOR", elapsed_time)
        lstBackbone = lstBackbone_1_final
        carte.posRouteurs = posRouteurs
        carte.nbRouteur = nbRouteur
        carte.posBackbones = lstBackbone
        carte.nbBackbone = len(lstBackbone)

def backboneGeneration_2(carte):
    """Genere les backbones sur une map, base sur la recherche du backbone le plus proche.
    Args :
        carte : objet Carte.
    Return :
        Une liste de position de backbones.
    """
    if(carte.posRouteurs == []):
        return
    posRouteurs = copy(carte.posRouteurs)
    lstRouteurDist = []

    for position in posRouteurs:
        dist = calculDistancePos(carte.backboneInit, position)
        lstRouteurDist.append([position, dist])

    lstRouteurDist = sorted(lstRouteurDist, key=lambda x: x[1])
    lstBackbone = carte.posBackbones
    for lst in lstRouteurDist:
        lstBackbone = positionnementBackbone(carte, lst[0], lstBackbone)
    return lstBackbone

def generationBackboneKruskalFirstRouteur(carte):
    """Renvoi l'arete entre le backbone initial et le routeur le plus proche de celui-ci.
    Args :
        carte : objet Carte.
    Return :
        L'arete entre le backbone initial et le routeur le plus proche de celui-ci.
    """
    distance = float('inf')
    bestPos = []
    for position in carte.posRouteurs:
        dist = calculDistancePos(carte.backboneInit, position)
        if(dist < distance):
            distance = dist
            bestPos = position
    return [carte.backboneInit, bestPos]

def backboneGeneration_1(carte):
    """Calcul la position des backbones selon l'algorithme de Kruskal.
    Args :
        carte : objet Carte.
    Return :
        Une liste de position de backbones.
    """
    diviseur = 20 # Diviseur utilise pour separe la distance des aretes
    maximum = int(((calculDistancePos(carte.backboneInit, [carte.nbLig, carte.nbCol])/2) // diviseur) + 1) # Calcul de la distance maximale théorique
    # Creation du répertoire "Datafiles", et supression de tout son contenu
    if not os.path.exists("DataFiles"):
        os.mkdir("DataFiles")
    else:
        for filename in os.listdir("DataFiles"):
            os.remove("DataFiles/" + filename)
    if(carte.posRouteurs == []):
        return
    coupleRouteurs = []
    coupleRouteurs.append(generationBackboneKruskalFirstRouteur(carte)) # Genertion de la premiere arete
    t = time.time()

    # Initialisation des threads pour le calcul des arêtes
    threads=[]
    for i in range(NOMBRE_THREADS):
        posRouteurs = copy(carte.posRouteurs)
        backboneInit = [carte.backboneInit[0], carte.backboneInit[1]]
        thread = threading.Thread(target=calculDistribue, args=[posRouteurs, i, backboneInit, maximum])
        threads.append(thread)
        del posRouteurs
        del backboneInit

    # Start des threads
    for thread in threads:
        thread.start()
    # Attente de la fin des threads
    for thread in threads:
        thread.join()

    # Creation des fichiers csv "regroupé" par range de distance
    fichierCSV = []
    nbFiles = len(carte.posRouteurs)//diviseur
    for i in range(nbFiles):
        nom = str(i)
        fichierCSV.append(nom)
        file = open("DataFiles/" + nom + ".csv", "w")
        file.close()

    # Fusion des csv genere par les threads dans un fichier csv "regroupéé selon la range de distance
    for filename in os.listdir("DataFiles"):
        if("_" in filename):
            identificateur = filename.split("_")[0]
            for fichier in fichierCSV:
                if(chr(ord('A') + int(fichier)) == identificateur and not(filename == fichier + ".csv")):
                    fichier = fichier + ".csv"
                    shutil.copyfileobj(open("DataFiles/" + filename, 'r'), open("DataFiles/" + fichier, 'a'))
                    os.remove("DataFiles/" + filename)


    elapsed_time = time.time() - t
    print("CALCUL ARETES", elapsed_time)
    lst = kruskal(carte, fichierCSV) # Selection des aretes selon Kruskal
    for element in lst:
        if(not(element in coupleRouteurs)):
            coupleRouteurs.append(element)
    lstBackbone = algoPositionnementBackboneKruskal(carte, coupleRouteurs) # Generation de la position des backbones
    return lstBackbone

def calculDistribue(posRouteurs, numero, backboneInit, maximum):
    """Calcul le poids des aretes (distance entre 2 routeurs).
    Args :
        posRouteurs : liste contenant la position [y, x] de tous les routeurs.
        numero : nombre indiquant le numero du thread (id du thread).
        backboneInit {y,]: coordonnées du backbone initial.
        maximum : nombre indiquant la distance maximale théorique entre 2 routeurs.
    """
    diviseur = 20 # Diviseur utilise pour separe la distance des aretes
    # Creation des fichiers csv par range de distance
    fichierCSV = []
    for i in range(maximum):
        lettre = chr(ord('A') + i)
        nom = lettre + "_" + str(numero) + ".csv"
        fichierCSV.append(nom)
        file = open("DataFiles/" + nom, "a")
        file.close()

    # Calcul des borneMin et borneMax correspondant à l'intervalle de routeurs
    # dont le thread doit calculer les aretes
    borne_Min = numero *(len(posRouteurs) // NOMBRE_THREADS)
    borne_Max = (numero+1) * (len(posRouteurs) // NOMBRE_THREADS) - 1

    # Ouverture des fichiers csv
    lstFile = []
    for i in range(len(fichierCSV)):
        file = open("DataFiles/" + fichierCSV[i],'a')
        lstFile.append(file)
    # Calcul du poids des aretes (distance entre 2 routeurs)
    for j in range(borne_Min, borne_Max + 1): # Boucle qui parcourt un intervalle de routeurs
        for i in range(j, len(posRouteurs) + 1): # Boucle qui parcourt tous les routeurs
            if(i != j):
                routeur_1 = posRouteurs[j]
                if(i == len(posRouteurs)):
                    routeur_2 = backboneInit
                    numeroRouteur = 0
                else:
                    routeur_2 = posRouteurs[i]
                    numeroRouteur = i + 1
                if(routeur_1 != routeur_2):
                    distance = calculDistancePos(routeur_2, routeur_1) # Calcul de la distance entre 2 routeurs
                    index = int(distance // diviseur)
                    if(index < len(fichierCSV)):
                        # Ajout des numeros des 2 routeurs et la distance entre eux dans un fichier csv 
                        out = lstFile[index]
                        csv_out=csv.writer(out, delimiter=';', lineterminator='\n')
                        csv_out.writerow([calculDistancePos(routeur_1, routeur_2), j + 1, numeroRouteur])
    # Fermeture des fichiers
    for i in range(len(lstFile)):
        lstFile[i].close()


def algoPositionnementBackboneKruskal(carte, coupleRouteurs):
    """Positionnement des backbones.
    Args :
        carte : objet Carte.
        coupleRouteurs : liste contenant les couples routeurs selectionnes via Kruskal.
    Return :
        Une liste de position de backbones.
    """
    lst = []
    rangementConnexion(carte.backboneInit, coupleRouteurs, lst) # Réordonnancement des aretes pour l'arbitre
    lstBackbone = []
    # Calcul de la position des bacbones pour tous les couples
    for couple in lst:
        lstBackbone = positionnementBackboneKruskal(carte, couple[0], couple[1], lstBackbone)
    return lstBackbone

def rangementConnexion(noeud, coupleRouteurs, lst):
    """Réordonnancement des aretes pour l'arbitre.
    Args :
        noeud [y, x]: position du noeud pour la recherche du routeur suivant.
        coupleRouteurs : liste contenant les couples routeurs selectionnes via Kruskal.
        lst : liste contenant les couples routeurs dans l'ordre.
    """
    index = 0
    # Parcourt de tous les couples routeurs 
    for couple in coupleRouteurs:
        if(noeud in couple):
            if(noeud == couple[1]):
                couple[0], couple[1] = couple[1], couple[0]
            lst.append(couple)
            noeudAVerif_1 = couple[1]
            noeudAVerif_2 = couple[0]
            del coupleRouteurs[index]
            rangementConnexion(noeudAVerif_1, coupleRouteurs, lst)
            rangementConnexion(noeudAVerif_2, coupleRouteurs, lst)
        index += 1

def positionnementBackboneKruskal(carte, posRouteur1, posRouteur2, lstBackbone):
    """Positionnement des backbones pour l'algorithme de Kruskal.
    Args :
        carte : objet Carte.
        posRouteur1 [y, x]: coordonnées du premier routeur.
        posRouteur2 [y, x]: coordonnées du second routeur.
        lstBackbone : liste contenant la position de tous les routeurs.
    Return :
        Une liste de position de backbones.
    """
    posYRouteur_1 = posRouteur2[0]
    posXRouteur_1 = posRouteur2[1]

    posYRouteur_2 = posRouteur1[0]
    posXRouteur_2 = posRouteur1[1]

    a = posXRouteur_2
    b = posYRouteur_2

    # Calcul de position des backbones
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
        # Ajout du backbones si il n'existe pas deja
        if(not([b, a] in lstBackbone) and not([b, a] == carte.backboneInit)):
            lstBackbone.append([b, a])
    return lstBackbone

def kruskal(carte, fichierCSV):
    """Algorithme de kruskal.
    Args :
        carte : objet Carte.
        fichierCSV : liste contenant le nom de tous les fichiers csv.
    Return :
        Une liste de couple routeurs.
    """
    tableau = [i + 1 for i in range(carte.nbRouteur + 1)] # Creation d'un tableau contenant le numero des composantes connexes
    coupleRouteur = []
    # Parcourt des fichiers csv (selon la range de distance)
    for i in range(len(fichierCSV)):
        with open("DataFiles/" + fichierCSV[i] + ".csv", newline='') as fin:
            reader = csv.reader(fin, delimiter=';')
            reader = sorted(reader, key=lambda x: float(x[0])) # Tri du fichier csv ouvert selon le poids des aretes
            for row in reader:
                num_1 = int(row[1]) # Recuperation du numero du routeur 1
                num_2 = int(row[2]) # Recuperation du numero du routeur 2
                numero_1 = tableau[num_1] # Recuperation du numero de la composante connexe du routeur 1
                numero_2 = tableau[num_2] # Recuperation du numero de la composante connexe du routeur 2
                # Algorithme de Kruskal
                if(numero_1 != numero_2):
                    newNumero = min(numero_1, numero_2)
                    oldNumero = max(numero_1, numero_2)
                    for j in range(len(tableau)):
                        if(tableau[j] == oldNumero):
                            tableau[j] = newNumero
                    if(num_1 == 0):
                        coupleRouteur.append([carte.backboneInit, carte.posRouteurs[num_2 - 1]])
                    elif(num_2 == 0):
                        coupleRouteur.append([carte.posRouteurs[num_1 - 1], carte.backboneInit])
                    else:
                        coupleRouteur.append([carte.posRouteurs[num_1 - 1],  carte.posRouteurs[num_2 - 1]])

                if(endKruskal(tableau)): # Detection de la fin de l'algorithme
                    break
    return coupleRouteur

def endKruskal(tableau):
    """Indique si l'algorithme de Kruskal est fini ou non.
    Args :
        tableau : tableau contenant le numero des composantes connexes.
    Return :
        True si toutes les composantes connexes ont le meme numero sinon False.
    """
    numero = tableau[0]
    for element in tableau:
        if(element != numero):
            return False
    return True

def triSelection(aretes, poids):
    """Tri de deux liste simultanement (NON UTILISE)
    Args :
        aretes : tableau contenant les couples routeurs (aretes).
        poids : tableau contenant le poids des aretes.
    Return :
        Les listes triées.
    """
    n = len(poids)
    for i in range(n-1):
        j = i
        for k in range(i+1,n):
            if(poids[k] < poids[j]):
                j = k
        poids[i], poids[j] = poids[j], poids[i]
        aretes[i], aretes[j] = aretes[j], aretes[i]
    return aretes, poids

def generationMatriceGrapheK(carte):
    """Generation d'une matrice avec le poids de chaque arete (NON UTILISE)
    Args :
        carte : objet Carte.
    Return :
        Une matrice de distance entre 2 routeurs.
    """
    matrice = [[0 for i in range(carte.nbRouteur + 1)] for i in range(carte.nbRouteur + 1)]
    backBonePos = carte.backboneInit
    index = 1
    for element in carte.posRouteurs:
        distance = calculDistancePos(backBonePos, element)
        matrice[index][0] = distance
        matrice[0][index] = distance
        index += 1

    for i in range(len(carte.posRouteurs)):
        for j in range(i + 1, len(carte.posRouteurs)):
            distance = calculDistancePos(carte.posRouteurs[i], carte.posRouteurs[j])
            matrice[i+1][j+1] = distance
            matrice[j+1][i+1] = distance
    return matrice


def rechercheBackbone(carte, posRouteur, lstBackbone):
    """Recherche du backbone le plus proche du routeur
    Args :
        carte : objet Carte.
        posRouteur [y,x]: coordonnee du routeur.
        lstBackbone : liste contenant la position de tous les backbones.
    Return :
        La coordonnee du backbone.
    """
    distance = float('inf')
    bestPos = []
    for position in lstBackbone:
        dist = calculDistancePos(posRouteur, position)
        if(dist < distance):
            distance = dist
            bestPos = position
    return bestPos

def positionnementBackbone(carte, posRouteur, lstBackbone):
    """Positionnement des backbones pour l'algorithme de Kruskal.
    Args :
        carte : objet Carte.
        posRouteur : liste contenant la position de tous les routeurs.
        lstBackbone : liste contenant la position de tous les backbones.
    Return :
        Une liste de position de backbones.
    """
    posYRouteur = posRouteur[0]
    posXRouteur = posRouteur[1]

    n = len(lstBackbone)

    if(n == 0):
        posYBackbone = carte.backboneInit[0]
        posXBackbone = carte.backboneInit[1]
    else:
        pos = rechercheBackbone(carte, posRouteur, lstBackbone) # Recherche du backbone le plus proche du routeur
        posYBackbone = pos[0]
        posXBackbone = pos[1]

    a = posXBackbone
    b = posYBackbone

    # Calcul de position des backbones
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

        # Ajout du backbones si il n'existe pas deja
        if(not([b, a] in lstBackbone) and not([b, a] == carte.backboneInit)):
            lstBackbone.append([b, a])
    return lstBackbone
def takeCouv(couv):
    """ Renvoie le 1er élément d'une liste. Fonction Utilisée par sorted pour trier sur
    le premier element des triplets de la liste des couvertures.
    Args :
        couv [] : la liste concernée
    """
    return couv[0]

def TriCouv(mapCouvertures):
    """Renvoie la liste des cases triées selon la valeur de couverture potentielle.
    Un élément de la liste est un triplet comprenant dans l'ordre :
    le nombre de cases possibles à couvrir, l'abscisse et l'ordonnée de la case.
    Args :
        mapCouvertures [] : matrice contenant les potentiels des couvertures des cases.
    """
    liste = []
    for i in range(len(mapCouvertures)):
        for j in range(len(mapCouvertures[0])):
            l = []
            l.append(mapCouvertures[i][j])
            l.append(i)
            l.append(j)
            liste.append(l)
    return sorted(liste, reverse=True,key=takeCouv)

def posAutourPosition(pos, pos_centrale, multi, carte):
    """Indique, pour une position donnée, si elle est située au-delà ou en-dessous
    d'un certain nombre de radius d'une carte, par rapport à une position centrale.
    Args :
        pos [x, y] : coordonnées de la position en question
        pos_centrale [x, y] : coordonnées de la position centrale
        multi int : indique à combien de radius on souhaite rechercher la position
        carte Carte : carte sur laquelle doivent se trouver les positions à comparer
    """
    rayon  = carte.radius * multi
    if pos != [] and pos_centrale != [] and rayon > 0:
        borneMinX = max(pos_centrale[0] - rayon, 0)
        borneMaxX = min(pos_centrale[0] + rayon, carte.nbLig-1)
        borneMinY = max(pos_centrale[1] - rayon, 0)
        borneMaxY = min(pos_centrale[1] + rayon, carte.nbCol-1)

        return pos[1] >= borneMinX and pos[1] <= borneMaxX and pos[0] >= borneMinY and pos[0] <= borneMaxY
        
        
def solve2(nom_fichier_entre) : 
    chemin_carte = "../cartes/" + nom_fichier_entre
    carte = Carte(chemin_carte)
    score=[]
    M=creationMapCouvertures(carte)
    afficherMap(M)
    L=TriCouv(M)
    def recur(carte,M,L) :
        if carte.dansBudget() or True :
            if L[0][0] != 0 : 
                cpt=0
                while L[cpt][0] == L[cpt+1][0]:
                    cpt += 1
                    if cpt >= len(L)-1 :
                        break
                for e in L[0:cpt+1] :
                    pos=(e[2],e[1])
                    ccarte=copy.deepcopy(carte)
                    ccarte.addBorne(pos)
                    MC=M[::]
                    updateMapCouvertures(ccarte,MC,pos)
                    recur(ccarte,MC[::],TriCouv(MC))
            else :
                afficherMap(carte.map)
        else :
            afficherMap(carte.map)
    recur(carte,M,L)

def solve(nom_fichier_entre):
    """Permet, à partir d'un fichier d'entrée adapté, de positionner les routeurs puis les backbones
    le plus efficacement possible.
    Args :
        nom_fichier_entre String : nom du fichier d'entrée à ajouter dans le dossier
                                   carte au niveau de la racine du projet
    """
    chemin_carte = "../cartes/" + nom_fichier_entre
    carte = Carte(chemin_carte)

    print("Création de la carte de couverture initiale")
    t = time.time()
    M = creationMapCouvertures(carte, test=False)
    elapsed_time = time.time() - t
    print(elapsed_time)

    print("Placement des routeurs")
    t = time.time()

    sous_liste = []
    nbBackboneMoy = 0
    # On va rajouter les routeurs tant qu'il nous reste du budget
    while carte.budget-carte.cout() > 0:

        sous_liste = []

        L=TriCouv(M) # Tri des cases selon leur couverture potentielle
        if L[0][0]<=0 :
            break

        # On regarde combien de cases pourraient couvrir le même nombre de cases que la première
        cpt = 0

        while L[cpt][0] == L[cpt+1][0]:
            cpt += 1

        if cpt != 0:
            pos = []
            couverture_max = L[0][0]
            sous_liste = L[0:cpt+1]

            while len(sous_liste) > 0 and carte.budget-carte.cout() > 0:
                # Initialisation des différents éléments de comparaison des cases quand leurs couvertures sont identiques
                minimum_moy = float("inf")  # Moyenne des couvertures des cases couvertes par une cellule
                minimum_med = float("inf")  # Médiane des couvertures des cases couvertes par une cellule
                minimum_dist = float("inf") # Distance de la case à un routeur de même couverture ou au backbone initial
                indice_minimum = -1
                i = 0
                cpt = len(sous_liste)

                while i < cpt:
                    case = sous_liste[i]
                    somme = 0
                    list_calc_med = []

                    if not M[case[1]][case[2]] == couverture_max:
                        # Si la couverture de la case a diminué, on la supprime
                        del sous_liste[i]
                        cpt -= 1

                    else:

                        if len(case) < 4:
                            # Si on a pas encore rajouté les informations au niveau des cases
                            case.append(-1) # Valeur par défaut pour la moyenne
                            case.append(-1) # Valeur par défaut pour la médiane
                            case.append(float("inf")) # Valeur par défaut pour la distance la plus proche de la case à un routeur présent


                        if case[3] == -1 or (pos != [] and posAutourPosition([case[2], case[1]], [pos[1],pos[0]], 3, carte)):
                            # Mise à jour des informations de comparaison
                            liste_cases_couvertes = carte.couverture((case[2],case[1]))
                            n = len(liste_cases_couvertes)
                            for j in range(n):
                                case_courante = liste_cases_couvertes[j]
                                valeurCourante = M[case_courante[1]][case_courante[0]]
                                if isinstance(valeurCourante, int):
                                    somme += valeurCourante
                                    list_calc_med.append(valeurCourante)
                            case[3] = somme
                            case[4] = median(list_calc_med)
                       
                        # Sélection de la case si elle possède un plus grand potentiel de couverture
                        # que les cases traitées auparavant
                        if case[3] < minimum_moy:
                            indice_minimum = i
                            minimum_moy = case[3]
                            minimum_med = case[4]
                            minimum_dist = case[5]

                        elif case[3] == minimum_moy:
                            if case[4] < minimum_med:
                                minimum_med = case[4]
                                minimum_dist = case[5]
                                indice_minimum = i


                            elif case[4] == minimum_med:
                                if case[5] < minimum_dist:
                                    minimum_dist = case[5]
                                    indice_minimum = i

                        i += 1

                # Ajout d'un routeur sur la case choisie auparavant parmi l'ensemble des cases de la liste
                if len(sous_liste) > 0:
                    pos=[sous_liste[indice_minimum][2],sous_liste[indice_minimum][1]]

                    # On met à jour la distance minimale de chaque case avec l'installation la plus proche (routeur ou backbone initial)
                    for i in range(cpt):
                        case = sous_liste[i]
                        dist_case_rout = min(calculDistancePos([case[1], case[2]], [pos[1], pos[0]]),
                        calculDistancePos([case[1], case[2]], [carte.backboneInit[1], carte.backboneInit[0]]))
                        if dist_case_rout < case[5]:
                            case[5] = dist_case_rout

                    del sous_liste[indice_minimum]
                    carte.addBorne(pos)
                    updateMapCouvertures(carte,M,pos)


        else:
            e = L.pop(0)
            pos=(e[2],e[1])
            carte.addBorne(pos)
            updateMapCouvertures(carte,M,pos)
            sous_liste = []

    del L
    elapsed_time = time.time() - t
    print(elapsed_time, carte.nbRouteur)
    carte.nbBackbone = 0

    carte.generationOUT()

    print("Placement des backbones")
    t = time.time()
    # Pose des backbones en fonction de si le budget va etre depassé ou non
    if(carte.budget-carte.cout() <= 0):
        backboneGeneration(carte, 0)
    else:
        backboneGeneration(carte, 1)
    elapsed_time = time.time() - t
    print(elapsed_time)
    print("Suppression de routeurs en trop")
    t = time.time()
    carte.generationOUT()
    nbSurplus = (carte.cout()-carte.budget) // carte.routerCost
    if nbSurplus == 0:
        nbSurplus += 1
    # Suppression des routeurs en trop
    if nbSurplus > 0:
        for i in range(nbSurplus):
            carte.posRouteursPop.append(carte.posRouteurs.pop())
            carte.nbRouteur -= 1
        carte.nbBackbone = 0
        carte.posBackbones = []
        backboneGeneration(carte, 1)
    elapsed_time = time.time() - t
    print(elapsed_time, carte.nbBackbone, carte.nbRouteur)

    carte.generationOUT()

    for filename in os.listdir("DataFiles"):
        os.remove("DataFiles/" + filename)

if __name__ == "__main__":
    print('solver')

    numero = input("Veuillez choisir une carte : \n 1. Charleston Road\n 2. Rue de Londres\n 3. Opéra\n 4. Lets go higher\nVotre choix : ")
    if(numero == str(1)):
        nom_fichier_entre = "charleston_road.in"
        solve(nom_fichier_entre)
    elif(numero == str(2)):
        nom_fichier_entre = "rue_de_londres.in"
        solve(nom_fichier_entre)
    elif(numero == str(3)):
        nom_fichier_entre = "opera.in"
        solve(nom_fichier_entre)
    elif(numero == str(4)):
        nom_fichier_entre = "lets_go_higher.in"
        solve(nom_fichier_entre)
    elif(numero == str(666)):
        nom_fichier_entre = "mapTest_1.in"
        solve2(nom_fichier_entre)
    else:
        print("Au revoir")
