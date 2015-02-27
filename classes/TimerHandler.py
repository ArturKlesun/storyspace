import pygame
from classes.Drawable.AbstractEventHandler import AbstractEventHandler
from classes.Drawable.Screen.Screen import Screen

from classes.Fp import isPointInRect, getVectorFromRectToPoint
from classes.Drawable.Screen import FocusedScreenEventHandler


class TimerHandler(object):

	FRAME_DELAY_IN_MILLISECONDS = 20
	
	def __init__(self, screenEventHandler: FocusedScreenEventHandler):
		self.iterationNo = 0
		self.screenEventHandler = screenEventHandler
		screenEventHandler.setTimerHandler(self)
		self.frameDelay = self.__class__.FRAME_DELAY_IN_MILLISECONDS
	
	def handleFrame(self):
		# TODO: in can not handle events quicker than frame delay, like holding backspace. Should handle some ammount of events per frame
		for event in pygame.event.get():
			self.screenEventHandler.handlePygameEvent(event, {})
		self.screenEventHandler.handleCustomEvent({'eventType': 'frameRefreshed'})

		Screen.getInstance().getSurface()
		pygame.display.flip()

		pygame.time.delay(self.frameDelay)

		self.iterationNo += 1
