import matplotlib.pyplot as pyplot
import time
#Ici, on indice les maps données
#1 -> Charleston Road
#2 -> Let's go Higher
#3 -> Opera
#4 -> Rue de Londres




salles=["charleston_road.in","lets_go_higher.in","opera.in","rue_de_londres.in","test.in"]

class Salle() : #Objet donnant à partir d'un nombre la map et les caractéristiques correspondantes

    def __init__(self, number) :
        k=0
        self.map=[]
        if  0 < number <=5 : 
            f=open(salles[number-1])
            self.piece=f.read()
            f.close()
        else :
            raise ValueError("Il faut rentrer un nombre de 1 à 4 pour choisir une salle")
        L=[]
        for line in self.piece.split('\n') :
            if k>=3 :
                self.map.append([])
                for e in line :
                    self.map[k-3].append(e)
            else :
                for e in line.split(" ") :
                    L.append(int(e))
            k+=1
        self.dim=(L[0],L[1]) #Taille de la carte 
        self.rad=L[2] #Rayon des bornes wifi
        self.cost_w=L[3] #Coût d'une borne wifi
        self.cost_b=L[4] #Coût d'un backbone
        self.budget=L[5] #Budget
        self.ipos=(L[6],L[7]) #Position du backbone initial
        self.bornes=[]
        
    def addBorne(self,pos) :
        self.bornes.append(pos)
        for e in couverture(pos) :
            self.map[e[1]][e[0]]="C"

    def __str__(self) :
        string=""
        for line in self.map :
            for e in line :
                string+=str(e)
            string+='\n'
        return string
        
    def couverture(self,pos,test=False) :
        if(self.map[pos[1]][pos[0]]== ".") :
            C,Cpos=carre(self.map,pos,self.rad)
            if test :
                afficherMap(C)
            
            Rpos = (pos[0]-Cpos[0],pos[1]-Cpos[1]) #Pos du routeur au sein du carré
            D=[]
            F=[pos]
            
            for i in range(4) :
                k=1
                d=((i==1)-(i==3),(i==2)-(i==0))
                val=0
                while(k<=self.rad and (C[Rpos[1]+d[1]][Rpos[0]+d[0]] == "." or C[Rpos[1]+d[1]][Rpos[0]+d[0]] == "C")) :
                    val=abs(d[1-i%2])
                    F.append((pos[0]+d[0],pos[1]+d[1]))
                    k+=1
                    d=(k*((i==1)-(i==3)),k*((i==2)-(i==0)))
                D.append(val)
                
            posHG=(Rpos[0]-D[3],Rpos[1]-D[0])
            tailleX=D[1]+D[3]+1
            tailleY=D[2]+D[0]+1
            S=selection(C,posHG,tailleX,tailleY)
            
            L=[selection(S,(0,0),D[3],D[0]),
                selection(S,(D[3]+1,0),D[1],D[0]),
                selection(S,(D[3]+1,D[0]+1),D[1],D[2]),
                selection(S,(0,D[0]+1),D[3],D[2])]

            for i in range(4) :
                y=0
                k=D[3] if (i==0 or i==3) else D[1]
                for line in revert(L[i],i) :
                    y+=1
                    x=0
                    for e in line[:k:] :
                        x+=1
                        
                        if test :
                            afficherMap(C)
                            
                        if e == "." :
                            newpos=(pos[0]+x*((i==1)+(i==2)-(i==3)-(i==0)),pos[1]+y*((i==3)+(i==2)-(i==1)-(i==0)))
                            F.append(newpos)
                            if test :
                                C[newpos[1]-Cpos[1]][newpos[0]-Cpos[0]]="C"
                        elif e == "C" :
                            break
                        else :
                            k=x-1
                            break
                            
            if test :
                afficherMap(C)
            F.sort()
            if not test :
                return F
        else :
            return "Il faut une case de type sol"
            
        
    def creationMapPuissance(self,test=False) : #Fonction qui retourne une liste de liste calquant la map donnée mais avec sur chaque cases le nombre de cases qu'on couvrirait si on mettait une borne(routeur) dessus
        if test :
            debut = time.time()
        M=[]
        for y in range(len(self.map)) :
            M.append([])
            for x in range(len(self.map[y])) :
                if self.map[y][x]=="." :
                    M[y].append(len(self.couverture((x,y))))
                else :
                    M[y].append(0)
        if test :
            fin = time.time()
            print(fin-debut)
        return M 
def revert(M,i) :
    return [[e for e in line[::(i==1)+(i==2)-(i==0)-(i==3)]] for line in M[::(i==3)+(i==2)-(i==1)-(i==0)]]
    
def mur(posRelMur,rad) :
    L=[]
    for x in range(posRelMur[0] if posRelMur[0]!=0 else -rad, -rad-1 if posRelMur[0]<0 else rad+1,-1 if posRelMur[0]<0 else +1) :
        for y in range(posRelMur[1] if posRelMur[1]!=0 else -rad, -rad-1 if posRelMur[1]<0 else rad+1,-1 if posRelMur[1]<0 else +1) :
            L.append((x,y))
    return L
          
    
def afficherMap(M) : #Fonction qui transforme une liste en chaîne de caractère pour bien l'afficher et le print (affichage dans le shell de python)
        separation=max([max([len(str(e)) for e in line]) for line in M])
        string=""
        for line in M :
            for e in line :
                string+=str(e)+" "*(separation-(len(str(e)))+1)
            string+='\n'
        return print(string)
        
def matAfficherMap(M) : #Fonction test d'affichage avec matplotlib (ne marche pas)
     mat = pyplot.matshow (M, vmin = 0, vmax = max ([max (ligne) for ligne in M]))
     pyplot.colorbar(mat)
     return mat.figure
    
def selection(L,posHG,tailleX,tailleY) : #Fonction qui renvoie la selection d'un rectange au sein d'une liste de liste (map), posHG est sa position haut gauche
    return [[L[posHG[1]+i][posHG[0]+j] for j in range(0,tailleX)] for i in range(0,tailleY)]
    
def carre(L,pos,rad) : #Fonction qui renvoie la sélection (liste de liste) d'un carré de demilongueur rad+1/2 et de centre pos au sein d'une carte (liste de liste) et la position haut gauche de la sélection

    Carre = []
    h=len(L)
    w=len(L[0])
    for y in range(-rad,rad+1) :
        Carre.append([])
        if h>pos[1]+y>=0 :
            for x in range(-rad,rad+1) :
                if w>pos[0]+x>=0 :
                    Carre[y+rad].append(L[pos[1]+y][pos[0]+x])
            
    return Carre,(pos[0]-rad,pos[1]-rad)
    
    
#Valeur qu'on prend initialement pour les tests
p=Salle(3)
M=p.creationMapPuissance(test=True)
#afficherMap(M)