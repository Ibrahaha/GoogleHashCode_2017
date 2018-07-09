#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Module de définition des structures de données de Poly#.
"""

__all__ = ['Map'] # ajouter dans cette liste tous les symboles 'importables'

class Map:
    def __init__(self, chemin_fichier, nom_map):

        # Nom donnée à la map
        self.nom_map = nom_map

        # Ouvrir le fichier en écriture
        fichier = open(chemin_fichier, "r")

        # Récupération des lignes du fichier
        liste_chaines = fichier.readlines()

        indications_map = (liste_chaines.pop(0)).split(" ")
        indications_couts = liste_chaines.pop(0).split(" ")
        indications_backbone = liste_chaines.pop(0).split(" ")

        self.nb_lignes = int(indications_map[0])        # Nombre de lignes de la map
        self.nb_colonnes = int(indications_map[1])      # Nombre de colonnes de la map
        self.radius_routeur = int(indications_map[2])   # Radius du routeur

        self.cout_backbone = int(indications_couts[0])  # Coût du backbone
        self.cout_routeur = int(indications_couts[1])   # Coût du routeur
        self.budget = int(indications_couts[2])         # Budget autorisé

        # Coordonnées du backbone
        self.coord_backbone = [int(indications_backbone[0]), int(indications_backbone[1])]

        self.map = liste_chaines
        # Fermeture du fichier
        fichier.close()


        self.nb_routeurs = 0            # Nombre de routeurs placés
        self.nb_backbones = 0           # Nombre de backbones placés
        self.nb_cellules_couvertes = 0  # Nombre de cellules couvertes

        # Listes de coordonnées [x,y]
        self.liste_routeurs = []
        self.liste_backbones = []
        self.liste_cellules_couvertes = []

        self.cout_total = 0     # Coût des infrastructures mises en place

    # Savoir si des coordonnées sont correctes (dans la map)
    def _coord_correctes(self, coordX, coordY):
        return coordX >= 0 and coordY >= 0 and coordX < self.nb_colonnes and coordY < self.lignes

    # Savoir si une cellule est vide ou non
    def _est_vide(self, coordX, coordY):
        return coord_correctes(coordX, coordY) and self.map[coordX][coordY] == '-'

    # Savoir si une cellule contient un mur ou non
    def _est_mur(self, coordX, coordY):
        return coord_correctes(coordX, coordY) and self.map[coordX][coordY] == '#'

    # Savoir si une cellule est cible ou non
    def _est_cible(self, coordX, coordY):
        return coord_correctes(coordX, coordY) and self.map[coordX][coordY] == '.'

    # Mettre à jour suite à un ajout, des attributs liés aux backbones 
    def ajout_backbone(self, coordX, coordY):
        if not ([coordX, coordY] in self.liste_backbones):
            self.liste_backbones.append([coordX, coordY])
            self.nb_backbones += 1

    # Mettre à jour suite à un ajout, des attributs liés aux cellules couvertes
    def ajout_cellule_couverte(self, coordX, coordY):
        if not ([coordX, coordY] in self.liste_cellules_couvertes):
            self.liste_cellules_couvertes.append([coordX, coordY])
            self.nb_cellules_couvertes += 1

    # Mettre à jour suite à un ajout, des attributs liés aux routeurs
    def ajout_routeur(self, coordX, coordY):
        if not ([coordX, coordY] in self.liste_routeurs):
            self.liste_routeurs.append([coordX, coordY])
            self.nb_routeurs += 1
        self.cellules_couvertes(coordX, coordY)

    # TODO -> calculer les cellules couvertes autour d'un routeur
    def cellules_couvertes(self,coordX, coordY):
        return 0

    # Mettre à jour le coût total des installations réseaux
    def maj_cout_total(self):
        self.cout_total = self.nb_backbones * cout_backbone + self.nb_routeurs * cout_routeur

    # Valider ou non le budget des installations réseaux
    def validation_budget(self):
        return self.budget >= self.cout_total

    # Calculer le score induit par les installations sur la carte
    def calcul_score(self):
        if self.validation_budget():
            return 1000 * self.nb_cellules_couvertes + (self.budget - self.cout_total)
        else:
            return -1
        
    # Création et écriture du fichier de résultat
    def creer_fichier_resultat(self):
        with open(self.nom_map + ".txt", 'w+') as file:
            file.write(str(self.nb_backbones) + '\n')
            for backbone in self.liste_backbones: # TODO Les backbones doivent  se suivrent
                file.write(str(backbone[0]) + " " + str(backbone[1]) + "\n") # 0 -> ligne et 1 --> colonne
            file.write(str(self.nb_routeurs) + '\n')
            for routeur in self.liste_routeurs:
                file.write(str(routeur[0]) + " " + str(routeur[1]) + "\n") # 0 -> ligne et 1 --> colonne

if __name__ == "__main__":
    map = Map("repository/PolyHash18/cartes/charleston_road.in", "charleston_road")
    map.ajout_backbone(1,2)
    map.ajout_backbone(3,1)
    map.ajout_backbone(3,3)
    map.ajout_routeur(2,2)
    map.ajout_routeur(1,1)
    map.creer_fichier_resultat()
