from abc import abstractmethod
import pygame
from pygame.event import Event
from classes.Drawable.AbstractEventHandler import AbstractEventHandler
from classes.Drawable.Screen.Block.Textfield.AbstractInput import AbstractInput
from classes.Fp import overrides


class AbstractFocusedInputEventHandler(AbstractEventHandler):

	def getInput(self) -> AbstractInput:
		return self.getContext()

	@overrides(AbstractEventHandler)
	def handleMouseEvent(self, event: dict, paramsFromParent: dict):
		return {}

	def handleKeydown(self, event: Event, paramsFromParent: dict):
		# excluding capslocks, numlocks, etc...
		bitMask = event.mod & (pygame.KMOD_ALT | pygame.KMOD_CTRL | pygame.KMOD_SHIFT)
		if bitMask & pygame.KMOD_LCTRL:

			if event.key == pygame.K_LEFT:
				self.getInput().ctrlMovePointer(-1)
			elif event.key == pygame.K_RIGHT:
				self.getInput().ctrlMovePointer(1)

			elif event.key == pygame.K_BACKSPACE:
				self.getInput().ctrlDeleteFromText(-1)
			elif event.key == pygame.K_DELETE:
				self.getInput().ctrlDeleteFromText(1)

		elif not bitMask or bitMask == pygame.KMOD_LSHIFT or bitMask == pygame.KMOD_RSHIFT:

			if event.key == pygame.K_LEFT:
				self.getInput().movePointer(-1)

			elif event.key == pygame.K_RIGHT:
				self.getInput().movePointer(1)

			elif event.key == pygame.K_BACKSPACE:
				self.getInput().deleteFromText(-1)

			elif event.key == pygame.K_DELETE:
				self.getInput().deleteFromText(1)

			elif len(event.unicode):
				self.getInput().insertIntoText(event.unicode)

		return self.handleKeydownInherited(event, paramsFromParent)

	#@abstractmethod
	def handleKeydownInherited(self, event: Event, paramsFromParent: dict):
		return {}
		# raise NotImplementedError("Please Implement this method for " + self.__class__.__name__)

	@overrides(AbstractEventHandler)
	def handleSpecificEvent(self, event: dict, paramsFromParent: dict):
		return {}