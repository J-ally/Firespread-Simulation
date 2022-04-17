# -*- coding : utf-8 -*-

"""
@author : Jaly
date : 13/03/2022
"""

import tkinter as tk
import random as rd
import numpy as np

class Parcelles_graphiques (object) :
    def __init__(self, x_parcelle, y_parcelle, nb_parcelles, pause = False):
        
        global fenetre, canvas
               
        #caractéristiques parcelles
        self.x_parcelle = x_parcelle
        self.y_parcelle = y_parcelle     
        self.x_plateau = self.x_parcelle*nb_parcelles
        self.y_plateau = self.y_parcelle*nb_parcelles
        
        self.pause = pause
        canvas = tk.Canvas(fenetre,width=self.x_plateau, height=self.y_plateau)
        
        canvas.pack()
    
    def create_parcelles (self, TE : float):
        """
        méthode permettant de créer les parcelles et rajoutant dans la matrice_rect les "index" des rectangles crées
        et rajoutant dans la matrice_attr les attributs des parcelles respectives        
        Args : 
            TE (float) : l'humidité des parcelles de la simulation
        Returns : 
            matrice_rect : la matrice d'identification des rectangles,
            matrice_parc : la matrice des objets de classe parcelle avec les attributs de parcelles stockes dans les tags respectifs
        """
        # les matrices remplie de zero correspondante
        matrice_rect = [[0 for col in range(int(self.x_plateau/self.x_parcelle))]  
                           for row in range (int(self.y_plateau/self.y_parcelle))]
        
        matrice_parc = [[0 for col in range(int(self.x_plateau/self.x_parcelle))] 
                           for row in range (int(self.y_plateau/self.y_parcelle))]
        
        for i in range (len(matrice_rect)):
            for j in range(len(matrice_rect[0])) :
                
                A =  Parcelle (i, j, "Arbre", TE, False, 0 )
                matrice_rect[i][j] = (canvas.create_rectangle(0+self.x_parcelle*i,0+self.y_parcelle*j, 
                                self.x_parcelle + self.x_parcelle*i, self.y_parcelle+self.y_parcelle*j, 
                                fill = A.get_couleur_parcelle(),
                                activefill= "purple"  ) )
                
                matrice_parc [i][j] = A
                
        self.matrice_parc = matrice_parc #matrice des objets
        self.matrice_rect = matrice_rect #matrice des 
        return ([matrice_rect, matrice_parc])
    
    def update_parcelle (self) :
        """
        mets à jour la parcelle concernée (self)
        """
        new_matrice_rect = [[0 for col in range(int(self.x_plateau/self.x_parcelle))] 
                           for row in range (int(self.y_plateau/self.y_parcelle))]
        
        for i in range (len(new_matrice_rect)):
            for j in range(len(new_matrice_rect[0])) :
                
                new_matrice_rect[i][j] = (canvas.create_rectangle(0+self.x_parcelle*i,0+self.y_parcelle*j, self.x_parcelle + self.x_parcelle*i, self.y_parcelle+self.y_parcelle*j, 
                                fill = A.get_couleur_parcelle() ) )
            
        new_matrice_rect = self.matrice_rect
        pass 

        
class Parcelle (object) :
    
    def __init__(self, i, j, type_parcelle, TE, feu, temps_feu):
        """creation de la classe parcelle, qui crée un rectangle dans canvas"""
       
        self.i = i   
        self.j = j
        
        self.type_parcelle = type_parcelle
        self.TE = TE
        self.feu = feu
        self.temps_feu = temps_feu

    def get_couleur_parcelle (self) :
        """
        donne la couleur de la parcelle en fonction de ses attributs
        Returns : 
            la couleur de la parcelle en fonction de ses attributs
        """
        
        if self.feu and self.temps_feu < 2  :
            return "red"
                
        elif self.feu and self.temps_feu >= 2  :
            return "grey"
        
        else :
            if self.type_parcelle == "Arbre" :
                return "green"
                
            elif self.type_parcelle == "Obstacle" :
                return "blue"
            
            elif self.type_parcelle == "Route" :
                return "yellow"
            
    def update_rectangle (self) :
        """creation du nouveau rectangle"""
        global x_parcelle, y_parcelle
        
        canvas.create_rectangle(0+x_parcelle*self.i,0+y_parcelle*self.j, x_parcelle + x_parcelle*self.i, y_parcelle + y_parcelle*self.j, 
                                fill = self.get_couleur_parcelle()   ) 
        pass       
    
    def set_parcelle_feu (self) :
        """change l'attribut de la parcelle pour la mettre en feu. Chaque parcelle a une probabilité d'être mise en feu en fonction de son humidité"""
        proba_feu = rd.random()
        if not self.feu and self.type_parcelle == "Arbre":
            if self.TE > 0.5 :
                if proba_feu < 0.1:
                    self.feu = True
                else:
                    pass
            elif 0.3 < self.TE and self.TE <= 0.5  :
                if proba_feu < 0.2 :
                    self.feu = True
                else :
                    pass
            elif 0.15 < self.TE and self.TE <= 0.3  :
                if proba_feu < 0.5 :
                    self.feu = True
                else :
                    pass
            elif 0.07 < self.TE and self.TE <= 0.15 :
                if proba_feu < 0.8 :
                    self.feu = True
                else :
                    pass
            elif 0 <= self.TE and self.TE <= 0.07  :
                    self.feu = True
        else : 
            pass
        
    def set_parcelle_feu_oblige (self) :
        """change l'attribut de la parcelle pour la mettre en feu, peu importe son humidité"""
        if not self.feu and self.type_parcelle == "Arbre":
            self.feu = True
        else :
            pass
    
    def set_parcelle_type (self, type : str) :
        """
        change le type de la parcelle en le type donné en argument
        Args :
            type (str) : le type de parcelle voulu ("Arbre", "Obstacle","Route")
        """
        self.type_parcelle = type
        pass
    
    def set_temps_feu (self) :
        """augmente le temps feu de 1"""
        self.temps_feu += 1 
        pass
    
    def print_attributs(self) :
        attributs = [self.type_parcelle, self.TE, self.feu, self.temps_feu]
        return (attributs)
    
class Propagation (Parcelle) :
    
    def __init__(self, i : int, j : int, vent,  step = 1) :
        """
        initialise la classe propagation
        Args:
            i, j (int): position de la parcelle initiale
            vent (bool, optional): présence de vent ("Droite", "Gauche", "Haut", "Bas") ou non ("False")
            step (int, optional): taille de l'incrementation. Defaults to 1.
        """
        self.i = i
        self.j = j
        self.vent = vent
        self.step = step
        pass
    
    def get_around_id_rect (self) :
        """
        récupère les indices des rectangles des parcelles adjacentes a la parcelle demandée
        Return :
            retourne les id des rectangles concernés
        """
        global canvas_rect
                
        cases = self.get_cases ()
        parc_ids = []
        
        for position in range(len(cases)):
            if cases [position][0]  < 0 or cases [position][1] < 0 or cases [position][0]  >= len(canvas_rect) or cases [position][1] >= len(canvas_rect[0]) :
                pass
                
            else :
                canv_parc = canvas_rect [cases [position][0]] [cases [position][1]]
                parc_ids.append (canv_parc)
        return parc_ids
    
    def get_cases (self) :
        """
        donne les coordonnées des cases adjacentes a une case dont la position est donnée en argument
        Returns:
            position_cases : la matrice contenant les indices des cases a inspecter 
        """        
        position_cases = [[self.i + self.step, self.j], [self.i - self.step, self.j],
                          [self.i, self.j + self.step],[self.i, self.j - self.step]] #droite, gauche, bas, haut
        
        if self.vent == "False" :
            return position_cases
        
        else :
            if self.vent == "Droite" :
                self.i += 1
                
            elif self.vent == "Gauche" :
                self.i -= 1
            
            elif self.vent == "Bas" :
                self.j += 1
            
            elif self.vent == "Haut" :
                self.j -= 1
            
            position_cases += [[self.i + self.step, self.j], [self.i - self.step, self.j],
                               [self.i, self.j + self.step],[self.i, self.j - self.step]] #droite, gauche, bas, haut
            return position_cases

    def propa_feu (self) :
        """
        code la propagation du feu et mets à jour le ticker des parcelles en feu
        """
        global canvas_parc, canvas_rect
        future_propa_index = self.get_around_id_rect()
                
        for i in range (len(future_propa_index)) :
            parc_id = future_propa_index [i] #index du rectangle
            parc_ind = id_to_indices_rect (parc_id)
            
            canvas_parc_id = canvas_parc [parc_ind[0]] [parc_ind[1]]
            
            if canvas_parc_id.get_couleur_parcelle () == "red" :
                    pass
            else :
                canvas_parc_id.set_parcelle_feu()
                canvas_parc_id.update_rectangle ()

####### Fonctions du jeu  
def indices_to_id_rect (i_parcelle, j_parcelle) :
        """
        methode recuperant l'id du rectangle demandé
        Args :
            i_parcelle, j_parcelle : les coordonnées de la parcelle
        Returns :
            l'indice du rectangle
        """
        global canvas_rect
        
        flag = True
        id = 0 #un id de zéro n'existe pas dans la matr_rect
        while flag : 
            try : 
                id = canvas_rect[i_parcelle][j_parcelle] 
                flag = False
            except IndexError :
                print("L'index n'est pas bon")
                return (canvas_parc)
        return id
                
def id_to_indices_rect (id) :
    """
    méthode récuperant les coordonnées du rectangle donné
    Args :
        id : le numero de la parcelle/du rectangle
    Returns :
        les coordonnées sous forme de liste [i,j]
    """
    global canvas_rect
    
    flag = True
    i_parcelle = 0
    j_parcelle = 0
    np_matrice_rect = np.array(canvas_rect)
    while flag : 
               
        try : 
            ij = np.where(np_matrice_rect == id)
            ij = np.array(ij)
            i_parcelle = ij[0][0]
            j_parcelle = ij[1][0]
            flag = False
        except IndexError :
            print("L'id n'est pas bon")
            return (np_matrice_rect)
    return ( [i_parcelle,j_parcelle] )

def get_loc_parc_feu () :
        """
        trouve sur l'ensemble de la simulation les parcelles en feu
        Returns :
            liste des parcelles en feu
        """
        global canvas_parc, canvas_rect
        
        parcelle_feu = []
        
        for i in range (len(canvas_parc)):
            for j in range(len(canvas_parc[0])) :
                attr_parc = canvas_parc [i][j]
                    
                if attr_parc.get_couleur_parcelle () == "red" : #on regarde si la parcelle est en feu
                    parcelle_feu.append(canvas_rect [i][j])
                    attr_parc.set_temps_feu()
              
        return(parcelle_feu)
    
#######Fonctions des évènements

def detection_click_feu (event) :
    global canvas_parc, A
    
    xsouris , ysouris = event.x, event.y
    id_object = canvas.find_closest(xsouris,ysouris)
    ind_object = id_to_indices_rect(id_object[0])
    
    canvas_parc_id = canvas_parc [ind_object[0]] [ind_object[1]]
    canvas_parc_id.set_parcelle_feu_oblige ()
    canvas_parc_id.update_rectangle ()
    pass
        
def detection_click_obstacle (event) :
    global canvas_parc
    
    xsouris , ysouris = event.x, event.y
    id_object = canvas.find_closest(xsouris,ysouris)
    ind_object = id_to_indices_rect(id_object[0])
    
    canvas_parc_id = canvas_parc [ind_object[0]] [ind_object[1]]
    canvas_parc_id.set_parcelle_type ("Obstacle")
    canvas_parc_id.update_rectangle ()
    pass

########La propagation du feu
def jeu () :
    """
    fonction itérative utilisé pour et mettre à jour le canvas ...
    """
    global fenetre, vent_choisi
    
    parc_feu = get_loc_parc_feu() #pour gagner de l'efficacité on aurait pu faire une liste des parcelles en feu que l'on 
    #gardait d'une itération à une autre et que l'on mettait à jour à chaque tour
    
    for i in range (len(parc_feu)):
        ind_parc = id_to_indices_rect (parc_feu[i])
        propa = Propagation (ind_parc[0], ind_parc[1], vent_choisi.get())
        propa_future = propa.propa_feu ()
        
    fenetre.after (800, jeu)

######Initialisation de la fenêtre graphique
def simulation () :
    """initialisation de la fenetre graphique"""
    global fenetre, canvas_rect, canvas_parc, x_parcelle, y_parcelle, TE_choisi
    
    #lancement de la fenetre graphique
    fenetre = tk.Tk()
    fenetre.title("Simulation de feux de forêts")
    fenetre.resizable()
    fenetre.config(relief=tk.RAISED, bd=3)
    label = tk.Label(fenetre, text="Click gauche pour enflammer une parcelle, click droit pour poser un pare-feu", font=(14))
    label.pack()

    #creation du canvas
    x_parcelle, y_parcelle, nb_parcelles = 15, 15, 20
    A = Parcelles_graphiques(x_parcelle ,y_parcelle, nb_parcelles )
    canvas_rect_parc = A.create_parcelles(TE = float((TE_choisi.get())))
    canvas_rect = canvas_rect_parc [0] 
    canvas_parc = canvas_rect_parc [1]

    #evenements
    fenetre.bind("<Button-1>", detection_click_feu)
    fenetre.bind("<Button-3>", detection_click_obstacle)

    #On fait la propagation
    jeu()
    fenetre.mainloop()


######Fenêtre de choix des parametres
def choix_parametres():
    global vent_choisi, TE_choisi 
    
    fenetre_intro = tk.Tk()
    fenetre_intro.title("Choix des paramètres")
    fenetre_intro.resizable()
    fenetre_intro.config(relief=tk.RAISED, bd=3)
    
    #vent
    label = tk.Label(fenetre_intro, text="On met du vent ?")
    label.pack()
    vent_choisi = tk.StringVar() 
    boutonF = tk.Radiobutton(fenetre_intro, text="Pas de vent", variable=vent_choisi, value = "False")
    boutonO = tk.Radiobutton(fenetre_intro, text="Vent Ouest", variable=vent_choisi, value="Gauche")
    boutonE = tk.Radiobutton(fenetre_intro, text="Vent Est", variable=vent_choisi, value="Droite")
    boutonN = tk.Radiobutton(fenetre_intro, text="Vent Nord", variable=vent_choisi, value="Haut")
    boutonS = tk.Radiobutton(fenetre_intro, text="Vent Sud", variable=vent_choisi, value="Bas")
    boutonF.select()
    boutonF.pack()
    boutonO.pack()
    boutonE.pack()
    boutonN.pack()
    boutonS.pack()
    
    #humidité
    TE_choisi = tk.DoubleVar()
    scale = tk.Scale(fenetre_intro, variable=TE_choisi, orient='horizontal', from_=0, to=1,
          resolution = 0.1, tickinterval=0.1, length=300,
          label="Quel taux d'humidité?")
    scale.pack()
    
    #bouton valider
    boutonValider=tk.Button(fenetre_intro, text="Valider", command=lambda:[fenetre_intro.destroy(), simulation()])
    boutonValider.pack()
    
    fenetre_intro.mainloop()

#####PROGRAMME PRINCIPAL
choix_parametres()