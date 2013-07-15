'''
Created: 2013-06-12
Updated: 2013-06-18
@author: catthew
'''
from time import time
from math import ceil
from pygmi import *
from rooms.sandbox import Sandbox
from bones.grid import Grid

if __name__ == '__main__':
    
    #Initialize the game
    game = Pygmi((800,600), "TFC", 0)
    assets = game.getAssetManager()
    #Make a roomddd
    game.addRoom(Sandbox(800,600))
    
    #Start the room
    game.gotoRoom("sandbox")

    while True:
        game.update()
        game.render()
        game.paint()
    