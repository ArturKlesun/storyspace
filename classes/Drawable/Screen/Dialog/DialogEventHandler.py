import pygame
from pygame.event import Event
from classes.Drawable.AbstractEventHandler import AbstractEventHandler
from classes.Drawable.Screen.Dialog.Dialog import Dialog


class DialogEventHandler(AbstractEventHandler):

	def getDialog(self) -> Dialog:
		return self.getContext()

	def handleMouseEvent(self, event: Event, paramsFromParent: dict):
		return {}

	def handleSpecificEvent(self, event: Event, paramsFromParent: dict):
		return {}

	def handleKeydown(self, event: Event, paramsFromParent: dict):

		if event.key == pygame.K_RETURN:
			self.getDialog().retrieveSelectedOption()
			self.getDialog().destroy()
		elif event.key == pygame.K_UP:
			self.getDialog().movePointer(-1)
		elif event.key == pygame.K_DOWN:
			self.getDialog().movePointer(+1)

		return {}