from abc import abstractmethod
import pygame
from pygame.event import Event
from classes.Drawable.AbstractDrawable import AbstractDrawable
from classes.Drawable.AbstractHandler import AbstractHandler
from classes.Drawable.Combo import Combo
from classes.Fp import vectorDiff, overrides


class AbstractBlockHandler(AbstractHandler):

	@overrides(AbstractHandler)
	def __init__(self, context):
		super(AbstractBlockHandler, self).__init__(context)
		self.lastMousePos = 0,0

	def getBlock(self):
		""":rtype: classes.Drawable.Screen.Block.AbstractBlock"""
		return self.getContext()

	@classmethod
	@overrides(AbstractHandler)
	def calcActionDict(cls, blockClass) -> dict:
		return { Combo(pygame.KMOD_LCTRL, pygame.K_DELETE): blockClass.destroy, }

	@overrides(AbstractHandler)
	def handleMouseEvent(self, event: Event):
		mouseVector = vectorDiff(event.pos, self.lastMousePos) # TODO: we create new handler instance on each iteration loh
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1 and self.getBlock().calcIsResizeCornerPointed(event.pos):
				self.getBlock().isResizing = True

		elif event.type == pygame.MOUSEBUTTONUP:
			if self.getBlock().isResizing:
				self.getBlock().recalcSurfaceRecursively(-1)
				self.getBlock().isResizing = False

		elif event.type == pygame.MOUSEMOTION:

			if event.buttons[0]: # left mouse button hold
				if self.getBlock().isResizing:
					self.getBlock().sizeAddVector(mouseVector)
					self.getBlock().recalcSurfaceRecursively(1)
				else:
					self.getBlock().posAddVector(mouseVector)

			self.getBlock().calcIsResizeCornerPointed(event.pos)
			self.lastMousePos = event.pos

	@overrides(AbstractHandler)
	def handleSpecificEvent(self, event: Event):
		return {}