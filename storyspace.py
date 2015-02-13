#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from classes.Block import Block
from classes.EventHandler import EventHandler
from pygame.constants import *
from classes.Screen import Screen

FRAME_DELAY = 20

blockList = []
pygame.key.set_repeat(200, FRAME_DELAY)

while 1:
	EventHandler.handlePygame(blockList)

	Screen.screen.fill([0,0,0])
	for block in blockList: #: :type block: Block
		block.drawOn(Screen.screen)
	pygame.display.flip()
	pygame.time.delay(FRAME_DELAY)