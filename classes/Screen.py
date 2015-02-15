import pygame
from pygame.constants import *
from classes.AbstractDrawable import AbstractDrawable
from classes.Fp import getVectorFromRectToPoint, isRectInRect, vectorSum
import classes

class Screen(AbstractDrawable):

	CAM_INDENT_WIDTH = 10
	CAM_STEP_PER_FRAME = 5

	CUR_MOUSE_POS = [0,0]
	IS_FULLSCREEN = False

	instance = None
	camLeft = 0
	camTop = 0

	screen = None

	def __init__(self):
		super(Screen, self).__init__(None)

		self.width = 400
		self.height = 400
		self.camLeft = 0
		self.camTop = 0

		self.recalcScreen()

	@staticmethod
	def getInstance():
		if Screen.instance is None:
			Screen.instance = Screen()
		return Screen.instance

	def getCameraBorderRect(self):
		indent = Screen.CAM_INDENT_WIDTH
		return indent, indent, self.getWidth() - indent * 2, self.getHeight() - indent * 2

	def moveCam(self, mousePos):
		vector = getVectorFromRectToPoint(self.getCameraBorderRect(), mousePos)
		self.camLeft += vector[0]
		self.camTop += vector[1]
		self.recalcSurfaceRecursively(1)

	def recalcScreen(self):
		self.surface = pygame.display.set_mode(self.size(), HWSURFACE|DOUBLEBUF|RESIZABLE)

	def switchFullscreen(self):
		if Screen.IS_FULLSCREEN:
			self.surface = pygame.display.set_mode(self.size(), HWSURFACE|DOUBLEBUF|FULLSCREEN)
			Screen.IS_FULLSCREEN = True
		else:
			self.recalcScreen()
			Screen.IS_FULLSCREEN = False

	def getSurface(self):
		if self.surfaceChanged:
			self.recalcSurface()
		return self.surface

	def recalcSurface(self):
		print self.camPos()
		self.surface.fill([0,0,0])
		for block in self.childList:
			if isRectInRect(self.getCamRect(), block.getRect()): 
				block.drawOnParent(self.camPos())

	def calcMouseAbsolutePos(self):
		return vectorSum(Screen.CUR_MOUSE_POS, self.camPos())

	def camPos(self, value=None):
		if value:
			self.camLeft = value[0]
			self.camTop = value[1]
		return self.camLeft, self.camTop

	def getCamRect(self):
		return self.camPos()[0], self.camPos()[1], self.size()[0], self.size()[1]

	def getBlockInFrameList(self):
		# TODO: "in frame"
		return [block for block in self.getChildBlockList() if isinstance(block, classes.Block.Block)]

	def getChildBlockList(self):
		return self.childList

	def clearBlockList(self):
		del self.childList[:]