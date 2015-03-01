import pygame
from pygame.constants import *

from classes.Drawable.AbstractDrawable import AbstractDrawable
from classes.Drawable.Screen.Dialog.Dialog import Dialog
from classes.Drawable.Screen.Dialog.IDialogCaller import IDialogCaller
from classes.Fp import isRectInRect, vectorSum, overrides, vectorMult, vectorDiff
from classes.Drawable.Screen.Block.AbstractBlock import AbstractBlock
from classes.Constants import Constants
import classes as huj


class Screen(AbstractDrawable):

	CAM_INDENT_WIDTH = 30
	CAM_STEP_PER_FRAME = 25
	SCALE_CHANGE_STEP = 0.1
	DEFAULT_WINDOW_SIZE = [600,400]

	CUR_MOUSE_POS = [0,0]
	IS_FULLSCREEN = False

	instance = None
	lastSize = (400,400)

	# abstract drawable's methods

	@overrides(AbstractDrawable)
	def __init__(self):
		self.scaleKoef = 1.0
		self.focusedBlock = None
		self.camPos([0,0])

		super(Screen, self).__init__(None)

		self.recalcSize()

	@overrides(AbstractDrawable)
	def recalcSurface(self):
		# TODO: do it without tmpSurface one day, i.e. drawing each minimized child separately maybe
		tmpSurface = pygame.Surface( vectorMult(self.size(), self.scaleKoef**-1) )
		tmpSurface.fill([0,0,0])
		for block in self.getBlockInFrameList():
			tmpSurface.blit(block.getSurface(), vectorDiff( block.pos(), self.camPos() ) )
		if self.getDialog() is not None:
			tmpSurface.blit(self.getDialog().getSurface(), vectorDiff( self.getDialog().pos(), self.camPos() ))
		self.surface.blit(
			pygame.transform.smoothscale(tmpSurface, self.size())
				if self.scaleKoef > 0.5 else pygame.transform.scale(tmpSurface, self.size()), [0,0])

	@overrides(AbstractDrawable)
	def recalcSize(self):
		self.surface = pygame.display.set_mode(self.size(), HWSURFACE|DOUBLEBUF|(RESIZABLE if not self.IS_FULLSCREEN else FULLSCREEN))

	@overrides(AbstractDrawable)
	def getEventHandler(self):
		return huj.Drawable.Screen.FocusedScreenEventHandler.FocusedScreenEventHandler(self)

	@overrides(AbstractDrawable)
	def getFocusedChild(self):
		return self.getFocusedBlock()

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
		return vectorSum( vectorMult(Screen.CUR_MOUSE_POS, self.scaleKoef**-1), self.camPos())

	def scale(self, koef):
		# TODO: move cam so that scale was centered
		self.scaleKoef *= 1.5**koef
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
		return self.camPos()[0], self.camPos()[1], int(self.size()[0] / self.scaleKoef), int(self.size()[1] / self.scaleKoef)

	def getCameraBorderRect(self):
		indent = Screen.CAM_INDENT_WIDTH
		return indent, indent, self.getWidth() - indent * 2, self.getHeight() - indent * 2

	def getBlockInFrameList(self):
		return [block for block in self.getChildBlockList() if isRectInRect(self.getCamRect(), block.getRect())]

	# child block methods

	def getFocusedBlock(self):
		""":rtype: classes.Drawable.Screen.Block.AbstractBlock"""
		return self.focusedBlock

	def setFocusedBlock(self, value):
		self.focusedBlock = value

	def getChildBlockList(self):
		return [block for block in self.childList if isinstance(block, AbstractBlock)]

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

	# child dialog methods

	def interceptDialog(self, interceptor: IDialogCaller, params):
		if self.getDialog() is not None:
			self.getDialog().destroy()
		Dialog(self, interceptor, params)

	# getters/setters

	def getDialog(self) -> Dialog:
		dialogList = [dialog for dialog in self.childList if isinstance(dialog, Dialog)]
		return dialogList[0] if len(dialogList) else None