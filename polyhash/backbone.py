# Fonctions de placement de backbones, s'execute à chaque placement d'un routeur
# Necessite un tableau global qui stocke les coordonnées de chaques backbones en place
# Auteur: Crequer Kilian
def backbonePlacement(listeBackbones,routeur):
    plusProche=[9999,9999] # Stocke la valeur du backbone le plus proche du routeur
    distancePlusProche # Distance entre les coordonées du routeur et le bckbone le plus proche
    for i in range(len(listeBackbones)): # On va comparer la distance pour chaque coordonnées de backbones
        if abs(routeur[0]-listeBackbones[i][0])+abs(routeur[1]-listeBackbones[i][1]) < distancePlusProche : # Si la distance entre le routeur et le backbone i est plus courte
            distancePlusProche= abs(routeur[0]-listeBackbones[i][0])+abs(routeur[1]-listeBackbones[i][1])
            plusProche = listeBackbones[i]
    distanceX= routeur[0]-plusProche[0] # distance sur l'absisse entre le routeur et le backbone le plus proche
    distanceY= routeur[1]-plusProche[1]
    currentBackbone= plusProche # Pointeur sur le backbone que l'on va creer
    while distanceX != 0 or distanceY != 0: #Creation des backbones
        if distanceX > 0 and distanceY > 0: # placement diagonal positif
            currentBackbone[0]= currentBackbonne[0]+1
            currentBackbone[1]= currentBackbonne[1]+1
            InsertBackbone(currentBackbone) # A revoir! fonction qui insert un backbone sur la map
            listeBackbones.append(currentBackbone)
            distanceX=distanceX -1
            distanceY=distanceY -1
        if distanceX < 0 and distanceY < 0: # placement diagonal negatif
            currentBackbone[0]= currentBackbonne[0]-1
            currentBackbone[1]= currentBackbonne[1]-1
            InsertBackbone(currentBackbone) # A revoir! fonction qui insert un backbone sur la map
            listeBackbones.append(currentBackbone)
            distanceX=distanceX +1
            distanceY=distanceY +1
        if distanceX > 0: # placement horizontal positif
            currentBackbone[0]= currentBackbonne[0]+1
            InsertBackbone(currentBackbone) # A revoir! fonction qui insert un backbone sur la map
            listeBackbones.append(currentBackbone)
            distanceX=distanceX -1
        if distanceX < 0: # placement horizontal negatif
            currentBackbone[0]= currentBackbonne[0]-1
            InsertBackbone(currentBackbone) # A revoir! fonction qui insert un backbone sur la map
            listeBackbones.append(currentBackbone)
            distanceX=distanceX +1
        if distanceY > 0: # placement vertical positif
            currentBackbone[1]= currentBackbonne[1]+1
            InsertBackbone(currentBackbone) # A revoir! fonction qui insert un backbone sur la map
            listeBackbones.append(currentBackbone)
            distanceY=distanceY -1
        if distanceY < 0: # placement vertical negatif
            currentBackbone[1]= currentBackbonne[1]-1
            InsertBackbone(currentBackbone) # A revoir! fonction qui insert un backbone sur la map
            listeBackbones.append(currentBackbone)
            distanceY=distanceY +1
    
                    
