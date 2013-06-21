'''
Created: 2013-06-12
Updated: 2013-06-18
@author: catthew
'''

from pygmi import *        


class Player(Object):

    def __init__(self,grid,x,y):
        self.g = grid
        super().__init__(x,y)
        self.grav = 2
        self.acc = 2
        self.jump = 7
        self._jump = 0
        self._jumpdecay = .70
        self._isWalking = 0
        self.friction = 0
        self.v_x_max = 5
        self.v_y_max = 15
        self.v_x = 0
        self.v_y = 0
    
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
        if self._jump > 0 and self.game.keys[K_w]:
            self.v_y -= self._jump
            self._jump *= self._jumpdecay
        
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
        self.v_y += self.grav
        if self.v_y > self.v_y_max:
            self.v_y = self.v_y_max
        self.v_x = self.v_x * (1-self.friction)
        if math.fabs(self.v_x) < 0.3:
            self.v_x = 0
        
        # Hazard top/below
        if(self.v_y > 0):
            mod = 32
        else:
            mod = -32
        hy = [None]*3
        x,y, = self.g.atPosition(self.x+self.v_x-14,self.y+self.v_y+mod)
        hy[0] = self.g.get(x,y)
        x,y, = self.g.atPosition(self.x+self.v_x,self.y+self.v_y+mod)
        hy[1] = self.g.get(x,y)
        x,y, = self.g.atPosition(self.x+self.v_x+13,self.y+self.v_y+mod)
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
            self.friction = hazardy.friction
            if mod == 32 and hazardy.y <= self.y+33:
                self._jump = self.jump       
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
        x,y, = self.g.atPosition(self.x+self.v_x+mod,self.y+self.v_y-31)
        hx[0] = self.g.get(x,y)
        x,y, = self.g.atPosition(self.x+self.v_x+mod,self.y+self.v_y-15)
        hx[1] = self.g.get(x,y)
        x,y, = self.g.atPosition(self.x+self.v_x+mod,self.y+self.v_y)
        hx[2] = self.g.get(x,y)
        x,y, = self.g.atPosition(self.x+self.v_x+mod,self.y+self.v_y+15)
        hx[3] = self.g.get(x,y)
        x,y, = self.g.atPosition(self.x+self.v_x+mod,self.y+self.v_y+31)
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
        
        self.move(self.v_x,self.v_y)
        