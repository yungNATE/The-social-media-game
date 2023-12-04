import pygame
import sys
from abc import ABC, abstractmethod
from Node import Node
import utility_functions as uf
import time

# Définition des couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Window(ABC):
    def __init__(self, largeur, hauteur, titre):
        pygame.init()
        self.largeur = largeur
        self.hauteur = hauteur
        self.titre = titre
        self.font = pygame.font.Font(None, 36)

    @abstractmethod
    def afficher_contenu(self):
        pass

    def afficher_texte(self, texte, x, y):
        texte_surface = self.font.render(texte, True, WHITE)
        texte_rect = texte_surface.get_rect(center=(x, y))
        self.screen.blit(texte_surface, texte_rect)


class Menu(Window):
    def __init__(self, largeur, hauteur, titre):
        super().__init__(largeur, hauteur, titre)

    def afficher_contenu(self):
        self.afficher_texte("Menu Principal", self.largeur // 2, self.hauteur // 4)
        self.afficher_texte("Jouer", self.largeur // 2, self.hauteur // 2)
        self.afficher_texte("Options", self.largeur // 2, self.hauteur // 2 + 50)
        self.afficher_texte("Quitter", self.largeur // 2, self.hauteur // 2 + 100)

    def gerer_clic(self, pos_souris):
        if self.bouton_clic(self.largeur // 2 - 50, self.hauteur // 2 - 25, 100, 50, pos_souris):
            print("Bouton Jouer cliqué")
        elif self.bouton_clic(self.largeur // 2 - 50, self.hauteur // 2 + 25, 100, 50, pos_souris):
            print("Bouton Options cliqué")
        elif self.bouton_clic(self.largeur // 2 - 50, self.hauteur // 2 + 75, 100, 50, pos_souris):
            pygame.quit()
            sys.exit()


class MAP(Window):
    def __init__(self, largeur, hauteur, titre):
        super().__init__(largeur, hauteur, titre)
        self.largeur = largeur
        self.hauteur = hauteur
        self.node = []
        self.screen = pygame.display.set_mode((largeur, hauteur))
        self.text_niveau = ""
        pygame.display.set_caption(titre)
    
    # Fonction pour dessiner les nœuds
    def draw_nodes(self, nodes):
        for node in nodes:
            pygame.draw.circle(self.screen, node.couleur, (node.x, node.y), node.size)
            
    
    # Fonction pour dessiner les connexions
    def draw_connections(self):
        for node in self.nodes:    
            for connection in node.following:        
                start_pos = (node.x, node.y)
                end_pos = (connection.x, connection.y)
                uf.draw_arrow(self.screen, pygame.Vector2(start_pos), pygame.Vector2(end_pos), WHITE, 2, 12, 10)
                    

    def border_screen(self, color:tuple):
        pygame.draw.rect(self.screen, color, (0, 0, self.largeur, self.hauteur), 10)
        pygame.display.flip()
        time.sleep(0.3)
        # Rétablir la couleur du bord initial
        pygame.draw.rect(self.screen, color, (0, 0, self.largeur, self.hauteur), 10)
        pygame.display.flip()
    

    def win_screen(self, n):
        print(n)
        self.screen.fill(BLACK)
        if n == "Tuto":
            self.afficher_texte("Tout les noeuds sont de la même couleur !", self.largeur // 2, self.hauteur // 2)
        if n == "Tuto 2":
            self.afficher_texte("Tu as fini le tutoriel !", self.largeur // 2, self.hauteur // 2)
        if n == "hidden_win":
            self.afficher_texte("Tu as relié tout les noeuds sans en changer la couleur intéressant..", self.largeur // 2, self.hauteur // 2)
        
    def lose_screen(self):
        self.screen.fill(BLACK)
        self.afficher_texte("Retry", self.largeur // 2, self.hauteur // 2)

    def initialiser_niveau(self, n:str):
        # Initialisation des nœuds

        

        if n == "Tuto":
            self.nodes = [
                Node(400, 200, RED),
                Node(350, 200, RED),
                Node(375, 300, GREEN),
            ]
            for node in self.nodes:
                node.activations = {'size' : False, 
                            'reach' : False, 
                            'color' : True}

        if n == "Tuto 2":
            self.nodes = [
                Node(400, 200, RED),
                Node(350, 200, RED),
                Node(375, 375, GREEN),
            ]

        if n == "Niveau 1":
            self.nodes = [
                Node(200, 200, RED),
                Node(200, 100, BLUE),
                Node(100, 200, GREEN),
                Node(500, 450, BLUE),
                Node(300, 450, GREEN),
                Node(500, 550, RED),
            ]

        if n == "Niveau 2":
            self.nodes = [
            ]

        self.text_niveau = f"{n}"

    def afficher_contenu(self):
        self.screen.fill(BLACK)
        self.afficher_texte("Drag and Drop Nodes", self.largeur // 2, self.hauteur // 40)
        self.afficher_texte(self.text_niveau, self.largeur // 2, self.hauteur // 15)

        
        self.draw_nodes(self.nodes)

        self.draw_connections()


    def update_nodes(self):
        for node in self.nodes:
            node.update_color()

    def equilibre_node(self):
        res = {}
        for node in self.nodes:
            if node.couleur in res.keys():
                res[node.couleur] += 1
            else:
                res[node.couleur] = 1
        if len(set(res.values())) != 1:
            return False
        else :
            return True
        
    def equilibre_links(self):
        if not False in [len([follow.couleur for follow in node.following]) >= 2 for node in self.nodes] :
            return True
        else:
            False
            

    def win_condition(self): 
        if len(set([node.couleur for node in self.nodes])) == 1:
            return True
        elif self.equilibre_links() and self.equilibre_node() :
            return "hidden_win"
        else :
            return False
    
    def lose_condition(self):
        if sum([len(node.following) for node in self.nodes]) == (2*len(self.nodes) + 1):
            return True
        else:
            return False