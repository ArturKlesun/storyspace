#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from classes.Block import Block
from classes.EventHandler import EventHandler
from pygame.constants import *
from classes.Screen import Screen
from classes.TimerHandler import TimerHandler

blockList = []
pygame.key.set_repeat(150, 5)

while 1:
	EventHandler.handlePygame()

	Screen.getInstance().getSurface()
	pygame.display.flip()

	TimerHandler.getInstance().handleFrame()