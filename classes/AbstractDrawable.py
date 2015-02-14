from classes.Fp import *
from classes.Constants import Constants
from abc import abstractmethod

class AbstractDrawable(object):

    width = 0
    height = 0
    left = 0
    top = 0

    surface = None
    surfaceChanged = True

    def __init__(self):
        self.width = 0
        self.height = 0
        self.left = 0
        self.top = 0

        self.surfaceChanged = True

        self.childList = []

    @abstractmethod
    def drawOn(self, surface, pos=[0,0]):
        raise NotImplementedError("Please Implement this method")

    @abstractmethod
    def recalcSize(self):
        raise NotImplementedError("Please Implement this method")
    
    @abstractmethod
    def getBitmap(self):
        raise NotImplementedError("Please Implement this method")

    def isPointed(self, pointerPos):
        return isPointInRect(pointerPos, (self.left, self.top, self.width, self.height))

    def sizeAddVector(self, vector):
        self.size( vectorSum(self.size(), vector) )

    def posAddVector(self, vector):
        self.pos( vectorSum(self.pos(), vector) )

    def size(self, value = None):
        if value != None:
            self.width = max(value[0], Constants.CHAR_WIDTH)
            self.height = max(value[1], Constants.CHAR_HEIGHT)

            for child in self.childList:
                child.recalcSize()
        return self.width, self.height
            
    def pos(self, value = None):
        if value:
            self.left = value[0]
            self.top = value[1]
        return self.left, self.top

    def getWidth(self):
        return self.size()[0]

    def setWidth(self, value):
        self.width = value

    def getHeight(self):
        return self.size()[1]