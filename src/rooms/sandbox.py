'''
Created: 2013-06-12
Updated: 2013-06-18
@author: matthew
'''

from math import ceil
from pygmi import Room
from bones.grid import Grid
from entities.world import Dirt
from entities.player import Player

class Sandbox(Room):

    def __init__(self, width, height):
        self.w = width
        self.h = height
        self.player = None
        super().__init__("sandbox",width,height)
        self.setRenderCulling(True)
    
    def update(self):
        self.viewx = self.player.x - ceil(self.w/2) + 16
        self.viewy = self.player.y - ceil(self.h/2) + 32
    
    def event_create(self):
        self.setBackground(self.assets.images["background"]["sky.png"])
        self.g = Grid(16,0,0,300,100)
        for i in range(1,50):
            for j in range(35,45):
                dirt = Dirt(self.g,(i,j))
                self.game.createInstance(dirt)
        self.player = Player(self.g,50,450)
        self.game.createInstance(self.player)
    
    def event_mouseReleased(self,button,pos):
        x,y, = self.g.atPosition(pos[0],pos[1])
        dirt = Dirt(self.g,(x,y))
        self.game.createInstance(dirt)
        neighbors = self.g.getNeighbors(x,y)
        print(dirt.settle())
        for n in neighbors:
            if n != None and n != 0:
                n.settle()
        
        