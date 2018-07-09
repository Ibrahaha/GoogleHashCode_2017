import random
import math


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


    
    
#-------------------------------------test avec la fonction couverture-----------------------------------------------------------------------------------------
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
        if(self.map[pos[1]][pos[0]]== "." or self.map[pos[1]][pos[0]]=="C") :  #On prend C, une selection dans la map d'un carré de demi-segment de longueur rad et de centre le routeur (C'est sur cette liste que l'on va travailler le couvrement)
            care,carePos=carre(self.map,pos,self.radius)

            if test :
                afficherMap(care)

            routeurPos = (pos[0]-carePos[0],pos[1]-carePos[1]) #Pos du routeur au sein du carré
            directions=[]
            if frag :
                HG,H,HD,D,BD,B,BG,G=[],[],[],[],[],[],[],[]
            else :
                final=[]#Liste finale des positions de couvrement
            if care[routeurPos[1]][routeurPos[0]] == "." :
                if not frag :
                    final.append(pos)#Liste finale des positions de couvrement
            if test :
                care[pos[1]][pos[0]]="R"
                afficherMap(care)

             #On regardde depuis le routeur, dans les 4 directions (haut,droite,bas,gauche) la distance
             #séparant le routeur d'une case mur. Distances que l'on va mettre dans cette ordre
             #(haut,droite,bas,gauche) au sein de la liste D (Et on recouvre par ailleurs les cases visitées sol)

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

            posHG=(routeurPos[0]-directions[3],routeurPos[1]-directions[0])           #Selection de la partie de map utile pour le recouvrement
            tailleX=directions[1]+directions[3]+1
            tailleY=directions[2]+directions[0]+1
            select=selection(care,posHG,tailleX,tailleY)


            listes=[selection(select,(0,0),directions[3],directions[0]) if 0 in zone else None,                    #Fragmentation en 4 zones autour du routeur de la selection précédente
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
        
Charleston_road=Carte(~/Polyhash/cartes/Charleston_road) #definition de Charleston_road comme une instance de la classe Carte
Charleston_road.couverture()

    
