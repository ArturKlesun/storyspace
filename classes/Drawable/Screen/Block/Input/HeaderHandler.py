import pygame
from classes.Drawable.AbstractHandler import AbstractHandler
from classes.Fp import overrides


class HeaderHandler(AbstractHandler):

	@classmethod
	@overrides(AbstractHandler)
	def calcActionDict(cls, headerClass) -> dict: pass

	@overrides(AbstractHandler)
	def handleSpecificEvent(self, event: dict): pass

	@overrides(AbstractHandler)
	def handleMouseEvent(self, event: dict): pass
