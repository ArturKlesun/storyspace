#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

import pygame
from pygame.constants import *

from classes.Config import Config
from classes.Drawable.AbstractEventHandler import AbstractEventHandler
from classes.Fp import vectorDiff, vectorReverse
from classes.Drawable.Screen.Block.TextBlock import TextBlock


class FocusedScreenEventHandler(AbstractEventHandler):

	def getScreen(self): # i could specify, that screen is instance of the Screen, but python won't allow to use circular imports. Pidr.
		""":rtype: classes.Drawable.Screen.Screen.Screen"""
		return self.getContext()

	def handleMouseEvent(self, event):
		if event.type == pygame.MOUSEBUTTONDOWN:
			self.getScreen().CUR_MOUSE_POS = event.pos

			blockList = self.getScreen().getBlockInFrameList()
			absoluteMousePos = self.getScreen().calcMouseAbsolutePos()
			pointedBlockList = [block for block in blockList if block.isPointed(absoluteMousePos)]
			self.getScreen().releaseFocusedBlock()
			if len(pointedBlockList):
				pointedBlockList[0].acquireFocus() # TODO: z-index

		elif event.type == pygame.MOUSEMOTION:

			mouseVector = vectorDiff(event.pos, self.getScreen().CUR_MOUSE_POS)

			if event.buttons[1] or event.buttons[2]: # middle mouse button hold
				self.getScreen().moveCam( vectorReverse(mouseVector) );

			self.getScreen().CUR_MOUSE_POS = event.pos

	def handleKeydown(self, event):

		# excluding capslocks, numlocks, etc...
		bitMask = event.mod & (pygame.KMOD_ALT | pygame.KMOD_CTRL | pygame.KMOD_SHIFT)

		if bitMask & pygame.KMOD_LCTRL:

			if event.key == pygame.K_s:
				Config.saveToFile()
			elif event.key == pygame.K_o:
				Config.openFile()

			elif event.key == pygame.K_n:
				block = TextBlock(self.getScreen(), {'pos': self.getScreen().camPos()})
				block.acquireFocus()

			elif event.key == pygame.K_SLASH:
				TextBlock.DISPLAY_STATUS_BAR = not TextBlock.TextBlock.DISPLAY_STATUS_BAR
				for block in self.getScreen().getChildBlockList():
					block.size(block.size())
					block.recalcSurfaceRecursively(1)

			elif event.key == pygame.K_EQUALS:
				self.getScreen().scale(+1)
			elif event.key == pygame.K_MINUS:
				self.getScreen().scale(-1)

			elif event.key == pygame.K_f:
				self.getScreen().switchFullscreen()

	def handleSpecificEvent(self, event):
		if event.type==VIDEORESIZE:
			self.getScreen().size(event.dict['size'])
			self.getScreen().recalcSize()

		elif event.type == pygame.QUIT:
			sys.exit()
