from abc import abstractmethod
import pygame
from classes.Constants import Constants

from classes.Drawable.AbstractDrawable import AbstractDrawable
from classes.Fp import *
import classes as huj

class AbstractBlock(AbstractDrawable):

	DEFAULT_SIZE = [200,200]

	def __init__(self, parentScreen, blockData={}):
		super(AbstractBlock, self).__init__(parentScreen)

		self.isResizing = False
		self.isResizeCornerPointed = False

		self.setObjectState(blockData)

	@abstractmethod
	def getObjectStateInherited(self):
		raise NotImplementedError("Please Implement this method for " + self.__class__.__name__)

	@abstractmethod
	def setObjectStateInherited(self, blockData: dict):
		raise NotImplementedError("Please Implement this method for " + self.__class__.__name__)

	@abstractmethod
	def recalcSurfaceInherited(self):
		raise NotImplementedError("Please Implement this method for " + self.__class__.__name__)

	@overrides(AbstractDrawable)
	def recalcSurface(self):
		frameColor = [0,255,0] if self is self.getParent().getFocusedBlock() else [127,127,127]
		self.surface.fill(frameColor)
		self.recalcSurfaceInherited()
		if self.isResizeCornerPointed:
			pygame.draw.circle(self.surface, [0,0,255], [self.width, self.height], Constants.RESIZE_CORNER_RADIUS, 0)

	@overrides(AbstractDrawable)
	def recalcSize(self):
		pass

	@overrides(AbstractDrawable)
	def getDefaultSize(self):
		return self.__class__.DEFAULT_SIZE

	@overrides(AbstractDrawable)
	def destroy(self):
		self.getParent().releaseFocusedBlock()
		super(AbstractBlock, self).destroy()

	def getObjectState(self):
		objectState = {'pos': self.pos(), 'size': self.size(), 'blockClass': self.__class__.__name__}
		objectState.update(self.getObjectStateInherited())

		return objectState

	def setObjectState(self, blockData: dict):
		self.pos(blockData['pos'] if 'pos' in blockData else [0,0])
		self.size(blockData['size'] if 'size' in blockData else self.__class__.DEFAULT_SIZE)

		self.setObjectStateInherited(blockData)

	def calcIsResizeCornerPointed(self):
		mousePos = self.getParent().calcMouseAbsolutePos()
		cornerPos = vectorSum(self.pos(), [self.width, self.height])

		result = distanceBetween(mousePos, cornerPos) <= Constants.RESIZE_CORNER_RADIUS and self.isPointed(mousePos)
		if result != self.isResizeCornerPointed:
				self.isResizeCornerPointed = result
				self.recalcSurfaceBacursively()

		return result

	@staticmethod
	def makeSuccessorByData(parentScreen, blockData):
		if blockData['blockClass'] == huj.Drawable.Screen.Block.TextBlock.TextBlock.__name__:
			return huj.Drawable.Screen.Block.TextBlock.TextBlock(parentScreen, blockData=blockData)
		elif blockData['blockClass'] == huj.Drawable.Screen.Block.ImageBlock.ImageBlock.__name__:
			return huj.Drawable.Screen.Block.ImageBlock.ImageBlock(parentScreen, blockData=blockData)
		else:
			raise Exception("Guzno")

	def acquireFocus(self):
		defocused = self.getParent().getFocusedBlock()
		self.getParent().setFocusedBlock(self)
		if defocused is not None:
			defocused.recalcSurfaceBacursively()
		self.recalcSurfaceBacursively()

