Préambule
============
Pandiculation
Projet Poly#
============

Google Hashcode : https://hashcode.withgoogle.com/2017/tasks/hashcode2017_final_task.pdf

Site de validation : http://pitools.polytech.univ-nantes.fr/polyhash/app/index

Vidéo : http://filex.univ-nantes.fr/get?k=F1MYhqHxfMF87oxdLH9

Le fichier `README.md` est écrit en **Markdown**
et permet de soigner la _mise en forme_.

L'équipe
===========
GUITTON Julien
OUKACHE Ayas
SOULEYMANE Ibrahim
COUGNAUD Julien
CREQUER Kilian
MOITEAUX Quentin

L'objectif
===========
Le but est de fournir une solution optimale, via un programme écrit sous python, au problème posé lors du concours GoogleHashCode 2017.
Ce problème étant de couvrir un étage entier de wifi grâce à des bornes wifi ayant une certaine limite d'émission, émission qui est aussi limitée par les murs et de relier ces bornes entre eux en un coût minimal.
L'étage est symbolisé par un pavé de caractère (donc défini de manière discrète).

Répartition
============
Proposition d'un modèle de base :
- MOITEAUX Quentin
- GUITTON Julien
- COUGNAUD Julien (+ fusion des modèles proposés)

Algorithme de pose des Backbones :
- GUITTON Julien
- CREQUER Kilian

Algorithme de pose des Routeurs :
- MOITEAUX Quentin (calcul couverture de la map)
- COUGNAUD Julien (algorithme : choix des routeurs)
- OUKACHE Ayas (tri des couvertures)

Algorithme basé sur l'aléatoire (titre comparatif) :
- SOULEYMANE Ibrahim
- OUKACHE Ayas

Planification des tâches :
- Souleymane Ibrahim

Vidéo :
 - CREQUER Kilian

 Procédure d'installation
===============================
Pour installer ce projet, il suffit de cloner le projet, ou de télécharger l'archive puis de la décompresser,
dans un dossier où l'utilisateur disposera des droits de lecture, d'écriture et d'exécution.

 Procédure d'exécution
===============================
Pour lancer ce projet avec les cartes existantes, il suffit d'aller dans le répertoire polyhash du projet et de lancer
le fichier main.py (python main.py dans votre terminal).

 Détail de la stratégie mise en oeuvre
===============================
Notre stratégie globale consiste à placer l'ensemble des routeurs jusqu'à ce que l'on couvre toute la carte ou bien que le budget est atteint.
Ensuite, on rajoute les backbones pour relier les routeurs entre eux. Si le budget se retrouve dépassé après cette étape, on va enlever autant de routeurs
que cela est nécessaire pour résoudre le problème dans le budget indiqué. On va distinguer par la suite nos deux stratégies pour d'une part, mettre en place les routeurs, et d'autre part, relier efficacement les routeurs entre eux.


Stratégie de placement des routeurs :

- Création d'une carte de couverture, associant, pour chacune des cases de la carte initiale, le nombre de cases qu'un routeur posé dessus pourrait couvrir.
- Tri de l'ensemble des cases selon son potentiel de couverture.
    - Deux cas se présentent alors :
        - Si une seule case est associée à la plus grande couverture possible, on va simplement ajouter le routeur dessus et mettre à jour la carte de couverture. 
        On revient alors à l'étape du tri et on recommence l'opération jusqu'à couvrir toute la carte ou bien jusqu'à atteindre la limite du budget.
        - Si plusieurs cases couvrent le même nombre maximal de cases, on va rajouter plusieurs critères de comparaison.
        Tout d'abord, on va, pour chacune de ces cases, faire la somme du nombre de cases que couvre chacune des cases qu'elle couvre.
        Ainsi, si on pose un routeur sur la case caractérisée par la somme la moins élevée, ce routeur couvrira moins de cases caractérisées par un fort potentiel de couverture.
        Ce qui laissera plus de cases avec un fort potentiel de couverture que si on avait choisi une autre case.
        Si plusieurs cases sont caractérisées par la même somme, on va calculer également la médiane de leur couverture pour les différencier en raisonnant de la même manière.
        Enfin, si les médianes sont identiques, on va choisir la case qui se situe le plus près possible d'un routeur déjà installé (de même couverture) ou du backbone initial.
        Comme dans le cas précédent (une seule case), on met à jour la carte après chaque pose de routeur et on effectue de nouvelles comparaisons avec les nouvelles données.

Stratégie de placement des backbones :
Pour placer les backbones, on utilise 2 stratégies différentes que l'on va comparer afin d'optimiser la répartition des backbones sur la carte.
La première stratégie est basée sur la recherche du backbone le plus proche et la seconde sur l'algorithme de Kruskal.
- On va tout d'abord utiliser ces deux algorithmes afin de relier les routeurs entre eux.
- On va alors comparer les résultats des deux algorithmes pour ne garder que ceux qui ont été obtenus par les deux algorithmes.
- Puis on exécute une nouvelle fois l'algorithme de Kruskal, en considérant cette fois-ci les backbones choisis comme des routeurs, que l'on doit chaîner entre eux, puis le second algorithme.
Et on recommence cette opération tant qu'il existe des backbones en commun afin d'obtenir les positions les plus optimales possibles.


Au niveau des performances, on peut noter que le programme n'occupe généralement pas beaucoup de mémoire.
On note par exemple 27 Mo au maximum de mémoire occupée pour la 1ère carte. L'occupation mémoire étant compensée notamment
lors de la pose des backbones, par l'écriture et la lecture dans des fichiers temporaires.
Du point de vue de la durée, cela varie fortement entre les cartes.
Pour la 1ère carte par exemple, la durée d'exécution est de l'ordre d'une minute sur des postes en salle de TP.
Néanmoins, la durée augmente fortement pour les autres cartes en particulier pour la dernière (Let's Go Higher).
    
    
 Organisation du code
===============================
Le projet est réparti en trois modules, chacun d'eux étant associé à un fichier :
  - polyhmodel  : module de définition de la structure de données d'une carte.
  - polyhsolver : module de résolution du problème de placement des bornes et des backbones.
  - polyhutils  : module des fonctions utilitaires et qui sont utilisées dans les autres modules.

Bugs et limitations connu.e.s
===============================
- Nombre de threads : nombre maximal égal au nombre de routeurs sur la map
- Nombre de threads : Peut également modifier le nombre de backbones (surtout sur Opéra)
- Durée longue sur Lets go higher
