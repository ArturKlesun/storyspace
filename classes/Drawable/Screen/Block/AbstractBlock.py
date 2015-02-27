from abc import abstractmethod
from classes.Constants import Constants

from classes.Drawable.AbstractDrawable import AbstractDrawable
from classes.Fp import *
import classes as huj

class AbstractBlock(AbstractDrawable):

	DEFAULT_SIZE = [200,200]
	DISPLAY_STATUS_BAR = False

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

	@overrides(AbstractDrawable)
	def recalcSize(self):
		pass

	@overrides(AbstractDrawable)
	def getDefaultSize(self):
		return self.__class__.DEFAULT_SIZE

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

		result = distanceBetween(mousePos, cornerPos) <= Constants.RESIZE_CORNER_RADIUS
		if result != self.isResizeCornerPointed: # because we can
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

	# stupid ide

	@abstractmethod
	def getEventHandler(self):
		raise NotImplementedError("Please Implement this method for " + self.__class__.__name__)

	@abstractmethod
	def getSurface(self):
		raise NotImplementedError("Please Implement this method for " + self.__class__.__name__)

	@abstractmethod
	def recalcSurface(self):
		raise NotImplementedError("Please Implement this method for " + self.__class__.__name__)

	@abstractmethod
	def getFocusedChild(self):
		raise NotImplementedError("Please Implement this method for " + self.__class__.__name__)
