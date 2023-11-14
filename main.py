import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Définition des couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Définition de la taille de la fenêtre
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Drag and Drop Nodes")

# Définition de la classe Node
class Node:
    def __init__(self, x, y, couleur):
        self.x = x
        self.y = y
        self.couleur = couleur

# Initialisation des nœuds
nodes = [
    Node(100, 100, RED),
    Node(200, 200, GREEN),
    Node(300, 300, BLUE),
    Node(400, 400, RED),
    Node(500, 500, GREEN),
    Node(600, 100, BLUE),
]

# Liste pour stocker les liaisons entre les nœuds
connections = []

# Fonction pour dessiner les nœuds
def draw_nodes():
    for node in nodes:
        pygame.draw.circle(screen, node.couleur, (node.x, node.y), 10)

# Fonction pour dessiner les connexions
def draw_connections():
    for connection in connections:
        start_pos = (connection[0].x, connection[0].y)
        end_pos = (connection[1].x, connection[1].y)
        pygame.draw.line(screen, WHITE, start_pos, end_pos, 2)
        
# Boucle principale
running = True
dragging = False
current_connection = []

while running:
    screen.fill(BLACK)

    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clic gauche
                for node in nodes:
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
            for node in nodes:
                if pygame.Rect(node.x - 10, node.y - 10, 20, 20).collidepoint(event.pos):
                    connections.append([current_connection[0], node])
                    drop_on_node = True
                    break
            if not drop_on_node:
                current_connection = []

    draw_nodes()
    draw_connections()

    # Dessine la ligne en cours de drag
    if dragging:
        print(screen,"/", WHITE, (current_connection[0].x, current_connection[0].y),"/", current_connection[1])
        pygame.draw.line(screen, WHITE, (current_connection[0].x, current_connection[0].y), current_connection[1], 2)
    pygame.display.flip()

# Quitte Pygame
pygame.quit()
sys.exit()