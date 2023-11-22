import pygame 

# Définition de la classe Node
class Node:
    def __init__(self, x, y, couleur):
        self.x = x
        self.y = y
        self.following = []   # following
        self.followers = []     # followers
        self.couleur = couleur
        self.size = 10 # radius du cercle
        self.reach = 100 #px (taille max des liens)
        
    def follow(self, node):
        if node not in self.following and node != self:
            self.following.append(node)
            self.update_color()

            node.add_follower(self)
            return True

        return False

    def add_follower(self, node):
        if node not in self.followers and node != self:
            self.followers.append(node)
            self.update_size()

    def update_size(self):
        self.set_size(10 + len(self.followers) * 4)
        self.update_reach()

    def update_reach(self):
        self.set_reach(100 + len(self.followers) * 100)

    def set_reach(self, reach):
        self.reach = reach

    def set_size(self, size):
        self.size = size

    def update_color(self):
        colors = {self.couleur: 1}

        for node in self.following:
            if node.couleur in colors:
                colors[node.couleur] += 1
            else:
                colors[node.couleur] = 1

        print(colors)
        print(max(colors, key = colors.get))

        self.couleur = max(colors, key = colors.get)