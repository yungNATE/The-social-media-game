import pygame 

# Définition de la classe Node
class Node:
    def __init__(self, x, y, couleur):
        self.x = x
        self.y = y
        self.connections = []
        self.last_connection = None # Pour changement de couleur >= 
        ## ↘️ TODO : voir si on garde cette histoire de priorité ou si on affiche des teinte intermédiaires
        self.couleur = couleur
        
    def add_connection(self, node):
        # if node not in self.connections and self not in node.connections:
        if node not in self.connections and node != self:
            self.connections.append(node)
            self.update_color()
            return True

        return False

    def update_color(self):
        colors = {self.couleur: 1}

        for node in self.connections:
            if node.couleur in colors:
                colors[node.couleur] += 1
            else:
                colors[node.couleur] = 1

        print(colors)
        print(max(colors, key = colors.get))

        self.couleur = max(colors, key = colors.get)