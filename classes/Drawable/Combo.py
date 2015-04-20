import pygame
from classes.Fp import overrides


class Combo(object):

	# TODO: __hash__, __equuals__

	def __init__(self, keyMods: int, keyCode: int):
		# TODO: left shift and right shift may be treaten separately - RESEARCH!
		self.keyMods = keyMods
		self.keyCode = keyCode

	@staticmethod
	def fromEvent(event: pygame.event):
		# excluding capslocks, numlocks, etc...
		keyMods = event.mod & (pygame.KMOD_ALT | pygame.KMOD_CTRL | pygame.KMOD_SHIFT)
		return Combo(keyMods, event.key)

	@staticmethod
	def getCharacterKeycodeList():
		return range(32, 123) # 122 - z, 32 - space

	@overrides(object)
	def __hash__(self) -> int:
		return int((self.keyCode << 4) + self.keyMods);

	@overrides(object)
	def __eq__(self, other):
		return self.__hash__() == other.__hash__()
