from abc import abstractmethod
import pygame
from pygame.event import Event
from classes.Drawable.AbstractEventHandler import AbstractEventHandler
from classes.Drawable.Screen.Block.AbstractBlock import AbstractBlock
from classes.Fp import vectorDiff, overrides


class AbstractFocusedBlockEventHandler(AbstractEventHandler):

	def getBlock(self) -> AbstractBlock:
		return self.getContext() # TODO: it should be passed from parent, not gotten from environment

	@overrides(AbstractEventHandler)
	def handleMouseEvent(self, event: Event, paramsFromParent: dict):
		if event.type == pygame.MOUSEBUTTONDOWN:
			if self.getBlock().calcIsResizeCornerPointed(): # TODO: and button is left mouse button
				self.getBlock().isResizing = True # TODO: getters/setters

		elif event.type == pygame.MOUSEBUTTONUP:
			if self.getBlock().isResizing:
				self.getBlock().recalcSurfaceRecursively(-1)
				self.getBlock().isResizing = False

		elif event.type == pygame.MOUSEMOTION:

			if event.buttons[0]: # left mouse button hold
				if self.getBlock().isResizing:
					self.getBlock().sizeAddVector( paramsFromParent['mouseVector'] )
					self.getBlock().recalcSurfaceRecursively(1)
				else:
					self.getBlock().posAddVector( paramsFromParent['mouseVector'] )

			self.getBlock().calcIsResizeCornerPointed()

		return {}

	@overrides(AbstractEventHandler)
	def handleKeydown(self, event: Event, paramsFromParent: dict):

		# excluding capslocks, numlocks, etc...
		bitMask = event.mod & (pygame.KMOD_ALT | pygame.KMOD_CTRL | pygame.KMOD_SHIFT)

		if bitMask & pygame.KMOD_LCTRL:

			# can do it instance, it has pros, for example no need to recalc ALL blocks
			# ----------------------
			# elif event.key == pygame.K_SLASH:
			# 	huj.TextBlock.TextBlock.DISPLAY_STATUS_BAR = not huj.TextBlock.TextBlock.DISPLAY_STATUS_BAR
			# 	for block in Screen.getChildBlockList():
			# 		block.size(block.size())
			# 		block.recalcSurfaceRecursively(1)

			if event.key == pygame.K_DELETE:
				self.getBlock().getParent().releaseFocusedBlock()
				self.getBlock().getParent().childList.remove(self.getBlock())

		self.handleKeydownInherited(event, paramsFromParent)
		return {}

	@abstractmethod
	def handleKeydownInherited(self, event: Event, paramsFromParent: dict):
		raise NotImplementedError("Please Implement this method for " + self.__class__.__name__)

	@overrides(AbstractEventHandler)
	def handleSpecificEvent(self, event: Event, paramsFromParent: dict):
		return {}