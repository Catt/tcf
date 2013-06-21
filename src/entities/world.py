'''
Created: 2013-06-12
Updated: 2013-06-18
@author: catthew
'''

from pygmi import *

class Dirt(Object):

    def __init__(self,grid,gridPos):
        self.g = grid
        self.gx = gridPos[0]
        self.gy = gridPos[1]
        self.g.set(self.gx,self.gy,self)
        x,y = self.g.getPosition(gridPos[0],gridPos[1])
        super().__init__(x,y)
    
    def event_create(self):
        self.friction = .15
        self.setSprite(Sprite(self.assets.images["dirt"]["dirt_0.png"],16,16),0,0)
        self.settle()
        
        
    def update(self):
        pass
    
    def settle(self):
        neighbors = self.g.getNeighbors(self.gx,self.gy)
        npos = 0
        for i,n in enumerate(neighbors):
            if n != None and n != 0:
                npos = npos | 2**(i)
        
        if npos == 511:
            self.setSprite(Sprite(self.assets.images["dirt"]["dirt_0.png"],16,16))
        if npos == 174 or npos == 190 or npos == 238:
            self.setSprite(Sprite(self.assets.images["dirt"]["dirt_1.png"],16,16))
        if npos == 199 or npos == 231:
            self.setSprite(Sprite(self.assets.images["dirt"]["dirt_1.png"],16,16))
            self.rotate(90)
        if npos == 91:
            self.setSprite(Sprite(self.assets.images["dirt"]["dirt_1.png"],16,16))
            self.rotate(180)
        if npos == 61 or npos == 189:
            self.setSprite(Sprite(self.assets.images["dirt"]["dirt_1.png"],16,16))
            self.rotate(270)
        if npos == 6:
            self.setSprite(Sprite(self.assets.images["dirt"]["dirt_1c.png"],16,16))
        if npos == 3:
            self.setSprite(Sprite(self.assets.images["dirt"]["dirt_1c.png"],16,16))
            self.rotate(90)
        if npos == 9:
            self.setSprite(Sprite(self.assets.images["dirt"]["dirt_1c.png"],16,16))
            self.rotate(180)
        if npos == 12:
            self.setSprite(Sprite(self.assets.images["dirt"]["dirt_1c.png"],16,16))
            self.rotate(270)
        if npos == 191:
            self.setSprite(Sprite(self.assets.images["dirt"]["dirt_1ce.png"],16,16))
        if npos == 239:
            self.setSprite(Sprite(self.assets.images["dirt"]["dirt_1ce.png"],16,16))
            self.rotate(90)
        if npos == 27 or npos == 59:
            self.setSprite(Sprite(self.assets.images["dirt"]["dirt_1cr.png"],16,16))
        if npos == 45:
            self.setSprite(Sprite(self.assets.images["dirt"]["dirt_1cr.png"],16,16))
            self.rotate(90)
        if npos == 142:
            self.setSprite(Sprite(self.assets.images["dirt"]["dirt_1cr.png"],16,16))
            self.rotate(180)
        if npos == 75 or npos == 203:
            self.setSprite(Sprite(self.assets.images["dirt"]["dirt_1cl.png"],16,16))
        if npos == 46:
            self.setSprite(Sprite(self.assets.images["dirt"]["dirt_1cl.png"],16,16))
            self.rotate(180)
        if npos == 135:
            self.setSprite(Sprite(self.assets.images["dirt"]["dirt_1cl.png"],16,16))
            self.rotate(270)
        
        if npos == 44 or npos == 172 or npos == 60 or npos == 188:
            self.setSprite(Sprite(self.assets.images["dirt"]["dirt_2.png"],16,16))
        if npos == 134 or npos == 166 or npos == 198 or npos == 230:
            self.setSprite(Sprite(self.assets.images["dirt"]["dirt_2.png"],16,16))
            self.rotate(90)
        if npos == 67 or npos == 83:
            self.setSprite(Sprite(self.assets.images["dirt"]["dirt_2.png"],16,16))
            self.rotate(180)
        if npos == 25 or npos == 89:
            self.setSprite(Sprite(self.assets.images["dirt"]["dirt_2.png"],16,16))
            self.rotate(270)
        if npos == 10 or npos == 42:
            self.setSprite(Sprite(self.assets.images["dirt"]["dirt_2o.png"],16,16))
        if npos == 5 or npos == 197:
            self.setSprite(Sprite(self.assets.images["dirt"]["dirt_2o.png"],16,16))
            self.rotate(90)
        if npos == 7:
            self.setSprite(Sprite(self.assets.images["dirt"]["dirt_2c.png"],16,16))
        if npos == 11:
            self.setSprite(Sprite(self.assets.images["dirt"]["dirt_2c.png"],16,16))
            self.rotate(90)
        if npos == 13:
            self.setSprite(Sprite(self.assets.images["dirt"]["dirt_2c.png"],16,16))
            self.rotate(180)
        if npos == 14:
            self.setSprite(Sprite(self.assets.images["dirt"]["dirt_2c.png"],16,16))
            self.rotate(270)
        if npos == 175:
            self.setSprite(Sprite(self.assets.images["dirt"]["dirt_2ce.png"],16,16))
        if npos == 95:
            self.setSprite(Sprite(self.assets.images["dirt"]["dirt_2ce.png"],16,16))
            self.rotate(180)
        
        if npos == 40 or npos == 24 or npos == 8 or npos == 56:
            self.setSprite(Sprite(self.assets.images["dirt"]["dirt_3.png"],16,16)) 
        if npos == 164 or npos == 36 or npos == 132 or npos == 4:
            self.setSprite(Sprite(self.assets.images["dirt"]["dirt_3.png"],16,16))
            self.rotate(90)     
        if npos == 194 or npos == 130 or npos == 2 or npos == 66:
            self.setSprite(Sprite(self.assets.images["dirt"]["dirt_3.png"],16,16))
            self.rotate(180)
        if npos == 65 or npos == 17 or npos == 81 or npos == 1:
            self.setSprite(Sprite(self.assets.images["dirt"]["dirt_3.png"],16,16))
            self.rotate(270)
        
        if (npos == 0 or npos == 80 or npos == 32 or npos == 160 or npos == 16 or npos == 208 or npos == 176 or npos == 48
        or npos == 64 or npos == 224 or npos == 192):
            self.setSprite(Sprite(self.assets.images["dirt"]["dirt_4.png"],16,16))
        if npos == 15:
            self.setSprite(Sprite(self.assets.images["dirt"]["dirt_4c.png"],16,16))
        
            
        
        
        return npos
            
        