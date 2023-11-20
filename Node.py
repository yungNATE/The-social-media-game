import pygame 

# Définition de la classe Node
class Node:
    def __init__(self, x, y, couleur):
        self.x = x
        self.y = y
        self.connections = {couleur:1}
        self.last_connection = None # Pour changement de couleur >= 
        self.couleur = couleur
        
    # change si >
    def change_color(self):
        print(max(self.connections, key=self.connections.get))
        self.couleur = max(self.connections, key = self.connections.get)
    
    """
    # change si >=
    def change_color(self):
        print(max(self.connections, key=self.connections.get))
        self.couleur = self.last_connection if list(self.connections.values()).count(max(self.connections.values()))>1 else max(self.connections, key = self.connections.get)
"""