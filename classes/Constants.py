import pygame

pygame.init()

class Constants(object):

	PROJECT_FONT = pygame.font.Font("UbuntuMono-R.ttf", 10)
	CHAR_WIDTH, CHAR_HEIGHT = PROJECT_FONT.size("w")
	
	RESIZE_CORNER_RADIUS = 10
	
	BLOCK_FRAME_WIDTH = 2