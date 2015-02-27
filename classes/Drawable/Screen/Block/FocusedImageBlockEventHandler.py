import pygame
from pygame.event import Event
from classes.Clipboard import Clipboard
from classes.Drawable.Screen.Block.AbstractFocusedBlockEventHandler import AbstractFocusedBlockEventHandler
from classes.Drawable.Screen.Block.ImageBlock import ImageBlock


class FocusedTextBlockEventHandler(AbstractFocusedBlockEventHandler):

	def getBlock(self) -> ImageBlock:
		return super(FocusedTextBlockEventHandler, self).getBlock()

	def handleKeydownInherited(self, event: Event, paramsFromParent: dict):

		# excluding capslocks, numlocks, etc...
		bitMask = event.mod & (pygame.KMOD_ALT | pygame.KMOD_CTRL | pygame.KMOD_SHIFT)

		if bitMask & pygame.KMOD_LCTRL and event.key == pygame.K_v:
			self.getBlock().insertIntoText(Clipboard.get())