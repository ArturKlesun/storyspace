import pygame
from pygame.constants import *

from classes.Drawable.AbstractDrawable import AbstractDrawable
from classes.Drawable.Combo import Combo
from classes.Drawable.Screen.Block.ImageBlock import ImageBlock
from classes.Drawable.Screen.Block.TextBlock import TextBlock
from classes.Drawable.Screen.Dialog.Dialog import Dialog
from classes.Drawable.Screen.Dialog.IDialogCaller import IDialogCaller
from classes.Drawable.Screen.ScreenHandler import ScreenHandler
from classes.Fp import isRectInRect, vectorSum, overrides, vectorMult, vectorDiff
from classes.Drawable.Screen.Block.AbstractBlock import AbstractBlock
from classes.Constants import Constants

class Screen(AbstractDrawable):

	CAM_INDENT_WIDTH = 30
	CAM_STEP_PER_FRAME = 25
	SCALE_CHANGE_STEP = 0.1
	DEFAULT_WINDOW_SIZE = [600,400]

	instance = None
	lastSize = (400,400)

	# abstract drawable's methods

	@overrides(AbstractDrawable)
	def __init__(self):
		self.scaleKoef = 1.0
		self.camPos([0,0])
		self.isFullscreen = False
		self.curMousePos = [0,0] # TODO: kinda deprecated

		super(Screen, self).__init__(None)

		self.recalcSize()

	@overrides(AbstractDrawable)
	def recalcSurface(self):
		# TODO: do it without tmpSurface one day, i.e. drawing each minimized child separately maybe
		tmpSurface = pygame.Surface( vectorMult(self.size(), self.scaleKoef**-1) ) # 50% processor time MAZAFAKAAAAA
		tmpSurface.fill([0,0,0])
		for block in self.getBlockInFrameList():
			tmpSurface.blit(block.getSurface(), vectorDiff( block.pos(), self.camPos() ) )
		if self.getDialog() is not None:
			tmpSurface.blit(self.getDialog().getSurface(), vectorDiff( self.getDialog().pos(), self.camPos() ))
		self.surface.blit(
			pygame.transform.smoothscale(tmpSurface, self.size())
				if self.scaleKoef > 0.5 else pygame.transform.scale(tmpSurface, self.size()), [0,0])

	def recalcSize(self):
		self.surface = pygame.display.set_mode(self.size(), HWSURFACE|DOUBLEBUF|(RESIZABLE if not self.getIsFullscreen() else FULLSCREEN))

	@overrides(AbstractDrawable)
	def makeHandler(self): return ScreenHandler(self)

	@overrides(AbstractDrawable)
	def getChildList(self): return self.getChildBlockList()

	@overrides(AbstractDrawable)
	def getDefaultSize(self):
		return Screen.DEFAULT_WINDOW_SIZE

	@overrides(AbstractDrawable)
	def getAbsolutePos(self):
		return 0,0

	# class specific methods

	@staticmethod
	def getInstance():
		""":rtype: Screen"""
		if Screen.instance is None:
			Screen.instance = Screen()
		return Screen.instance

	# cam methods

	def fitPointToScale(self, point: list):
		return vectorMult(point, self.scaleKoef**-1)

	def getScaledVector(self, wasPoint: list, becamePoint: list):
		return vectorDiff(self.fitPointToScale(becamePoint), self.fitPointToScale(wasPoint))

	def calcMouseAbsolutePos(self, realMousePos):
		return vectorSum( vectorMult(realMousePos, self.scaleKoef**-1), self.camPos())

	def moveCam(self, vector):
		self.camPos( vectorSum(self.camPos(), vector) )
		self.recalcSurfaceRecursively(1)

	def camPos(self, value=None):
		if value:
			self.camLeft = value[0]
			self.camTop = value[1]
		return self.camLeft, self.camTop

	def getCamRect(self):
		return self.camPos()[0], self.camPos()[1], int(self.size()[0] / self.scaleKoef), int(self.size()[1] / self.scaleKoef)

	def getCameraBorderRect(self):
		indent = Screen.CAM_INDENT_WIDTH
		return indent, indent, self.getWidth() - indent * 2, self.getHeight() - indent * 2

	def getBlockInFrameList(self):
		return [block for block in self.getChildBlockList() if isRectInRect(self.getCamRect(), block.getRect())]

	# child block methods

	def getChildBlockList(self):
		return [block for block in self.childList if isinstance(block, AbstractBlock)]

	def getObjectState(self):
		return {'jsonStructureFormatVersion': Constants.LAST_JSON_STRUCTURE_FORMAT_VERSION,
				'blockDataList': [b.getObjectState() for b in self.getChildBlockList()],}

	@overrides(AbstractDrawable)
	def setObjectState(self, screenData):
		self.clearBlockList()
		if isinstance(screenData, list): # legacy
			self.jsonStructureFormatVersion = Constants.PARAGRAPH_NOT_OBJECT_FORMAT_VERSION # just till legacy removed
			for blockData in screenData:
				BlockClass = self.getBlockClass(blockData['blockClass'])
				BlockClass(self).setObjectState(blockData)
		else:
			self.jsonStructureFormatVersion = screenData['jsonStructureFormatVersion']
			for blockData in screenData['blockDataList']:
				BlockClass = self.getBlockClass(blockData['blockClass'])
				BlockClass(self).setObjectState(blockData)

	@staticmethod
	def getBlockClass(className: str):
		""":rtype: classes.Drawable.Screen.Block.AbstractBlock"""
		for childClass in Screen.getChildClassList():
			if className == childClass.__name__: return childClass
		raise Exception("Unknown Block Class: [" + className + "]")

	@staticmethod
	def getChildClassList():
		return [TextBlock, ImageBlock]

	def getFocusedBlock(self):
		""":rtype: classes.Drawable.Screen.Block.AbstractBlock.AbstractBlock"""
		return self.getFocusedChild()

	def clearBlockList(self): del self.childList[:]

	def releaseFocusedBlock(self):
		if self.getFocusedIndex() > -1:
			defocused = self.getFocusedBlock()
			self.setFocusedIndex(-1)
			defocused.recalcSurfaceBacursively()

	# child dialog methods

	def interceptDialog(self, interceptor: IDialogCaller, params):
		if self.getDialog() is not None:
			self.getDialog().destroy()
		Dialog(self, interceptor, params)

	# general purpose getters

	def getIsFullscreen(self): return self.isFullscreen
	def setIsFullscreen(self, value: bool):
		self.isFullscreen = value
		return self

	def getCurMousePos(self): return self.curMousePos
	def setCurMousePos(self, value: list):
		self.curMousePos = value
		return self

	def getDialog(self) -> Dialog:
		dialogList = [dialog for dialog in self.childList if isinstance(dialog, Dialog)]
		return dialogList[0] if len(dialogList) else None

	# field getters/setters

	def getScaleKoef(self): return self.scaleKoef
	def setScaleKoef(self, value: int):
		self.scaleKoef = value
		return self