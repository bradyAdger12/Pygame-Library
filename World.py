'''
Author: Graham Montgomery
Western State Colorado University

This constructs the concurency safe world list
'''

import threading

from Constants import *
from GObj import *


class World:

    def __init__(self):
        self._lock = threading.Lock()
        self.world = []
        self.width = 500
        self.height = 500
        self.caption = "Game Window"
        self.color = WHITE

    def acquire(self):
        self._lock.acquire()
    def release(self):
        self._lock.release()

    def setWidth(self, width):
        self.width = width
    def setHeight(self, height):
        self.height = height
    def getWidth(self):
        return self.width
    def getHeight(self):
        return self.height
    def setSize(self, width, height):
        self.width = width
        self.height = height
    def setCaption(self, caption):
        self.caption = caption
    def setColor(self, color):
        self.color = color

    def add(self, obj, xPos, yPos):
        if xPos is None or yPos is None:
            xPos = obj.x
            yPos = obj.y
        obj.setLocation(xPos, yPos)
        self.world.append(obj)
        
        obj.collidable = True

        # Commented out Fall 2017 DF
        # if(type(obj) is Button or type(obj) is Label):
        #     obj.collidable = False

      
    def remove(self, obj):
        self.world.remove(obj)
        obj.collidable = False

    def inWorld(self, obj): #do we need this????? DLS4/5
        for gobj in self.world:
            if obj is gobj:
                return True
        return False
