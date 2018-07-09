class ResolveurCouv():

    def __init__(self, mapfile):
        # Parsing de l'en-tete du fichier de la carte
        self.file = open(mapfile, "r")
        self.lines = self.file.readlines()
        dimension = self.lines[0].split(" ")
        self.nb_rows = int(dimension[0])
        self.nb_columns = int(dimension[1])
        self.radius = int(dimension[2])
        costs = self.lines[1].split(" ")
        self.cost_bb = int(costs[0])
        self.cost_router = int(costs[1])
        self.budget = int(costs[2])
        self.init_cell = self.lines[2].split(" ")

    def afficheCarte(self):
        # Affichage des propriétés de la carte
        print("Dimension : ")
        print("\tnb rows : ", self.nb_rows)
        print("\tnb columns : ", self.nb_columns)
        print("\tradius : ", self.radius)
        print("Costs: ")
        print("\tbackbone : ", self.cost_bb)
        print("\trouter : ", self.cost_router)
        print("\tbudget : ", self.budget)
        print("init cell : ", self.init_cell)


    def calculMaxRouters(self):
        # Calcul du nombre maximale de routeur que l'on peut disposer
        # avec le budget imparti et la couverture maximal que l'on peut avoir
        #nb : nombre de routeurs poses, cc: nombre de case couvertes potentiellement
        nb = 0
        b = self.budget
        cc = 0
        while((b-(self.cost_router+self.cost_bb))>=0): #on verifie que le budget soit toujours superieur à la somme du cout du routeur et du backbone
            nb+=1
            # on suppose que pour chaque routeur il y a un backbone
            b-=(self.cost_router+self.cost_bb)
            cc += self.radius**2-1

        print("il peut y avoir maximum ",str(nb)," routeurs qui couvrent au maximum ",str(cc)," cases")
        print("il reste ",b," du budget")


    def carreCouv(self,couv,map):
        # A finir
    def poseRouteurs(self, listeCouv,mapCouv):
        # A finir
        listeRouteurs = []
        listeRouteurs.append(listeCouv[0])
        listeCouv = listeCouv[1:]



r = ResolveurCouv("cartes/opera.in")
r.afficheCarte()
r.calculMaxRouters()
print("il y a ",r.nb_rows*r.nb_columns, "cases")
