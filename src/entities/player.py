'''
Created: 2013-06-12
Updated: 2013-06-18
@author: catthew
'''

from pygmi import *        
from pygame import time

class Player(Object):

    def __init__(self,grid,x,y):
        self.g = grid
        super().__init__(x,y)
        self.grav = 25
        self.acc = 2
        self.jump = 200
        self.jumpdecay = 0.85
        self._jump = 0 
        self._jumpdecay = 0.85
        self._isWalking = 0
        self.friction = 0
        self.v_x_max = 5
        self.v_y_max = 300
        self.v_x = 0
        self.v_y = 0
        self.jumpno = 0
        self.jumping = False
    
    def event_create(self):
        self.setSprite(Sprite(self.assets.images["boy"]["boy_idle"],32,64),-16,-32)
        self.sprite.setFrameTime(15)
        
    def update(self):
        
        #Keys
        if self.game.keys[K_a]:
            if self.v_x >= -self.v_x_max:
                self.v_x -= self.acc
            else:
                self.v_x = -self.v_x_max
        if self.game.keys[K_d]:
            if self.v_x <= self.v_x_max:
                self.v_x += self.acc
            else:
                self.v_x = self.v_x_max
        if  self.game.keys[K_w]:
            if self.jumpno < 2 and not self.jumping:
                self.jumping = True
                self._jump = self.jump
                self._jumpdecay = self.jumpdecay
                self.jumpno += 1
                
            self.v_y -= self._jump
            self._jump *= self._jumpdecay
            self._jumpdecay *= self._jumpdecay
        
        elif self.jumping and not self.game.keys[K_w]:
            self.jumping = False
            
        
        if self.v_x != 0:
            if self._isWalking == 0:
                self.setSprite(Sprite(self.assets.images["boy"]["boy_walk"],32,64))
                self.sprite.setFrameTime(8)
                self.assets.playSound("walking_grass.ogg",-1)
                self._isWalking = 1
            if self.v_x > 0:
                self.setFlipped(False,False)
            else:
                self.setFlipped(True,False)
        else:
            self._isWalking = 0
            self.assets.stopSound("walking_grass.ogg")
            self.setSprite(Sprite(self.assets.images["boy"]["boy_idle"],32,64))
        
        #Physics
        clock = time.Clock()
        fps = clock.get_fps()
        if (fps != 0):
            newy = (self.v_y + self.grav/2)/clock.get_fps()
        else:
            newy = (self.v_y + self.grav/2)/35
        self.v_y += self.grav
        if self.v_y > self.v_y_max: 
            self.v_y = self.v_y_max #Terminal velocity
        self.v_x = self.v_x * (1-self.friction)
        if math.fabs(self.v_x) < 0.3:
            self.v_x = 0
        
        # Hazard top/below
        if(self.v_y > 0):
            mod = 32
        else:
            mod = -32
        hy = [None]*3
        x,y, = self.g.atPosition(self.x+self.v_x-14,self.y+newy+mod)
        hy[0] = self.g.get(x,y)
        x,y, = self.g.atPosition(self.x+self.v_x,self.y+newy+mod)
        hy[1] = self.g.get(x,y)
        x,y, = self.g.atPosition(self.x+self.v_x+13,self.y+newy+mod)
        hy[2] = self.g.get(x,y)
        if mod < 0:
            mod -= 16
        hazardy = None
        for h in hy:
            if h:
                hazardy = h
                break
        if hazardy:
            x,y = self.g.getPosition(x,y)
            self.setY(y-mod)
            self.v_y = 0
            newy = 0
            self.friction = hazardy.friction
            
            #The player lands on something
            if mod == 32 and hazardy.y <= self.y+33:
                self._jump = self.jump
                self._jumpdecay = self.jumpdecay
                self.jumpno = 0    
                self.jumping = False   
            elif mod == -32:
                self._jump = 0     
        else:
            self.friction = 0
        
        # Hazard side
        if(self.v_x > 0):
            mod = 16
        else:
            mod = -16
        hx = [None]*4
        x,y, = self.g.atPosition(self.x+self.v_x+mod,self.y+newy-31)
        hx[0] = self.g.get(x,y)
        x,y, = self.g.atPosition(self.x+self.v_x+mod,self.y+newy-15)
        hx[1] = self.g.get(x,y)
        x,y, = self.g.atPosition(self.x+self.v_x+mod,self.y+newy)
        hx[2] = self.g.get(x,y)
        x,y, = self.g.atPosition(self.x+self.v_x+mod,self.y+newy+15)
        hx[3] = self.g.get(x,y)
        x,y, = self.g.atPosition(self.x+self.v_x+mod,self.y+newy+31)
        hstep = self.g.get(x,y)
        if mod < 0:
            mod -= 16
        hazardx = None
        for h in hx:
            if h:
                hazardx = h
                break
        if hazardx:
            x,y = self.g.getPosition(x,y)
            self.setX(x-mod)
            self.v_x = 0
            
        elif hstep:
            #self._jump == self.jump when grounded
            if self._jump == self.jump and ((self.game.keys[K_a] and self.v_x < 0) or (self.game.keys[K_d] and self.v_x > 0)):
                x,y = self.g.getPosition(x,y)
                self.setX(x-mod)
                self.v_x = 0
                self.v_y = -3.5
                
            else:
                x,y = self.g.getPosition(x,y)
                self.setX(x-mod) 
                self.v_x = 0
        
        self.move(self.v_x, newy)
        