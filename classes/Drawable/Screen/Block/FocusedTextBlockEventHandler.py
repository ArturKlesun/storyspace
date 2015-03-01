import pygame
from pygame.event import Event
from classes.Drawable.Screen.Block.AbstractFocusedBlockEventHandler import AbstractFocusedBlockEventHandler


class FocusedTextBlockEventHandler(AbstractFocusedBlockEventHandler):

	def handleKeydownInherited(self, event: Event, paramsFromParent: dict):

		if event.key == pygame.K_SLASH:
			self.getBlock().switchFocus()

