import pygame



pygame.init()
infoObject = pygame.display.Info()

class Constants(object):

	PROJECT_FONT = pygame.font.Font("UbuntuMono-R.ttf", 14)
	CHAR_WIDTH, CHAR_HEIGHT = PROJECT_FONT.size("w")
	
	RESIZE_CORNER_RADIUS = 10
	
	BLOCK_FRAME_WIDTH = 2

	MONITOR_RESOLUTION = (infoObject.current_w, infoObject.current_h)