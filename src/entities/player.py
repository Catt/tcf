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
        self.walk_acc = 2
        self.dash_acc = 8
        self.aerial_acc = 2
        self.jump = 200
        self.jumpdecay = 0.85
        self._jump = 0 
        self._jumpdecay = 0.85
        self._isWalking = 0
        self.friction = 0
        self.air_friction = 0
        self.walk = 8
        self.dash = 15
        self.dashing = False
        self.v_y_max = 300
        self.v_x_max = 0
        self.v_x_maxair = self.walk
        self.v_x = 0
        self.v_y = 0
        self.jumpno = 0
        self.aerial = False
        self.prev_up = False
        self.prev_left = False
        self.prev_right = False
        self.tap_time = 0
    
    def event_create(self):
        self.setSprite(Sprite(self.assets.images["boy"]["boy_idle"],32,64),-16,-32)
        self.sprite.setFrameTime(15)
     
    def update_keys(self):
        self.prev_up = self.game.keys[K_w]
        self.prev_left = self.game.keys[K_a]
        #ensures game won't register both left and right at same time
        if self.prev_left == True:
            self.prev_right = False
        else:
            self.prev_right = self.game.keys[K_d]
        
    def changed_direction(self):
        if self.game.keys[K_a] and self.prev_right == True:
            return True
        elif self.game.keys[K_d] and self.prev_left == True:
            return True
        else:
            return False
    
    def pressed_left(self):
        return self.game.keys[K_a] and not self.prev_left
    
    def pressed_right(self):
        return self.game.keys[K_d] and not self.prev_right   
    
    def update_dashing(self):
        timeBetweenTaps = 500
        if self.pressed_left() or self.pressed_right():
            timeBetweenTaps = time.get_ticks() - self.tap_time
            self.tap_time = time.get_ticks()
        if self.aerial and not self.dashing:
            self.dashing = False
        elif self.dashing and (self.game.keys[K_a] or self.game.keys[K_d]):
            #Maintain dash
            self.dashing = True
        elif not (self.game.keys[K_a] or self.game.keys[K_d]):
            #Dashing stops if not moving left or right
            self.dashing = False
        elif timeBetweenTaps < 200:
            self.dashing = True
        else:
            self.dashing = False
           
    def update(self):
        self.update_dashing()
        #Keys
        #Movement varies based on whether the player is aerial or not
        if self.aerial:
            if  self.game.keys[K_w]:
                if self.jumpno < 2:
                    if not self.prev_up:
                        self._jump = self.jump
                        self._jumpdecay = self.jumpdecay
                        self.v_y = 0
                        self.jumpno += 1
                        if self.changed_direction():
                            self.v_x = 0
                self.v_y -= self._jump
                self._jump *= self._jumpdecay
                self._jumpdecay *= self._jumpdecay
            if self.game.keys[K_a]:
                if self.v_x > -self.v_x_maxair:
                    self.v_x -= self.aerial_acc
                else:
                    self.v_x = -self.v_x_maxair/(1-self.air_friction)
            elif self.game.keys[K_d]:
                if self.v_x < self.v_x_maxair:
                    self.v_x += self.aerial_acc
                else:
                    self.v_x = self.v_x_maxair/(1-self.air_friction)
            
                
        #On the ground
        else:
            if self.dashing:
                max_speed = self.dash
                acc = self.dash_acc
            else:
                max_speed = self.walk
                acc = self.walk_acc
                
            if self.game.keys[K_a]:
                if self.v_x > -max_speed:
                    self.v_x -= acc
                else:
                    self.v_x = -max_speed/(1-self.friction)
      
            if self.game.keys[K_d]:
                if self.v_x < max_speed:
                    self.v_x += acc
                else:
                    self.v_x = max_speed/(1-self.friction)
            if  self.game.keys[K_w]:
                self.aerial = True
                self._jump = self.jump
                self._jumpdecay = self.jumpdecay
                    
                self.v_y -= self._jump
                self._jump *= self._jumpdecay
                self._jumpdecay *= self._jumpdecay
                if self.dashing:
                    self.v_x_max = math.fabs(self.v_x)
                else:
                    self.v_x_max = self.v_x_maxair
                    
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
        if self.aerial:
            self.v_x = self.v_x * (1-self.air_friction)
        else:
            self.v_x = self.v_x * (1-self.friction)
            print("After Friction: %d"%self.v_x)
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
                self.jumpno = 1    
                self.aerial = False
                
            #The player hits something above it       
            elif mod == -32:
                self._jump = 0   
                
        #nothing above or below  
        else:
            #self.friction = 0
            self.aerial = True
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
        self.update_keys()
        