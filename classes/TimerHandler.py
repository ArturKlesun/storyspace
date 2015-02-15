import pygame
from classes.EventHandler import EventHandler
from classes.Fp import isPointInRect
from classes.Screen import Screen

class TimerHandler(object):

	FRAME_DELAY_IN_MILLISECONDS = 40
	
	instance = None
	
	def __init__(self):
		self.iterationNo = 0
	
	@staticmethod
	def getInstance():
		if TimerHandler.instance is None:
			TimerHandler.instance = TimerHandler()
		return TimerHandler.instance
	
	def handleFrame(self):
		if not isPointInRect(Screen.CUR_MOUSE_POS, Screen.getInstance().getCameraBorderRect()):
			Screen.getInstance().moveCam(Screen.CUR_MOUSE_POS)
		pygame.time.delay(TimerHandler.FRAME_DELAY_IN_MILLISECONDS)
		self.iterationNo += 1