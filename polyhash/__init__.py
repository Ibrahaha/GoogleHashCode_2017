#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Paquet du projet Poly#, copie à l'identique des phases finales
    du Google Hash Code 2017.

    Il contient en particulier le modèle et les algorithmes du projet Poly#,
    ainsi que tous les traitements supplémentaires utiles à son bon fonctionnement.
"""

__version__ = "1.0"


# [Optionnel] ajouter ici les principaux symboles, à importer facilement lors de l'usage du paquet polyhash

# permet l'usage dans le module main de: from .polyhash import solve
# plutôt que: from .polyhash.polyhsolver import solve
from .polyhsolver import solve
from .polyhmodel import Carte
