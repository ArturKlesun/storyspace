from abc import abstractmethod, ABCMeta
import pygame
from pygame.event import Event
from classes.Drawable.Combo import Combo


class AbstractHandler(metaclass=ABCMeta):

	# static fields
	MOUSE_EVENT_TYPE_LIST = [pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP]
	actionDict = None

	def __init__(self, context):
		self.context = context
		self.keyBitmask = 0
		if self.__class__.actionDict is None: # i access it statically cuz i suppose it can cause leak of performance if do it for each instance
			self.__class__.actionDict = self.__class__.calcActionDict(context.__class__)

	@classmethod
	@abstractmethod
	def calcActionDict(cls, contextClass) -> dict:
		raise NotImplementedError("Please Implement this method for " + cls.__name__)

	def handlePygameEvent(self, event: pygame.event):
		if event.type == pygame.KEYDOWN: self.handleKey(Combo.fromEvent(event))
		elif event.type in self.MOUSE_EVENT_TYPE_LIST: self.handleMouseEvent(event)
		else: self.handleSpecificEvent(event)

		if self.getContext() is self.getContext().getRootParent(): # TODO: temporary solution. should think something about these events
			if self.getContext().getRootParent().getDialog() is not None:
				self.getContext().getRootParent().getDialog().getHandler().handlePygameEvent(event)
		if self.getContext().getFocusedChild() is not None:
			self.getContext().getFocusedChild().getHandler().handlePygameEvent(event)

	def handleKey(self, combo: Combo) -> bool:
		child = self.getContext().getFocusedChild()
		childDid = child is not None and child.getHandler().handleKey(combo)
		return childDid or self.handleKeyFinal(combo) in [True, None]

	def handleKeyFinal(self, combo: Combo) -> bool:
		return combo in self.__class__.actionDict and self.__class__.actionDict.get(combo)(self.getContext())

	# override me please!
	def handleMouseEvent(self, event: Event):
		pass

	# override me please!
	def handleSpecificEvent(self, event: Event):
		pass

	def getContext(self):
		""":rtype: classes.Drawable.AbstractDrawable.AbstractDrawable"""
		return self.context
