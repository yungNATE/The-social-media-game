import pygame
import sys
from abc import ABC, abstractmethod
from Node import Node
import utility_functions as uf

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
        nb_lignes = 10
        nb_colonnes = 10
        # Calcul de la taille des spots en fonction de la fenêtre
        self.taille_spot = min(largeur // nb_colonnes, hauteur // nb_lignes)
        #self.matrice_nodes = [[None for _ in range(nb_colonnes)] for _ in range(nb_lignes)]
        self.node = []
        self.connections = []
        self.screen = pygame.display.set_mode((largeur, hauteur))
        self.text_niveau = ""
        pygame.display.set_caption(titre)
    
    # Fonction pour dessiner les nœuds
    def draw_nodes(self, nodes):
        for node in nodes:
            pygame.draw.circle(self.screen, node.couleur, (node.x, node.y), 10)
    
    # Fonction pour dessiner les connexions
    def draw_connections(self, nodes):
        for node in self.nodes:    
            for connection in node.connections:        
                start_pos = (node.x, node.y)
                end_pos = (connection.x, connection.y)
                # pygame.draw.line(self.screen, WHITE, start_pos, end_pos, 2)
                uf.draw_arrow(self.screen, pygame.Vector2(start_pos), pygame.Vector2(end_pos), WHITE, 2, 12, 5)

    def initialiser_niveau(self, n):
        # Initialisation des nœuds
        if n == 1:
            self.nodes = [
                Node(100, 100, RED),
                Node(150, 100, RED),
                Node(200, 200, GREEN),
                Node(300, 300, BLUE),
                Node(300, 350, BLUE),
                Node(400, 400, RED),
                Node(500, 500, GREEN),
                Node(600, 100, BLUE),
            ]
        self.text_niveau = f"Niveau {n}"

    def afficher_contenu(self):
        self.screen.fill(BLACK)
        self.afficher_texte("Drag and Drop Nodes", self.largeur // 2, self.hauteur // 40)
        self.afficher_texte(self.text_niveau, self.largeur // 2, self.hauteur // 15)

        
        self.draw_nodes(self.nodes)
        self.draw_connections(self.nodes)

    def update_nodes(self):
        for node in self.nodes:
            node.update_color()