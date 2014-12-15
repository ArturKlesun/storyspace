#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from classes.Block import Block
from classes.EventHandler import EventHandler


size = width, height = 400, 400
screen = pygame.display.set_mode(size)

blockList = []

while 1:
	EventHandler.handlePygame(blockList)
	screen.fill((0,0,0))
	for block in blockList: #: :type block: Block
		block.drawOn(screen)
	pygame.display.flip()