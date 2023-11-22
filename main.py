import pygame
import math
import utility_functions as uf
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
    current_node = None
    cursor_position = None
    cursor_over_max_limit = False

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic gauche
                    for node in map.nodes:
                        if pygame.Rect(node.x - node.size, node.y - node.size, 20, 20).collidepoint(event.pos):
                            dragging = True
                            current_node = node
                            cursor_position = event.pos
                            break

            elif event.type == pygame.MOUSEMOTION and dragging:
                cursor_position = event.pos

            elif event.type == pygame.MOUSEBUTTONUP and dragging:
                dragging = False
                drop_on_node = False
                if(cursor_over_max_limit): 
                    cursor_over_max_limit = False
                    break

                # Vérifie si le drop est sur un nœud, sinon supprime la connexion
                for node in map.nodes:
                    reached_node = pygame.Rect(node.x - 10, node.y - 10, 20, 20).collidepoint(event.pos)
                    if reached_node:
                        drop_on_node = True
                        
                        isFollowSuccessful = current_node.follow(node)
                        if not isFollowSuccessful: break
                        else: map.update_nodes()
                
                if not drop_on_node:
                    current_node = None
                    cursor_position = None

        map.afficher_contenu()
            
        # Dessine la ligne en cours de drag
        if dragging:

            # Calcul du virtual_point_to_draw_line_with_max_length, emule une taille max pour les draw line
            grand_adjacent_length = cursor_position[0] - current_node.x
            grand_oppose_length = cursor_position[1] - current_node.y
            grand_hypotenuse_length = math.sqrt(grand_adjacent_length**2 + grand_oppose_length**2)
            
            if(grand_hypotenuse_length == 0): grand_hypotenuse_length = 0.0001

            angle = math.asin(grand_oppose_length / grand_hypotenuse_length)

            petit_hypothenus_length = node.reach

            modified_cos = math.cos(angle) if cursor_position[0] > current_node.x else -math.cos(angle) 
            #pacth d'un bug, je suis trop mauvais en math pour comprendre

            petit_adjacent_length = petit_hypothenus_length * modified_cos
            petit_oppose_length = petit_hypothenus_length * math.sin(angle)

            print(math.sin(angle))

            if(grand_hypotenuse_length > petit_hypothenus_length):
                virtual_point_to_draw_line_with_max_length = (current_node.x + petit_adjacent_length, current_node.y + petit_oppose_length)
                cursor_over_max_limit = True
            else:
                virtual_point_to_draw_line_with_max_length = cursor_position
                cursor_over_max_limit = False

            current_node_position = (current_node.x, current_node.y)
            # pygame.draw.line(map.screen, WHITE, current_node_position, virtual_point_to_draw_line_with_max_length, 2)
            uf.draw_arrow(map.screen, pygame.Vector2(current_node_position), pygame.Vector2(virtual_point_to_draw_line_with_max_length), WHITE, 2, 12, 5)
            
    

        pygame.display.flip()
    