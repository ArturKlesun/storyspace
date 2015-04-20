import pygame
from pygame.event import Event
from classes.Drawable.AbstractHandler import AbstractHandler
from classes.Drawable.Combo import Combo
from classes.Fp import overrides


class DialogHandler(AbstractHandler):

	@classmethod
	@overrides(AbstractHandler)
	def calcActionDict(cls, contextClass) -> dict:
		return {
			Combo(0, pygame.K_RETURN): contextClass.retrieveSelectedOption,
			Combo(0, pygame.K_DOWN): contextClass.focusNext,
			Combo(0, pygame.K_UP): contextClass.focusBack,
		}

