from abc import abstractmethod
from classes.Constants import Constants

from classes.Drawable.AbstractDrawable import AbstractDrawable
from classes.Fp import *
import classes as huj

class AbstractBlock(AbstractDrawable):

	def recalcSize(self):
		pass

	DISPLAY_STATUS_BAR = False

	def __init__(self, parentScreen, blockData=None):
		super(AbstractBlock, self).__init__(parentScreen)
		self.isResizing = False

	def isResizeCornerPointed(self):
		mousePos = self.getParent().calcMouseAbsolutePos()
		cornerPos = vectorSum(self.pos(), [self.width, self.height])
		return distanceBetween(mousePos, cornerPos) <= Constants.RESIZE_CORNER_RADIUS

	@staticmethod
	def makeSuccessorByData(parentScreen, blockData):

		if blockData['blockClass'] == 'TextBlock':
			return huj.Drawable.Screen.Block.TextBlock.TextBlock(parentScreen, blockData)
		elif blockData['blockClass'] == 'ImageBlock':
			return huj.Drawable.Screen.Block.ImageBlock.ImageBlock(parentScreen, blockData)
		else:
			return 'guzno'

	def acquireFocus(self):
		defocused = huj.Drawable.Screen.Screen.Screen.getInstance().getFocusedBlock()
		huj.Drawable.Screen.Screen.Screen.getInstance().setFocusedBlock(self)
		if defocused is not None:
			defocused.recalcSurfaceBacursively()
			defocused.getSurface()
		self.recalcSurfaceBacursively()

	@abstractmethod
	def getObjectState(self):
		raise NotImplementedError("Please Implement this method for " + self.__class__.__name__)

	@abstractmethod
	def setObjectState(self):
		raise NotImplementedError("Please Implement this method for " + self.__class__.__name__)
