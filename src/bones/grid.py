'''
Created on Jun 13, 2013

@author: catthew
'''

from math import floor

class Grid(object):


    def __init__(self,size,x,y,width,height):
        self.x = x
        self.y = y
        self.s = size
        self.w = width
        self.h = height
        self.grid = []
        for _ in range(0,width):
            self.grid.append([0]*height)
        
    def get(self,x,y):
        if x >= 0 and y >= 0 and x < self.w and y < self.h:
            return self.grid[x][y]
        else:
            return None
    
    def set(self,x,y,obj):
        self.grid[x][y] = obj
    
    def getPosition(self,x,y):
        return (self.x + x * self.s, self.y + y * self.s)
    
    def atPosition(self,x,y):
        return (floor(x / self.s) - self.x, floor(y / self.s) - self.y )
    
    def getNeighbors(self,x,y):
        neighbors = []
        neighbors.append(self.get(x,y-1))
        neighbors.append(self.get(x+1,y))
        neighbors.append(self.get(x,y+1))
        neighbors.append(self.get(x-1,y))
        neighbors.append(self.get(x-1,y-1))
        neighbors.append(self.get(x-1,y+1))
        neighbors.append(self.get(x+1,y-1))
        neighbors.append(self.get(x+1,y+1))
        return neighbors