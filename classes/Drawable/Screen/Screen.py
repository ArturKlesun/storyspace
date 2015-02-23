import pygame
from pygame.constants import *

from classes.Drawable.AbstractDrawable import AbstractDrawable
from classes.Fp import isRectInRect, vectorSum, overrides
from classes.Drawable.Screen.Block.AbstractBlock import AbstractBlock
from classes.Constants import Constants
import classes as huj


class Screen(AbstractDrawable):

	CAM_INDENT_WIDTH = 30
	CAM_STEP_PER_FRAME = 25
	SCALE_CHANGE_STEP = 0.5
	DEFAULT_WINDOW_SIZE = [600,400]

	CUR_MOUSE_POS = [0,0]
	IS_FULLSCREEN = False

	scaleKoef = 1.0

	instance = None
	lastSize = (400,400)

	# abstract drawable's methods

	@overrides(AbstractDrawable)
	def __init__(self):
		super(Screen, self).__init__(None)

		self.size(Screen.DEFAULT_WINDOW_SIZE)
		self.camPos([0,0])
		self.scaleKoef = 1.0
		self.focusedBlock = None

		self.recalcSize()

	@overrides(AbstractDrawable)
	def getSurface(self):
		if self.surfaceChanged:
			self.recalcSurface()
		return self.surface

	@overrides(AbstractDrawable)
	def recalcSurface(self):
		self.surface.fill([0,0,0])
		for block in self.childList:
			if isRectInRect(self.getCamRect(), block.getRect()):
				# TODO: scaling is alfa now
				block.drawOnParent(self.camPos())

	@overrides(AbstractDrawable)
	def recalcSize(self):
		self.surface = pygame.display.set_mode(self.size(), HWSURFACE|DOUBLEBUF|(RESIZABLE if not self.IS_FULLSCREEN else FULLSCREEN))

	@overrides(AbstractDrawable)
	def getEventHandler(self):
		return huj.Drawable.Screen.FocusedScreenEventHandler.FocusedScreenEventHandler(self)

	@overrides(AbstractDrawable)
	def getFocusedChild(self):
		return self.getFocusedBlock()

	# class specific methods

	@staticmethod
	def getInstance():
		""":rtype: Screen"""
		if Screen.instance is None:
			Screen.instance = Screen()
		return Screen.instance

	def switchFullscreen(self):
		if not Screen.IS_FULLSCREEN:
			self.lastSize = self.size()
			self.size(Constants.MONITOR_RESOLUTION)
		else:
			self.size(self.lastSize)

		Screen.IS_FULLSCREEN = not Screen.IS_FULLSCREEN
		self.recalcSize()

	# cam methods

	def calcMouseAbsolutePos(self):
		return vectorSum(Screen.CUR_MOUSE_POS, self.camPos())

	def scale(self, koef):
		self.scaleKoef += koef * Screen.SCALE_CHANGE_STEP
		self.recalcSurfaceRecursively(0)

	def moveCam(self, vector):
		self.camPos( vectorSum(self.camPos(), vector) )
		self.recalcSurfaceRecursively(1)

	def camPos(self, value=None):
		if value:
			self.camLeft = value[0]
			self.camTop = value[1]
		return self.camLeft, self.camTop

	def getCamRect(self):
		return self.camPos()[0], self.camPos()[1], self.size()[0], self.size()[1]

	def getCameraBorderRect(self):
		indent = Screen.CAM_INDENT_WIDTH
		return indent, indent, self.getWidth() - indent * 2, self.getHeight() - indent * 2

	def getBlockInFrameList(self):
		# TODO: "in frame"
		return self.getChildBlockList()

	# child block methods

	def getFocusedBlock(self): # i could specify that context is instance of AbstractBlock, but python won't allow circular imports easily. Pidr.
		""":rtype: classes.Drawable.Screen.Block.AbstractBlock"""
		return self.focusedBlock

	def setFocusedBlock(self, value):
		self.focusedBlock = value

	def getChildBlockList(self):
		return self.childList

	def reconstruct(self, blockDataList):
		self.clearBlockList()
		for blockData in blockDataList:
			AbstractBlock.makeSuccessorByData(self, blockData)

	def clearBlockList(self):
		del self.childList[:]

	def releaseFocusedBlock(self):
		defocused = self.getFocusedBlock()
		self.setFocusedBlock(None)
		if defocused is not None:
			defocused.recalcSurfaceBacursively()
			defocused.getSurface()