import pygame
from classes.Drawable.AbstractEventHandler import AbstractEventHandler
from classes.Drawable.Screen.Screen import Screen

from classes.Fp import isPointInRect, getVectorFromRectToPoint
from classes.Drawable.Screen import FocusedScreenEventHandler


class TimerHandler(object):

	FRAME_DELAY_IN_MILLISECONDS = 40
	
	def __init__(self, screenEventHandler: FocusedScreenEventHandler):
		self.iterationNo = 0
		self.screenEventHandler = screenEventHandler
	
	def handleFrame(self):
		# TODO: in can not handle events quicker than frame delay, like holding backspace. Should handle some ammount of events per frame
		for event in pygame.event.get():
			self.screenEventHandler.handlePygameEvent(event, {})

		Screen.getInstance().getSurface()
		pygame.display.flip()

		if Screen.IS_FULLSCREEN: # TODO: move it into FocusedScreenEventHandler
			borderRect = Screen.getInstance().getCameraBorderRect()
			if not isPointInRect(Screen.CUR_MOUSE_POS, borderRect):
				Screen.getInstance().moveCam( getVectorFromRectToPoint(borderRect, Screen.CUR_MOUSE_POS) )
		pygame.time.delay(TimerHandler.FRAME_DELAY_IN_MILLISECONDS)

		self.iterationNo += 1
