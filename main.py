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
                            cursorPosition = event.pos
                            current_connection = [node, cursorPosition]
                            break

            elif event.type == pygame.MOUSEMOTION and dragging:
                current_connection[1] = event.pos

            elif event.type == pygame.MOUSEBUTTONUP and dragging:

                dragging = False
                # Vérifie si le drop est sur un nœud, sinon supprime la connexion
                drop_on_node = False
                for node in map.nodes:
                    reached_node = pygame.Rect(node.x - 10, node.y - 10, 20, 20).collidepoint(event.pos)
                    if reached_node:
                        drop_on_node = True
                        
                        # print(current_connection)
                        isConnectionSuccessful = current_connection[0].add_connection(node)
                        if not isConnectionSuccessful: break
                        else: map.update_nodes()
                
                if not drop_on_node:
                    current_connection = []

        map.afficher_contenu()
            
        # Dessine la ligne en cours de drag
        if dragging:
            # print(map.screen,"/", WHITE, (current_connection[0].x, current_connection[0].y),"/", current_connection[1])
            pygame.draw.line(map.screen, WHITE, (current_connection[0].x, current_connection[0].y), current_connection[1], 2)
    

        pygame.display.flip()
    