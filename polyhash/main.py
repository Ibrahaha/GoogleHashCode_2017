#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Module d'entrée pour la mise en oeuvre du projet Poly#.
"""

from polyhsolver import solve

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
        solve(nom_fichier_entre)
    else:
        print("Au revoir")
