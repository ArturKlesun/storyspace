#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

import pygame
from pygame.constants import *

from classes.Config import Config
from classes.Drawable.AbstractEventHandler import AbstractEventHandler
from classes.Drawable.Screen.Block.ImageBlock import ImageBlock
from classes.Drawable.Screen.Screen import Screen
from classes.Fp import vectorDiff, vectorReverse, overrides, isPointInRect, getVectorFromRectToPoint, vectorMult
from classes.Drawable.Screen.Block.TextBlock import TextBlock
import classes as huj


class FocusedScreenEventHandler(AbstractEventHandler):

	def getScreen(self):
		""":rtype: classes.Drawable.Screen.Screen.Screen"""
		return self.getContext()

	@overrides(AbstractEventHandler)
	def handleMouseEvent(self, event, paramsFromParent: dict):

		mouseVector = vectorMult( vectorDiff(event.pos, Screen.CUR_MOUSE_POS), self.getScreen().scaleKoef**-1 )

		if event.type == pygame.MOUSEBUTTONDOWN:
			Screen.CUR_MOUSE_POS = event.pos

			blockList = self.getScreen().getBlockInFrameList()
			absoluteMousePos = self.getScreen().calcMouseAbsolutePos()
			pointedBlockList = [block for block in blockList if block.isPointed(absoluteMousePos)]
			self.getScreen().releaseFocusedBlock()
			if len(pointedBlockList):
				pointedBlockList[0].acquireFocus() # TODO: z-index

		elif event.type == pygame.MOUSEMOTION:

			if event.buttons[1] or event.buttons[2]: # middle mouse button hold
				self.getScreen().moveCam( vectorReverse(mouseVector) );

			Screen.CUR_MOUSE_POS = event.pos

		return {'mouseVector': mouseVector}

	@overrides(AbstractEventHandler)
	def handleKeydown(self, event, paramsFromParent: dict):

		# excluding capslocks, numlocks, etc...
		bitMask = event.mod & (pygame.KMOD_ALT | pygame.KMOD_CTRL | pygame.KMOD_SHIFT)

		if bitMask & pygame.KMOD_LCTRL:

			if event.key == pygame.K_s:
				Config.getInstance().saveToFile()
			elif event.key == pygame.K_o:
				self.getScreen().reconstruct(Config.getInstance().readDataFromFile())

			elif event.key == pygame.K_t:
				block = TextBlock(self.getScreen(), {'pos': self.getScreen().camPos()})
				block.acquireFocus()
			elif event.key == pygame.K_i:
				block = ImageBlock(self.getScreen(), {'pos': self.getScreen().camPos()})
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

			# slow tempo for debug
			elif event.key == pygame.K_LEFTBRACKET: # [
				self.getTimerHandler().frameDelay *= 2
			elif event.key == pygame.K_RIGHTBRACKET: # ]
				self.getTimerHandler().frameDelay //= 2

		return {}

	@overrides(AbstractEventHandler)
	def handleSpecificEvent(self, event, paramsFromParent: dict):
		if event.type==VIDEORESIZE:
			self.getScreen().size(event.dict['size'])
			self.getScreen().recalcSize()

		elif event.type == pygame.QUIT:
			sys.exit()

		return {}

	def handleCustomEvent(self, event: dict):
		if event['eventType'] == 'frameRefreshed':
			if Screen.IS_FULLSCREEN: # TODO: it should be instance
				borderRect = Screen.getInstance().getCameraBorderRect()
				if not isPointInRect(Screen.CUR_MOUSE_POS, borderRect):
					Screen.getInstance().moveCam( getVectorFromRectToPoint(borderRect, Screen.CUR_MOUSE_POS) )

	def setTimerHandler(self, timerHandler):
		self.timerHandler = timerHandler

	def getTimerHandler(self):
		return self.timerHandler