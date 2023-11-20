import pygame
import sys
from Window import MAP
from Node import Node

# Définition des couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Exemple d'utilisation
if __name__ == "__main__":
    # Initialisation de Pygame
    pygame.init()
    map = MAP(800, 600, "Jeu")
    map.initialiser_niveau(1)
    # Boucle principale
    dragging = False
    current_connection = []

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic gauche
                    for node in map.nodes:
                        if pygame.Rect(node.x - 10, node.y - 10, 20, 20).collidepoint(event.pos):
                            dragging = True
                            current_connection = [node, event.pos]
                            break
            elif event.type == pygame.MOUSEMOTION and dragging:
                current_connection[1] = event.pos
            elif event.type == pygame.MOUSEBUTTONUP and dragging:
                dragging = False
                # Vérifie si le drop est sur un nœud, sinon supprime la connexion
                drop_on_node = False
                for node in map.nodes:   
                    if pygame.Rect(node.x - 10, node.y - 10, 20, 20).collidepoint(event.pos):
                        # Autorise que une connection entre 2 noeuds
                        if [current_connection[0], node] in map.connections :
                            current_connection = []
                            print("Lien déjà existent")
                            break
                        map.connections.append([current_connection[0], node])
                        drop_on_node = True
                        # stock la couleur du noeud lie
                        if current_connection[0].couleur in node.connections:
                            node.connections[(current_connection[0].couleur)] += 1
                        else:
                            node.connections[(current_connection[0].couleur)] = 1
                        # change la couleur du noeud en fonction de ses liens (définir intéraction pour nombre de liens égaux)
                        node.last_connection = current_connection[0].couleur
                        node.change_color()
                        print(map.connections)
                        break
                if not drop_on_node:
                    current_connection = []

        map.afficher_contenu()
            
        # Dessine la ligne en cours de drag
        if dragging:
            print(map.screen,"/", WHITE, (current_connection[0].x, current_connection[0].y),"/", current_connection[1])
            pygame.draw.line(map.screen, WHITE, (current_connection[0].x, current_connection[0].y), current_connection[1], 2)
    

        pygame.display.flip()
    