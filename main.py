import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Définition des couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Définition de la taille de la fenêtre
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Drag and Drop Nodes")

# Définition des nœuds initiaux
nodes = [
    (100, 100),
    (200, 200),
    (300, 300),
    (400, 400),
]

# Liste pour stocker les liaisons entre les nœuds
connections = []

# Fonction pour dessiner les nœuds
def draw_nodes():
    for node in nodes:
        pygame.draw.circle(screen, WHITE, node, 10)

# Fonction pour dessiner les connexions
def draw_connections():
    for connection in connections:
        pygame.draw.line(screen, WHITE, connection[0], connection[1], 2)

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
                    if pygame.Rect(node[0] - 10, node[1] - 10, 20, 20).collidepoint(event.pos):
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
                if pygame.Rect(node[0] - 10, node[1] - 10, 20, 20).collidepoint(event.pos):
                    connections.append([current_connection[0], node])
                    drop_on_node = True
                    break
            if not drop_on_node:
                current_connection = []

    draw_nodes()
    draw_connections()

    # Dessine la ligne en cours de drag
    if dragging:
        pygame.draw.line(screen, WHITE, current_connection[0], current_connection[1], 2)

    pygame.display.flip()

# Quitte Pygame
pygame.quit()
sys.exit()
