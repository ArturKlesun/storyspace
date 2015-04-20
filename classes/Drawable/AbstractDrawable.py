import pygame
from classes.Fp import *
from classes.Constants import Constants
from abc import abstractmethod, ABCMeta

class AbstractDrawable(metaclass=ABCMeta):

	width = 0
	height = 0
	left = 0
	top = 0
	
	def __init__(self, parent):
		self.parent = parent
		self.childList = []
		self.focusedIndex = -1
		self.surface = pygame.Surface(self.getDefaultSize())
		self.surfaceChanged = True

		if not self.getParent() is None: self.getParent().childList.append(self)
		self.handler = self.makeHandler()
		self.size(self.getDefaultSize())
		self.pos([0,0])

		self.recalcSurfaceBacursively()

	# abstract methods

	@abstractmethod
	def recalcSize(self):
		raise NotImplementedError("Please Implement this method for " + self.__class__.__name__)

	@abstractmethod
	def recalcSurface(self):
		raise NotImplementedError("Please Implement this method for " + self.__class__.__name__)

	@abstractmethod
	def makeHandler(self):
		""":rtype: classes.Drawable.AbstractHandler.AbstractHandler"""
		raise NotImplementedError("Please Implement this method for " + self.__class__.__name__)

	@abstractmethod
	def getChildList(self):
		""":rtype: list of AbstractDrawable"""
		raise NotImplementedError("Please Implement this method for " + self.__class__.__name__)

	# cuz it may be final
	# @abstractmethod
	# def getFocusedChild(self):
	# 	""":rtype: AbstractDrawable"""
	# 	raise NotImplementedError("Please Implement this method for " + self.__class__.__name__)

	@abstractmethod
	def getDefaultSize(self):
		raise NotImplementedError("Please Implement this method for " + self.__class__.__name__)

	@abstractmethod
	def getObjectState(self):
		raise NotImplementedError("Please Implement this method for " + self.__class__.__name__)

	@abstractmethod
	def setObjectState(self, objectData):
		raise NotImplementedError("Please Implement this method for " + self.__class__.__name__)

	# final methods

	def drawOnParent(self, shiftVector=[0,0]):
		self.getParent().surface.blit(self.getSurface(), vectorSum(self.pos(), vectorReverse(shiftVector)))

	# TODO: this method must not exist
	def recalcSurfaceRecursively(self, n=0):
		self.surfaceChanged = True
		if n == 0: return
		for child in self.childList:
			child.recalcSurfaceRecursively(n - 1)
	
	def recalcSurfaceBacursively(self):
		self.surfaceChanged = True
		if self.getParent() is not None: self.getParent().recalcSurfaceBacursively()

	def destroy(self):
		for child in self.childList:
			child.destroy()
		self.getParent().childList.remove(self)

	# getters

	def isPointed(self, pointerPos):
		return isPointInRect(pointerPos,(self.left, self.top, self.width, self.height) )

	def getAbsolutePos(self):
		return vectorSum(self.getParent().getAbsolutePos(), self.pos())

	def getRootParent(self): # love you recursion
		""":rtype: classes.Drawable.Screen.Screen.Screen"""
		if self.getParent() is None: return self
		else: return self.getParent().getRootParent()

	def getRect(self):
		return self.pos()[0], self.pos()[1], self.size()[0], self.size()[1]

	# field getters/setters

	def getHandler(self):
		""":rtype: classes.Drawable.AbstractHandler.AbstractHandler"""
		return self.handler

	def getParent(self):
		""":rtype: AbstractDrawable"""
		return self.parent;

	def getSurface(self):
		if self.surfaceChanged:
			self.recalcSurface()
			self.surfaceChanged = False
		return self.surface

	def getFocusedIndex(self) -> int:
		return self.focusedIndex

	def setFocusedIndex(self, value: int):
		if value < -1: value = -1
		if value >= len(self.getChildList()): value = len(self.getChildList()) - 1
		self.focusedIndex = value
		self.recalcSurfaceBacursively()
		return self

	def getFocusedChild(self):
		if self.getFocusedIndex() > -1: return self.getChildList()[self.getFocusedIndex()]
		else: return None

	# transformations

	def sizeAddVector(self, vector):
		self.size( vectorSum(self.size(), vector) )

	def posAddVector(self, vector):
		self.pos( vectorSum(self.pos(), vector) )

	def pos(self, value = None):
		if value:
			self.left = value[0]
			self.top = value[1]

			if self.getParent() is not None: self.getParent().recalcSurfaceBacursively()
		return self.left, self.top

	def size(self, value = None):
		if value is not None:
			self.width = max(value[0], Constants.CHAR_WIDTH)
			self.height = max(value[1], Constants.CHAR_HEIGHT)
			self.surface = pygame.Surface([self.width, self.height])
			self.recalcSurfaceBacursively()

			for child in self.childList:
				child.recalcSize()

		return self.width, self.height

	def setTop(self, value):
		self.top = value

	def setLeft(self, value):
		self.left = value

	def getWidth(self):
		return self.size()[0]

	def setWidth(self, value):
		self.size([value, self.size()[1]])

	def getHeight(self):
		return self.size()[1]

	def setHeight(self, value):
		self.size([self.size()[0], value])

	# event handles

	def focusNext(self): return self.getFocusedIndex() != self.setFocusedIndex(self.getFocusedIndex + 1).getFocusedIndex()
	def focusBack(self): return self.getFocusedIndex() != self.setFocusedIndex(self.getFocusedIndex - 1).getFocusedIndex()