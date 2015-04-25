from time import sleep
import pygame
from classes.Drawable.AbstractHandler import AbstractHandler
from classes.Drawable.Screen.Screen import Screen

from classes.Fp import isPointInRect, getVectorFromRectToPoint
from classes.Drawable.Screen import ScreenHandler


class TimerHandler(object):

	FRAME_DELAY_IN_MILLISECONDS = 20
	
	def __init__(self, screenHandler: ScreenHandler):
		self.iterationNo = 0
		self.screenHandler = screenHandler
		screenHandler.setTimerHandler(self)
		self.frameDelay = self.__class__.FRAME_DELAY_IN_MILLISECONDS
	
	def handleFrame(self):
		# TODO: in can not handle events quicker than frame delay, like holding backspace. Should handle some ammount of events per frame
		for event in pygame.event.get():
			self.screenHandler.handlePygameEvent(event)
		self.screenHandler.handleCustomEvent({'eventType': 'frameRefreshed'})

		Screen.getInstance().getSurface()
		pygame.display.flip()

		# pygame.time.delay(self.frameDelay)
		sleep(self.frameDelay / 1000)

		self.iterationNo += 1
