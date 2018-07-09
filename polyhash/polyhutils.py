#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Module des fonctions utilitaires utilisées dans les autres modules.
"""


__all__ = ['afficherMap', 'selection', 'carre', 'calculDistancePos', 'printMatrice', 'copy', 'median']  # ajouter dans cette liste tous les symboles 'importables'


def afficherMap(liste) :
    """Fonction qui transforme une liste en chaîne de caractère pour bien
     l'afficher et la print (affichage dans le shell de python).
     Args :
        liste []: liste à afficher.
    """
    separation = len(str(liste[0][0]))
    for line in liste :
        for e in line :
            if len(str(e)) > separation :
                separation = len(str(e))
    string=""

    for line in liste :
        for e in line :
            string+=str(e)+" "*(separation-(len(str(e)))+1)
        string+='\n'
    print(string)

def selection(L,posHG,tailleX,tailleY) :
    """Fonction qui renvoie la sélection d'un rectangle au sein d'une liste
     de listes (map).
     Args :
        L [] : liste à traiter.
        posHG entier: position haut-gauche du rectangle.
        tailleX entier: dimension du rectangle suivant l'axe des x.
        tailleY entier: dimension du rectangle suivant l'axe des y.
    Return :
        Une liste de listes contenant les éléments désirés.
    """
    return [[L[posHG[1]+i][posHG[0]+j] for j in range(0,tailleX)] for i in range(0,tailleY)]



def carre(L,pos,rad) :
    """Fonction qui renvoie la sélection (liste de liste) d'un carré de
    au sein d'une liste de listes (map).
    Args :
        L [] : liste à traiter.
        pos entier: centre du carré à renvoyer.
        rad entier: le carré à une demi-longueur (rad + 0.5).
    Return :
        Une liste de listes contenant les éléments désirés.
    """
    Carre = []
    h=len(L)
    w=len(L[0])
    debX = pos[0]-rad if pos[0]-rad <0 else 0
    debY = pos[1]-rad if pos[1]-rad <0 else 0
    for y in range(-rad-debY,rad+1) :
        if h>pos[1]+y>=0 :
            Carre.append([])
            for x in range(-rad-debX,rad+1) :
                if w>pos[0]+x>=0 :
                    Carre[y+rad+debY].append(L[pos[1]+y][pos[0]+x])

    return Carre,(pos[0]-rad-debX,pos[1]-rad-debY)


def calculDistancePos(pos1, pos2):
    """Calcule la distance entre deux points suivant leurs coordonnées.
    Args :
        pos1 [x,y]: les coordonnées du premier point.
        pos2 [x,y]: les coordonnées du second point.
    Return :
        Un nombre décimal correspondant à la distance entre les deux points.
    """
    res = 0
    for i in range(len(pos1)):
        res += (pos2[i]- pos1[i])**2
    res = res**0.5
    return res


def printMatrice(matrice):
    """Affiche le contenu d'une matrice.
    Args :
        matrice : La matrice à afficher.
    """
    for element in matrice:
        print(element)


def copy(lst):
    """Renvoie la copie d'une liste.
    Args :
        lst []: la liste à copier.
    Return :
        La copie de la liste, de type [].
    """
    copyLst = []
    nbElement = 0
    for liste in lst:
        copyLst.append([])
        for element in liste:
            copyLst[nbElement].append(element)
        nbElement += 1

    return copyLst


def median(liste):
    """Calcule la valeur médiane d'une liste de nombres.
    Args :
        liste []: la liste de nombres.
    Return :
        None si la liste est vide.
        Un nombre représentant la médiane de la liste sinon.
            - Si la longueur de la liste est paire, retourne la moyenne
            des deux éléments centraux de la liste.
            - Sinon, retourne l'élément central de la liste.
    """
    n = len(liste)
    liste_triee = sorted(liste)
    if n < 1:
        return None
    if n == 1:
        return liste_triee[0]
    if n % 2 == 1:
        return liste[n//2]
    else:
        return (liste_triee[n//2-1] + liste_triee[n//2]) / 2.0
