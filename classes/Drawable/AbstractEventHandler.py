from abc import abstractmethod, ABCMeta
import pygame
from pygame.event import Event
from classes.Fp import vectorDiff


class AbstractEventHandler(metaclass=ABCMeta):

	MOUSE_EVENT_TYPE_LIST = [pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP]

	def __init__(self, context):
		self.context = context

	def getContext(self):
		""":rtype: classes.Drawable.AbstractDrawable.AbstractDrawable""" # i could specify that context is instance of AbstractDrawable, but python won't allow circular imports easily. Pidr.
		return self.context

	def handlePygameEvent(self, event: Event, paramsFromParent: dict = {}): # TODO: this paramsFromParent actually is bad, just temporary solution
		if event.type == pygame.KEYDOWN:
			paramsFromParent.update(self.handleKeydown(event, paramsFromParent))
		elif event.type in self.MOUSE_EVENT_TYPE_LIST:
			paramsFromParent.update(self.handleMouseEvent(event, paramsFromParent))
		else:
			paramsFromParent.update(self.handleSpecificEvent(event, paramsFromParent))

		if self.getContext().getFocusedChild() is not None:
			self.getContext().getFocusedChild().getEventHandler().handlePygameEvent(event, paramsFromParent)

	@abstractmethod
	def handleMouseEvent(self, event: Event, paramsFromParent: dict):
		raise NotImplementedError("Please Implement this method for " + self.__class__.__name__)

	@abstractmethod
	def handleKeydown(self, event: Event, paramsFromParent: dict):
		raise NotImplementedError("Please Implement this method for " + self.__class__.__name__)

	@abstractmethod
	def handleSpecificEvent(self, event: Event, paramsFromParent: dict):
		raise NotImplementedError("Please Implement this method for " + self.__class__.__name__)
