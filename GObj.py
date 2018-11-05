'''
Authors: Graham Montgomery, Preston Adger
Western State Colorado University

This file holds the Graphic objects for the library
'''

from Globals import *
from Constants import *
import Globals as g
import StartPy as s

#-------------------------------------------------------------------
class GObj:
    #constructor
    def __init__(self, color, x, y):
        self._lock = threading.Lock()
        self.cx = 0
        self.cy = 0
        self.x = x
        self.y = y
        self.color = color
        self.visible = True
        self.collidable = False
        self.isBackground = False
#-------------------------------------------------------------------      
    #simple movement
    def forward(self, obj, amount):
        obj.move(amount, 0)
#--------------------------------------------------------------------
        
    #setters
    def move(self, xv, yv):
        if not isinstance(xv, (int, float)):
            raise Exception('Argument1 must be a number'
                            '\nValid Example: circle1.move(10, 10)')
        if not isinstance(yv, (int, float)):
            raise Exception('Argument2 must be a number'
                            '\nValid Example: circle1.move(10, 10)')
        self.x += xv
        self.y += yv

    def setLocation(self, x, y):
        if not isinstance(x, (int, float)):
            raise Exception('Argument1 must be a number'
                            '\nValid Example: circle1.setLocation(10, 10)')
        if not isinstance(y, (int, float)):
            raise Exception('Argument2 must be a number'
                            '\nValid Example: circle1.setLocation(10, 10)')
        self.x = x
        self.y = y
        
    def setColor(self, color):
        if not isinstance(color, tuple) or not len(color) == 3:
            raise Exception('Argument must be a color'
                            '\nValid Example: circle1.setColor(Black)')
        if self._type == 'Image':
            print('WARNING: The color of an image cannot be changed')
        else:
            self.color = color

    def setVisible(self, val):
        if not isinstance(val, bool):
            raise Exception('Argument must be True or False'
                            '\nValid Example: circle1.setVisible(False)')
        self.visible = val

    def setBackground(self):
        if _isLabel(self):
            raise Exception('Button and Label objects cannot be set as background')
        for obj in g.world.world:
            if obj.isBackground:
                print('WARNING: Only one background may be set at a time. \n         '
                      'The background has been changed to the most recent set background.')
                obj.isBackground = False
        self.isBackground = True
        self.setWidth(g.world.width)
        self.setHeight(g.world.height)
        self.setLocation(0, 0)
        self.collidable = False
        s.sendToBack(self)

    #getters
    def getLocation(self):
        return (self.x, self.y)

    def getX(self): 
        return self.x

    def getY(self): 
        return self.y
    
    def getColor(self):
        return self.color

    def getVisible(self):
        return self.visible

    #threading
    def acquire(self):
        self._lock.acquire()
    def release(self):
        self._lock.release()
    def __setattr__(self, item, value):
        if item is "_lock":
            self.__dict__[item] = value
        else:
            self.acquire()
            self.__dict__[item] = value
            self.release()
    
    #miscellaneous      
    def __add__(self, obj):
        if type(obj) is GComp:
            return obj + self
        elif isinstance(obj, GObj):
            obj.cx = obj.x
            obj.x = 0
            obj.cy = obj.y
            obj.y = 0
            self.cx = self.x
            self.x = 0
            self.cy = self.y
            self.y = 0
            return GComp(self, obj)

#-------------------------------------------------------------------
class GComp(GObj):
    """ every bit of these needs to be checked """
    #constructor
    def __init__(self, obj1, obj2):
        GObj.__init__(self, WHITE, 0, 0)
        # Due to implemented resizing of GComps, Circles and Squares are replaced with Ovals and Rectangles
        obj1 = makeStretchable(obj1)
        obj2 = makeStretchable(obj2)
        self.objs = [obj1, obj2]
        self._type = 'GComp'
        self.isBackground = False

    #setters
    def move(self, xv, yv):
        if not isinstance(xv, (int, float)):
            raise Exception('Argument1 must be a number'
                            '\nValid Example: comp1.move(10, 10)')
        if not isinstance(yv, (int, float)):
            raise Exception('Argument2 must be a number'
                            '\nValid Example: comp1.move(10, 10)')
        self.x += xv
        self.y += yv
        for obj in self.objs:
            if obj._type == 'Button':
                obj.move(xv, yv)
            # Lines are not currently implemented
            # elif obj._type == "Line":
            #     obj.move(xv,yv)
        self.updateQualities()
        
    def setLocation(self, x, y):
        if not isinstance(x, (int, float)):
            raise Exception('Argument1 must be a number'
                            '\nValid Example: comp1.setLocation(10, 10)')
        if not isinstance(y, (int, float)):
            raise Exception('Argument2 must be a number'
                            '\nValid Example: comp1.setLocation(10, 10)')
        # the move method in button knows how to move all parts of the button, the GComp doesn't
        for obj in self.objs:
            if obj._type == 'Button':
                obj.move(x - self.x, y - self.y)

        self.x = x
        self.y = y

        # Commented out since Lines aren't implemented but may be in the future - Fall 2017 DF
        # for obj in self.objs:
        #     if obj._type == "Line":
        #         obj.setLocation(x, y)
        self.updateQualities()
        
    def setVisible(self, val):
        if not isinstance(val, bool):
            raise Exception('Argument must be True or False'
                            '\nValid Example: comp1.setVisible(False)')
        self.visible = val
        self.updateQualities()

    def setObjectColor(self, objNum, color):
        if not isinstance(objNum, (float, int)):
            raise Exception('Argument must be a number'
                            '\nValid Example: comp1.setObjectColor(1, BLUE)')
        if not isinstance(color, tuple) or not len(color) == 3:
            raise Exception('Argument must be a color'
                            '\nValid Example: comp1.setObjectColor(1, BLUE)')
        self.objs[objNum].setColor(color)
 

    def setBackground(self):
        # for o in self.objs:
        #     if _isLabel(o):
        #         raise Exception('Compound objects containing buttons or labels cannot be set as backgrounds.')
        for obj in g.world.world:
            if obj.isBackground:
                print('WARNING: Only one background may be set at a time. \n         '
                      'The background has been changed to the most recent set background.')
                obj.isBackground = False
        self.isBackground = True
        self.setWidth(g.world.width)
        self.setHeight(g.world.height)
        self.setLocation(0, 0)
        self.collidable = False
        s.sendToBack(self)

    def setScale(self, factor):
        if not isinstance(factor, (int, float)):
            raise ValueError(number_arg(1) + '\nValid Example: comp.setScale(2.5)')
        for obj in self.objs:
            obj.cx = int((obj.cx - self.cx)*factor + self.cx)
            obj.cy = int((obj.cy - self.cy)*factor + self.cy)
            obj.setScale(factor)
        self.updateQualities()

    def setWidth(self, width):
        if not isinstance(width, (int, float)):
            raise ValueError(number_arg(1) + '\nValid Example: comp.setWidth(100)')
        # all this work to prevent labels from being scaled
        objs = self.objs
        scalable_objs = [obj for obj in self.objs if not _isLabel(obj)]
        self.objs = scalable_objs
        scalable_width = self.getWidth()
        self.objs = objs
        all_width = self.getWidth()
        factor = (width - (all_width - scalable_width))/(scalable_width)
        for obj in self.objs:
            obj.cx = int((obj.cx - self.cx) * factor + self.cx)
            if obj._type == 'Button':
                obj.x = obj.cx
                obj.update()
            if not _isLabel(obj):
                obj.setWidth(int(obj.getWidth() * factor))
        self.updateQualities()

    def setHeight(self, height):
        if not isinstance(height, (int, float)):
            raise ValueError(number_arg(1) + '\nValid Example: comp.setHeight(75)')
        # all this work to prevent labels from being scaled
        objs = self.objs
        scalable_objs = [obj for obj in self.objs if not _isLabel(obj)]
        self.objs = scalable_objs
        scalable_height = self.getHeight()
        self.objs = objs
        all_height = self.getHeight()
        factor = (height - (all_height - scalable_height)) / (scalable_height)
        for obj in self.objs:
            obj.cy = int((obj.cy - self.cy) * factor + self.cy)
            if obj._type == 'Button':
                obj.y = obj.cy
                obj.update()
            if not _isLabel(obj):
                obj.setHeight(int(obj.getHeight() * factor))
        self.updateQualities()

    def setSize(self, width, height):
        if not isinstance(width, (int, float)):
            raise ValueError(number_arg(1) + '\nValid Example: comp.setSize(100, 75)')
        if not isinstance(height, (int, float)):
            raise ValueError(number_arg(2) + '\nValid Example: comp.setSize(100, 75)')
        self.setWidth(width)
        self.setHeight(height)


    #getters
    def getLocation(self):  # prior to this change was returning (0,0) no matter where the object was
        xmin = 10000
        ymin = 10000
        for obj in self.objs:
            if obj.x < xmin:
                xmin = obj.x
        for obj in self.objs:
            if obj.y < ymin:
                ymin = obj.y
                
            
        return (xmin ,ymin)

    def getObjectColor(self, objNum):
        if not isinstance(objNum, (float, int)):
            raise Exception('Argument must be a number'
                            '\nValid Example: comp1.getObjectColor(1)')
        return self.objs[objNum].getColor()
    
    def getWidth(self):
        maxX = -10000
        minX = 10000 
        for obj in self.objs:
            min, max = obj.getBox()
            if max[0] >= maxX:
                maxX = max[0]
            if min[0] <= minX:
                minX = min[0]
        return maxX-minX

    def getHeight(self):
        maxY = -10000
        minY = 10000  # DLS - 1/18 - # As a bonus? No more negative width/height readings from empty gcompounds.
        for obj in self.objs:
            min, max = obj.getBox()
            if max[1] >= maxY:
                maxY = max[1]
            if min[1] <= minY:
                minY = min[1]
        return maxY-minY

    #miscellaneous
    def updateQualities(self):
        for obj in self.objs:
            obj.x = self.x + obj.cx
            obj.y = self.y + obj.cy
            obj.setVisible(self.visible)

    def draw(self, window):
        for obj in self.objs:
            obj.draw(window)

    def __add__(self, obj):
        if type(obj) is GComp:
            self.objs += obj.objs
        elif isinstance(obj, GObj):
            obj = makeStretchable(obj)
            obj.cx = obj.x
            obj.x = 0
            obj.cy = obj.y
            obj.y = 0
            self.objs.append(obj)
        return self

    def getBox(self):
        maxX = 0
        maxY = 0
        minX = 10000
        minY = 10000
        for obj in self.objs:
                min, max = obj.getBox() 
                #Check min and max X
                if max[0] >= maxX:
                    maxX = max[0]
                if min[0] <= minX:
                    minX = min[0]
                #Check min and max Y
                if max[1] >= maxY:
                    maxY = max[1]
                if min[1] <= minY:
                    minY = min[1]
        return ((minX, minY), (maxX, maxY))
    
#-------------------------------------------------------------------
"""
# all of this needs to be checked
class Line(GObj):
    #constructor
    def __init__(self, thickness, color, x, y, x2, y2):
        GObj.__init__(self, color, x, y)
        self.x2 = x2
        self.y2 = y2
        self.thickness = thickness
        self._type = "Line"
        
    #setters
    def setWidth(self, thickness):
        self.thickness = thickness
         
    def setLocation(self, x, y):
        xDif = x-self.x
        yDif = y-self.y
        self.x = x
        self.y = y
        self.x2 = self.x2 + xDif
        self.y2 = self.y2 + yDif

    def setStartPoint(self, x, y):
        self.x = x
        self.y = y

    def setEndPoint(self, x2, y2):
        self.x2 = x2
        self.y2 = y2  
                 
    #getters
    def getThickness(self):
        return self.thickness
    
    def getX2(self):
        return self.x2
    
    def getY2(self):
        return self.y2
    
    def getStartPoint(self):
        return(self.x,self.y)

    def getEndPoint(self):
        return(self.x2,self.y2) 
    
    #miscellaneous
    def draw(self, window):
        if self.visible:
            pygame.draw.line(window, self.color, (self.x,self.y), (self.x2,self.y2), self.thickness)
            
    def move(self, xv, yv):
        self.x += xv
        self.y += yv
        self.x2 += xv
        self.y2 += yv
    

    def _getBox(self):
        x = self.x
        y = self.y
        w = self.x1 - self.x
        h = self.y1 - self.y
        return((x,y), (x + w,h + y))
"""
#-------------------------------------------------------------------
""" all of this needs to be checked """
"""
 class Point(GObj):
   
    #constructor
    def __init__(self, color, x = 0, y = 0):
        GObj.__init__(self, color, x, y)
        self._type = "Point"
        self.r = 2  # radius of the point

    #miscellaneous
    def draw(self, window):
        if self.visible:
            pygame.draw.circle(window, self.color, (int(self.x+self.r), int(self.y+self.r)), self.r, 0)

    def getBox(self):
        x = self.x
        y = self.y
        r = self.r
        return ((x, y),(x+2*r, y+2*r))  
"""
#-------------------------------------------------------------------

class Circle(GObj):
    # constructor
    def __init__(self, diam, color, x=0, y=0):
        if not isinstance(diam, int) and not isinstance(diam, float):
            raise ValueError(number_arg(1) + circle_ex)
        if not isinstance(color, tuple) or len(color) != 3:
            raise ValueError(color_arg(2) + circle_ex)
        if not isinstance(x, int) and not isinstance(x, float):
            raise ValueError(number_arg(3) + circle_ex)
        if not isinstance(y, int) and not isinstance(y, float):
            raise ValueError(number_arg(4) + circle_ex)

        GObj.__init__(self, color, x, y)
        self.diam = diam
        self._type = "Circle"

    # setters
    def setDiameter(self, diam):
        if not isinstance(diam, int) and not isinstance(diam, float):
            raise ValueError(number_arg(1) + '\nValid Example: c.setDiameter(10)')
        self.diam = diam

    def setWidth(self, width):
        if not isinstance(width, int) and not isinstance(width, float):
            raise ValueError(number_arg(1) + '\nValid Example: c.setWidth(10)')
        self.setDiameter(width)

    def setHeight(self, height):
        if not isinstance(height, int) and not isinstance(height, float):
            raise ValueError(number_arg(1) + '\nValid Example: c.setHeight(10)')
        self.setDiameter(height)


    def setSize(self, size):  # may need 3rd argument as '*args' -------------------------------------------
        if not isinstance(size, int) and not isinstance(size, float):
            raise ValueError(number_arg(1) + '\nValid Example: c.setSize(10)')
        self.diam = size

    def setScale(self, factor):
        if not isinstance(factor, (int, float)):
            raise ValueError(number_arg(1) + '\nValid Example: c.setScale(.5)')
        self.diam *= factor

    # getters
    def getDiameter(self):
        return self.diam

    def getWidth(self):
        return self.diam

    def getHeight(self):
        return self.diam

    # miscellaneous
    def draw(self, window):
        if self.visible:
            pygame.draw.circle(window, self.color, (int(self.x+self.diam/2), int(self.y+self.diam/2)), int(self.diam/2), 0)

    def getBox(self):
        x = self.x
        y = self.y
        r = self.diam/2
        return (x, y), (x+2*r, y+2*r)
    
# -------------------------------------------------------------------

class Square(GObj): 
    # constructor
    def __init__(self, width, color, x=0, y=0):
        if not isinstance(width, int) and not isinstance(width, float):
            raise ValueError(number_arg(1) + square_ex)
        if not isinstance(color, tuple) or len(color) != 3:
            raise ValueError(color_arg(2) + square_ex)
        if not isinstance(x, int) and not isinstance(x, float):
            raise ValueError(number_arg(3) + square_ex)
        if not isinstance(y, int) and not isinstance(y, float):
            raise ValueError(number_arg(4) + square_ex)
        GObj.__init__(self, color, x, y)
        self.width = width
        self._type = "Square"

    # setters
    def setWidth(self, width):
        if not isinstance(width, int) and not isinstance(width, float):
            raise ValueError(number_arg(1) + '\nValid Example: s.setWidth(10)')
        self.width = width

    def setHeight(self, height):
        if not isinstance(height, int) and not isinstance(height, float):
            raise ValueError(number_arg(1) + '\nValid Example: s.setHeight(10)')
        self.width = height

    def setSize(self, size, *args):
        if not isinstance(size, int) and not isinstance(size, float):
            raise ValueError(number_arg(1) + '\nValid Example: s.setSize(10)')
        self.width = size
        self.height = size

    def setScale(self, factor):
        if not isinstance(factor, (int, float)):
            raise ValueError(number_arg(1) + '\nValid Example: s.setScale(5)')
        self.width *= factor

    # getters
    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.width

    # miscellaneous
    def draw(self, window):
        if self.visible:
            pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width), 0)

    def getBox(self):
        x = self.x
        y = self.y
        w = self.width
        return (x, y), (x+w, y+w)  # should this be a 2d tuple?

# -------------------------------------------------------------------

class Oval(GObj):
    # constructor
    def __init__(self, width, height, color, x=0, y=0):
        if not isinstance(width, int) and not isinstance(width, float):
            raise ValueError(number_arg(1) + oval_ex)
        if not isinstance(height, int) and not isinstance(height, float):
            raise ValueError(number_arg(2) + oval_ex)
        if not isinstance(color, tuple) or len(color) != 3:
            raise ValueError(color_arg(3) + oval_ex)
        if not isinstance(x, int) and not isinstance(x, float):
            raise ValueError(number_arg(4) + oval_ex)
        if not isinstance(y, int) and not isinstance(y, float):
            raise ValueError(number_arg(5) + oval_ex)
        GObj.__init__(self, color, x, y)
        self.width = width
        self.height = height
        self._type = "Oval"
    
    # setters
    def setSize(self, width, height):
        if not isinstance(width, int) and not isinstance(width, float):
            raise ValueError(number_arg(1) + '\nValid Example: o.setSize(10, 20)')
        if not isinstance(height, int) and not isinstance(height, float):
            raise ValueError(number_arg(2) + '\nValid Example: o.setSize(10, 20)')
        self.width = width
        self.height = height
        
    def setWidth(self, width):
        if not isinstance(width, int) and not isinstance(width, float):
            raise ValueError(number_arg(1) + '\nValid Example: o.setWidth(20)')
        self.width = width
        
    def setHeight(self, height):
        if not isinstance(height, int) and not isinstance(height, float):
            raise ValueError(number_arg(1) + '\nValid Example: o.setHeight(20)')
        self.height = height
        
    def setScale(self, factor):
        if not isinstance(factor, (int, float)):
            raise ValueError(number_arg(1) + '\nValid Example: s.setScale(5)')
        self.width *= factor
        self.height *= factor

    # getters
    def getWidth(self):
        return self.width
    
    def getHeight(self):
        return self.height

    # miscellaneous
    def draw(self, window):
        if self.visible:
            pygame.draw.ellipse(window, self.color, (self.x, self.y, self.width, self.height), 0)

    def getBox(self):
        x = self.x
        y = self.y
        w = self.width
        h = self.height
        return (x, y), (x+w, y+h)

# -------------------------------------------------------------------

class Rectangle(GObj):
    # constructor
    def __init__(self, width, height, color, x=0, y=0):
        if not isinstance(width, int) and not isinstance(width, float):
            raise ValueError(number_arg(1) + rectangle_ex)
        if not isinstance(height, int) and not isinstance(height, float):
            raise ValueError(number_arg(2) + rectangle_ex)
        if not isinstance(color, tuple) or len(color) != 3:
            raise ValueError(color_arg(3) + rectangle_ex)
        if not isinstance(x, int) and not isinstance(x, float):
            raise ValueError(number_arg(4) + rectangle_ex)
        if not isinstance(y, int) and not isinstance(y, float):
            raise ValueError(number_arg(5) + rectangle_ex)

        GObj.__init__(self, color, x, y)
        self.width = width
        self.height = height
        self.pos = (x,y)
        self._type = "Rectangle"

    # setters
    def setSize(self, width, height):
        if not isinstance(width, int) and not isinstance(width, float):
            raise ValueError(number_arg(1) + '\nValid Example: r.setSize(10, 20)')
        if not isinstance(height, int) and not isinstance(height, float):
            raise ValueError(number_arg(2) + '\nValid Example: r.setSize(10, 20)')
        self.width = width
        self.height = height
        
    def setHeight(self, height):
        if not isinstance(height, int) and not isinstance(height, float):
            raise ValueError(number_arg(1) + '\nValid Example: r.setHeight(20)')
        self.height = height
        
    def setWidth(self, width):
        if not isinstance(width, int) and not isinstance(width, float):
            raise ValueError(number_arg(1) + '\nValid Example: r.setWidth(20)')
        self.width = width
        
    def setScale(self, factor):
        if not isinstance(factor, (int, float)):
            raise ValueError(number_arg(1) + '\nValid Example: s.setScale(5)')
        self.width *= factor
        self.height *= factor    

    # getters
    def getWidth(self):
        return self.width
    
    def getHeight(self):
        return self.height

    # miscellaneous
    def draw(self, window):
        if self.visible:
            pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height), 0)

    def getBox(self):
        x = self.x
        y = self.y
        w = self.width
        h = self.height
        return ((x, y),(x+w, y+h))

#-------------------------------------------------------------------

class Image(GObj):
    # currently has to be created after start()
    def __init__(self, filename, x=0, y=0, color=None):
        if not s.started:
            raise Exception('start() must be called before creating an image')
        GObj.__init__(self, color, x, y)
        self.filename = filename  
        self.image = pygame.image.load(filename).convert_alpha()
        self.size = self.image.get_rect().size
        self._type = 'Image'
        self.isBackground = False

    def setSize(self, w, h):
        if not isinstance(w, (int, float)):
            raise ValueError(number_arg(1) + '\nValid Example: img.setSize(100, 100)')
        if not isinstance(h, (int, float)):
            raise ValueError(number_arg(2) + '\nValid Example: img.setSize(100, 100)')
        self.image = pygame.transform.scale(self.image, (w, h))

    def setWidth(self, width):
        if not isinstance(width, (int, float)):
            raise ValueError(number_arg(1) + '\nValid Example: img.setWidth(100)')
        self.image = pygame.transform.scale(self.image, (width, int(self.getHeight())))

    def setHeight(self, height):
        if not isinstance(height, (int, float)):
            raise ValueError(number_arg(1) + '\nValid Example: img.setHeight(100)')
        self.image = pygame.transform.scale(self.image, (int(self.getWidth()), height))

    def setScale(self, factor):
        if not isinstance(factor, (int, float)):
            raise ValueError(number_arg(1) + '\nValid Example: img.setScale(.2)')
        self.setSize(int(self.getWidth()*factor), int(self.getHeight()*factor))

    def getSize(self):
        self.size = self.image.get_rect().size
        return self.size[0]

    def getWidth(self):
        self.size = self.image.get_rect().size
        return self.size[0]
         
    def getHeight(self):
        self.size = self.image.get_rect().size
        return self.size[1]

    def setBackground(self):
        window = g.world
        width = window.getWidth()
        height = window.getHeight()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.x = 0
        self.y = 0
        for obj in g.world.world:
            if obj._type == 'Image':
                if obj.isBackground:
                    print('WARNING: Only one background may be set at a time. \n         '
                          'The background has been changed to the most recent set background.')
                    obj.isBackground = False
        self.isBackground = True
        self.collidable = False
        s.sendToBack(self)

    def getBox(self):
        self.size = self.image.get_rect().size
        x = self.x
        y = self.y
        width = self.size[0]
        height = self.size[1]
        return ((x,y), (x+width, y+height))

    def draw(self, window):
        window.blit(self.image, (self.x,self.y))
        if self.isBackground:
            s.sendToBack(self)

#-------------------------------------------------------------------

class Label(GObj):
    #constructors
    def __init__(self, size, color, message, x=0, y=0):
        if not isinstance(size, int) and not isinstance(size, float):
            raise ValueError(number_arg(1) + label_ex)
        if not isinstance(color, tuple) or len(color) != 3:
            raise ValueError(color_arg(2) + label_ex)
        if not isinstance(message, str):
            raise ValueError(string_arg(3) + label_ex)
        if not isinstance(x, int) and not isinstance(x, float):
            raise ValueError(number_arg(4) + label_ex)
        if not isinstance(y, int) and not isinstance(y, float):
            raise ValueError(number_arg(5) + label_ex)
        GObj.__init__(self, color, x, y)
        self.message = message
        self.fontSize = size
        self.fontType = None
        self._type = 'Label'

    #setters
    def setFontSize(self, fontSize):
        if not isinstance(fontSize, int) and not isinstance(fontSize, float):
            raise ValueError(number_arg(1) + '\nValid Example: lbl.setFontSize(20)')
        self.fontSize = fontSize
        
    def setText(self, message):
        if not isinstance(message, str):
            raise ValueError(string_arg(1) + "\nValid Example: lbl.setText('Hi')")
        self.message = message    
        
    def setScale(self, factor):
        if not isinstance(factor, (int, float)):
            raise ValueError(number_arg(1) + '\nValid Example: lbl.setScale(5)')
        self.fontSize = int(round(self.fontSize*factor, 0))
        
    #getters
    def getFontSize(self):          
        return self.fontSize
        
    def getText(self):
        return self.message
    
    #miscellaneous
    def draw(self, window):
        if self.visible:
            window.blit(pygame.font.Font(self.fontType, self.fontSize).render(self.message, 1, self.color), (self.x, self.y))

    # Added  2017 DFFall
    def getWidth(self):
        w, h = pygame.font.Font(self.fontType, self.fontSize).size(self.message)
        return w

    def getHeight(self):
        w, h = pygame.font.Font(self.fontType, self.fontSize).size(self.message)
        return h

    def getBox(self):
        x = self.x
        y = self.y
        w = self.getWidth()
        h = self.getHeight()
        return ((x, y),(x+w, y+h))

    def setWidth(self, width):
        if not isinstance(width, (int, float)):
            raise ValueError(number_arg(1) + '\nValid Example: l.setWidth(100)')
        w, h = pygame.font.Font(self.fontType, self.fontSize).size(self.message)
        while w < width:
            self.fontSize += 1
            w, h = pygame.font.Font(self.fontType, self.fontSize).size(self.message)
        while w > width:
            self.fontSize -= 1
            if self.fontSize < 1:
                raise ValueError('The given width is too small for the text. Reduce the text or give a larger width')
            w, h = pygame.font.Font(self.fontType, self.fontSize).size(self.message)

    def setHeight(self, height):
        if not isinstance(height, (int, float)):
            raise ValueError(number_arg(1) + '\nValid Example: l.setHeight(25)')
        w, h = pygame.font.Font(self.fontType, self.fontSize).size(self.message)
        while h < height:
            self.fontSize += 1
            w, h = pygame.font.Font(self.fontType, self.fontSize).size(self.message)
        while h > height:
            self.fontSize -= 1
            if self.fontSize < 1:
                raise ValueError('The given height is too small. A larger height is required.')
            w, h = pygame.font.Font(self.fontType, self.fontSize).size(self.message)

#-------------------------------------------------------------------

class Button(GObj):
    #constructor
    def __init__(self, fontSize, fontColor, bkgColor, text, x=0, y=0, fontType=None):
        if not isinstance(text, str):
            raise ValueError(string_arg(1) + button_ex)
        if not isinstance(fontSize, (int, float)):
            raise ValueError(number_arg(2) + button_ex)
        if not isinstance(fontColor, tuple) or len(fontColor) != 3:
            raise ValueError(color_arg(3) + button_ex)
        if not isinstance(bkgColor, tuple) or len(bkgColor) != 3:
            raise ValueError(color_arg(4) + button_ex)
        if not isinstance(x, (int, float)):
            raise ValueError(number_arg(4) + button_ex)
        if not isinstance(y, (int, float)):
            raise ValueError(number_arg(5) + button_ex)
        # error for font type?

        GObj.__init__(self, bkgColor, x, y)
        self.text = text
        self.fontSize = fontSize
        self.fontType = fontType
        self.fontColor = fontColor
        self.bkgColor = bkgColor
        self.update()
        self._type = "Button"

    #setters
    def setText(self, text):
        if not isinstance(text, str):
            raise ValueError(string_arg(1) + '\nValid Example: b.setText(\'Text\')')
        self.text = text
        self.update()

    def setFontSize(self, size):
        if not isinstance(size, (int, float)):
            raise ValueError(number_arg(1) + '\nValid Example: b.setFontSize(24)')
        self.fontSize = size
        self.update()

    def setLocation(self, x, y):
        if not isinstance(x, (int, float)):
            raise ValueError(number_arg(1) + '\nValid Example: b.setLocation(40, 40)')
        if not isinstance(y, (int, float)):
            raise ValueError(number_arg(2) + '\nValid Example: b.setLocation(40, 40)')
        self.x = x
        self.y = y
        self.update()

    def setBackgroundColor(self, color):
        if not isinstance(color, tuple) or len(color) != 3:
            raise ValueError(color_arg(1) + '\nValid Example: b.setBackColor(RED)')
        self.bkgColor = color
        self.update()

    def setTextColor(self, color):
        if not isinstance(color, tuple) or len(color) != 3:
            raise ValueError(color_arg(1) + '\nValid Example: b.setTextColor(BLUE)')
        self.fontColor = color
        self.update()
        
    def setScale(self, factor):
        if not isinstance(factor, (int, float)):
            raise ValueError(number_arg(1) + '\nValid Example: s.setScale(5)')
        self.fontSize =200

    #getters
    def getText(self):
        return self.text
   
    def getFontSize(self):
        return self.fontSize

    def getBackgroundColor(self):
        return self.bkgColor

    def getTextColor(self):
        return self.fontColor
    
    #miscellaneous
    def update(self, extra_width=0, extra_height=0):
        '''
        Renders the text and changes the width and height if set to auto
        gets called when any sets are called.
        Direct manipulation of the variables will not cause the update to happen (yet?)
        '''
        self.drawn_font = pygame.font.Font(None, self.fontSize)
        self.drawn_text = self.drawn_font.render(self.text, 1, self.fontColor)
    
        self.drawn_width = self.drawn_text.get_width()
        self.drawn_height = self.drawn_text.get_height()

        self.back = Rectangle(self.drawn_width + 10 + extra_width, self.drawn_height + 10 + extra_height, self.bkgColor,
                              x=self.x + 2, y=self.y + 2)
        self.border = Rectangle(self.drawn_width + 14 + extra_width, self.drawn_height + 14 + extra_height,
                                self.fontColor, x=self.x, y=self.y)

    def move(self, xv, yv):
        self.x += xv
        self.y += yv
        self.update()
 
    def draw(self, window):
        if self.visible:
            self.border.draw(window)
            self.back.draw(window)
            window.blit(self.drawn_text, (self.x + 6, self.y + 7))

    def getWidth(self):
        return self.border.getWidth()

    def getHeight(self):
        return self.border.getHeight()

    def getBox(self):
        x = self.x
        y = self.y
        w = self.getWidth()
        h = self.getHeight()
        return ((x, y), (x + w, y + h))

    def setWidth(self, width):
        if not isinstance(width, (int, float)):
            raise ValueError(number_arg(1) + '\nValid Example: b.setWidth(100)')
        w, h = pygame.font.Font(self.fontType, self.fontSize).size(self.text)
        while w < width - 14:
            self.fontSize += 1
            w, h = pygame.font.Font(self.fontType, self.fontSize).size(self.text)
        while w > width - 14:
            self.fontSize -= 1
            if self.fontSize < 1:
                raise ValueError('The given width is too small for the text. Reduce the text or give a larger width')
            w, h = pygame.font.Font(self.fontType, self.fontSize).size(self.text)
        diff = width - w - 14
        self.update(extra_width=diff)

    def setHeight(self, height):
        if not isinstance(height, (int, float)):
            raise ValueError(number_arg(1) + '\nValid Example: b.setHeight(25)')
        w, h = pygame.font.Font(self.fontType, self.fontSize).size(self.text)
        while h < height - 14:
            self.fontSize += 1
            w, h = pygame.font.Font(self.fontType, self.fontSize).size(self.text)
        while h > height - 14:
            self.fontSize -= 1
            if self.fontSize < 1:
                raise ValueError('The given height is too small. A larger height is required.')
            w, h = pygame.font.Font(self.fontType, self.fontSize).size(self.text)

        diff = height - h - 14
        self.update(extra_height=diff)

#-------------------------------------------------------------------

# Changes Circles to Ovals and Squares to Rectangles so GComps can stretch horizontally or vertically
def makeStretchable(obj):
    if obj._type == 'Circle':
        obj = Oval(obj.getDiameter(), obj.getDiameter(), obj.getColor(), obj.x, obj.y)
    elif obj._type == 'Square':
        obj = Rectangle(obj.getWidth(), obj.getWidth(), obj.getColor(), obj.x, obj.y)
    return obj

def collides(obj1, obj2):
    if not isinstance(obj1, GObj):
        raise Exception('Argument1 must be a graphic object'
                        '\nValid Example: collides(circle1, circle2)')
    if not isinstance(obj2, GObj):
        raise Exception('Argument2 must be a graphic object'
                        '\nValid Example: collides(circle1, circle2)')

    if obj1 is None or obj2 is None or not obj1.collidable or not obj2.collidable:
        return False

    box1 = obj1.getBox()
    box2 = obj2.getBox()
    xmin = 0
    xmax = 0
    ymin = 0
    ymax = 0
    w = 0
    h = 0
    if box1[0][0] < box2[0][0]:
        xmin = box1[0][0]
        xmax = box2[0][0]
        w = box1[1][0] - box1[0][0]
    else:
        xmin = box2[0][0]
        xmax = box1[0][0]
        w = box2[1][0] - box2[0][0]
    if box1[0][1] < box2[0][1]:
        ymin = box1[0][1]
        ymax = box2[0][1]
        h = box1[1][1] - box1[0][1]
    else:
        ymin = box2[0][1]
        ymax = box1[0][1]
        h = box2[1][1] - box2[0][1]
    return xmax - xmin < w and ymax - ymin < h

# Added this function so that type checking could be streamlined.
def  _isLabel(obj):
    return (type(obj) is Label) or (type(obj) is Button)

# strings for error throwing
def number_arg(x):
    return 'Argument ' + str(x) + ' must be a number'

def color_arg(x):
    return 'Argument ' + str(x) + ' must be a color or tuple of length 3'

def string_arg(x):
    return 'Argument ' + str(x) + ' must be letters'

circle_ex = '\nValid Examples: Circle(10, RED)\n                Circle(10, RED, 5, 5)'
rectangle_ex = '\nValid Examples: Rectangle(10, 20, BLUE)\n                Rectangle(10, 20, BLUE, 5, 5)'
oval_ex = '\nValid Examples: Oval(20, 10, RED)\n                Oval(20, 10, RED, 5, 5)'
square_ex = '\nValid Examples: Square(10, RED)\n                Square(10, RED, 5, 5)'
label_ex = "\nValid Examples: Label(12, RED, 'HELLO')\n                Label(12, RED, 'HELLO', 100, 100)"
button_ex = "\nValid Examples: Button('Button Text', 50, PINK, BLUE)\n                " \
            "Button('Button Text', 50, PINK, BLUE, 25, 25)"
