import pygame
from classes.Drawable.AbstractHandler import AbstractHandler
from classes.Fp import overrides


class HeaderHandler(AbstractHandler):

	@classmethod
	@overrides(AbstractHandler)
	def calcActionDict(cls, headerClass) -> dict: return {}

