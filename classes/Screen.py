import pygame
from pygame.constants import *

class Screen(object):

	screen = pygame.display.set_mode([400, 400], HWSURFACE|DOUBLEBUF|RESIZABLE)

	@staticmethod
	def setScreen(value):
		Screen.screen = value