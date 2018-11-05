'''
Author: Graham Montgomery
Western State Colorado University

This file is the basic import file for any cs0 project. It will 
hold some basic functions for manipulating the world and starting 
the engine
'''

import time
import random
import Globals as g

g.pygame.init()

import Engine
import Events
from GObj import *

window = g.world
started = False

###### GUI Editing

def inWorld(obj):
    if not isinstance(obj, GObj):
        raise Exception('Argument must be a graphic object'
                        '\nValid Example: inWorld(circle1)')
    return window.inWorld(obj)

def add(obj, xPos=None, yPos=None):
    if not isinstance(obj, GObj):
        raise Exception('Argument1 must be a graphic object'
                        '\nValid Example: add(circle1)')
    elif xPos is not None and not isinstance(xPos, (int, float)):
        raise Exception('Argument2 must be a number'
                        '\nValid Example: add(circle1, 10, 10)')
    elif yPos is not None and not isinstance(yPos, (int, float)):
        raise Exception('Argument3 must be a number'
                        '\nValid Example: add(circle1, 10, 10)')
    elif obj in window.world:
        raise Exception('Object has already been added to the world')

    window.add(obj, xPos, yPos)

    if isinstance(obj, GComp):
            for o in obj.objs:
                if o._type == 'Button':
                    o.update()

def remove(obj):
    if not isinstance(obj, GObj):
        raise Exception('Argument must be a graphic object'
                        '\nValid Example: remove(circle1)')
    window.remove(obj) 
    
def removeAll(): 
    window.world = []

def setCaption(message):
    if not isinstance(message, str):
        raise Exception("Argument must be a string"
                        "\nValid Example: setCaption('This is the caption')")
    window.setCaption(message)

def setWidth(width):
    if not isinstance(width, (int, float)):
        raise Exception('Argument must be a number'
                        '\nValid Example: setWidth(1000)')
    window.setWidth(width)
    
def setHeight(height):
    if not isinstance(height, (int, float)):
        raise Exception('Argument must be a number'
                        '\nValid Example: setHeight(1000)')
    window.setHeight(height)

def getWidth():
    return window.getWidth()

def getHeight():
    return window.getWidth()
    
def setSize(width, height):
    if not isinstance(width, (int, float)):
        raise Exception('Argument1 must be a number'
                        '\nValid Example: setSize(1000, 800)')
    if not isinstance(height, (int, float)):
        raise Exception('Argument2 must be a number'
                        '\nValid Example: setHeight(1000, 800)')
    window.setSize(width, height)

def setColor(color):
    if not isinstance(color, tuple) or not len(color) == 3:
        raise Exception('Argument must be a color'
                        '\nValid Example: setColor(RED)'
                        '\n               setColor((0, 0, 19))')
    window.setColor(color)

def makeColorRGB(r,g,b):
    c = (r, g, b)
    for v in c:
        if not isinstance(v, (int, float)):
            raise ValueError('Arguments must be numbers'
                             '\nValid Example: makeColorRGB(127, 0, 255)')
        if v > 255 or v < 0:
            raise ValueError('Arguments must be posative numbers less than 256'
                             '\nValid Example: makeColorRGB(127, 0, 255)')
    return c

def makeColorHex(hexValue):
    if len(hexValue) != 6:
        raise ValueError('Argument for hex code should be six characters long'
                         '\nValid Example: makeColorHex(7F00FF)')
    hexValue = str(hexValue).upper() + "000000"  # Conversion and buffer so it doesn't error out if it gets weird inputs.
    for ch in hexValue:
        if not '0' <= ch <= '9' and not 'A' <= ch <= 'F':
            raise ValueError('Argument for hex code should only contain numeric values and letters A-F'
                             '\nValid Example: makeColorHex(7F00FF)')
    r = int(hexValue[:2], 16)
    g = int(hexValue[2:4], 16)
    b = int(hexValue[4:6], 16)
    return r, g, b


####### Engine Starting/Stoping

def start(thread=False):
    global started
    started = True
    Engine.start(window, thread)

def stop():
    Engine.stop()


######## Event Handling
# dummy mouseClicked handler
def mouseClickedEvent(handle):
    Events.addMouseClickedEvent(handle)

def mc(evt):
    return

mouseClickedEvent(mc)

#dummy mouseReleased handler
def mouseReleasedEvent(handle):
    Events.addMouseReleasedEvent(handle)

def mr(evt):
    return

mouseReleasedEvent(mr)

#dummy mouseMoved handler
def mouseMovedEvent(handle):
    Events.addMouseMovedEvent(handle)

def mm(evt):
    return

mouseMovedEvent(mm)

#dummy keyPressed Event
def keyPressedEvent(handle):
    Events.addKeyPressedEvent(handle)

def kp(evt):
    return

keyPressedEvent(kp)

#dummmy keyReleasedEvent
def keyReleasedEvent(handle):
    Events.addKeyReleasedEvent(handle)

def kr(evt):
    return

keyReleasedEvent(kr)

#dummy mouseDraggedEvent
def mouseDraggedEvent(handle):
    Events.addMouseDraggedEvent(handle)

def md(evt):
    return

mouseDraggedEvent(md)

def waitForClick():
    Events.waitForClick()
    
def pause(t):
    if not isinstance(t, (int, float)):
        raise Exception('Argument must be a number'
                        '\nValid Example: pause(1000)')
    if not g.multithreading and g.running:
        #print("fliping Display")
        Engine.flipOnce()
    time.sleep(t/1000.0)

###### Extra functions
""" objectAt functions need to be checked """
def objectAtLocation(pos): #--------------- several changes here
    if not isinstance(pos, tuple) or not len(pos) == 2:
        raise Exception('Argument must be a tuple of length 2'
                        '\nValid Example: objectAtLocation((100, 50))')
    # p = Rectangle(1, 1, WHITE, pos[0], pos[1]) #---don't know why this doesn't work
    p = Rectangle(1, 1, WHITE)                #---but these 2 statements
    p.setLocation(pos[0], pos[1])             #---make it work
    p.collidable = True  # New code in collisions make it necessary to put this in.
    # Objects have to be collidable, but not necessarily in the world, in order to detect hits.
    # We don't want to leave white squares everywhere so we just make it "collidable" without being in the world.
    # Reversing the world list in order to get stack ordering
    for obj in reversed(g.world.world):
        if collides(obj, p):
            return obj
    return None

def objectAtXY(x, y):
    if not isinstance(x, (int, float)):
        raise Exception('Argument1 must be a number'
                        '\nValid Example: objectAtXY(100, 70)')
    if not isinstance(y, (int, float)):
        raise Exception('Argument2 must be a number'
                        '\nValid Example: objectAtXY(100, 70)')
    pos = (x, y)
    return objectAtLocation(pos)

def sendForward(obj):
    if not isinstance(obj, GObj):
        raise Exception('Argument must be a graphic object'
                        '\nValid Example: sendForward(circle1)')
    if obj.isBackground:
        print('WARNING: A background cannot be moved.')
        return
    world = g.world.world
    index = world.index(obj)
    if index < len(world) - 1:
        world.insert(index+1, world.pop(index))

def sendBackward(obj):
    if not isinstance(obj, GObj):
        raise Exception('Argument must be a graphic object'
                        '\nValid Example: sendBackward(circle1)')
    if obj.isBackground:
        print('WARNING: A background cannot be moved.')
        return
    world = g.world.world
    index = world.index(obj)
    if index != 0:
        world.insert(index-1, world.pop(index))

def sendToFront(obj):
    if not isinstance(obj, GObj):
        raise Exception('Argument must be a graphic object'
                        '\nValid Example: sendToFront(circle1)')
    if obj.isBackground:
        print('WARNING: A background cannot be moved.')
        return
    world = g.world.world
    index = world.index(obj)
    world.append(world.pop(index))

def sendToBack(obj):
    if not isinstance(obj, GObj):
        raise Exception('Argument must be a graphic object'
                        '\nValid Example: sendToBack(circle1)')
    world = g.world.world
    background = None
    for o in world:
        if o.isBackground:
            background = o
    index = world.index(obj)
    if background is None or obj == background:
        world.insert(0, world.pop(index))
    else:
        world.insert(1, world.pop(index))


def setBackground(obj):
    if not isinstance(obj, (GObj, GComp)):
        raise Exception('Argument 1 must be an object')
    obj.setBackground()
    obj.collidable = False

def getBackground():
    for obj in g.world.world:
        if obj.isBackground:
            return obj

#-------------------------------------- my random functions
def randomSeed(val):
    random.seed(val)

def randomInt(min, max=None, step=None): #clever, I didn't know about None
    # returns random int in range [min, max] or [0, min]
    if step is None:
        if max is None:
            return random.randint(0, min)
        else:
            return random.randint(min, max)
    else:
        return random.randrange(min, max, step)

def randomDouble(min, max=None):
    # return random double in range [min, max) or [0, min)
    if max is None:
        return (min)*random.random()
    else:
        return (max-min)*random.random() + min

def randomBoolean():
    v = randomInt(1, 2)
    if v == 1: return True
    else: return False

def randomProbability(p):
    r = randomDouble(1)
    if r < p: return True
    else: return False
