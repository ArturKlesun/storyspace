#!/usr/bin/env python
# -*- coding: utf-8 -*-
import inspect

import sys

import pygame
from pygame.constants import *

from classes.Config import Config
from classes.Constants import Constants
from classes.Drawable.AbstractHandler import AbstractHandler
from classes.Drawable.Combo import Combo
from classes.Drawable.Screen.Block.ImageBlock import ImageBlock
from classes.Fp import vectorReverse, overrides, isPointInRect, getVectorFromRectToPoint, vectorMult
from classes.Drawable.Screen.Block.TextBlock import TextBlock


class ScreenHandler(AbstractHandler):

	def getScreen(self):
		""":rtype: classes.Drawable.Screen.Screen.Screen"""
		return self.getContext()

	@classmethod
	@overrides(AbstractHandler)
	def calcActionDict(cls, screenClass) -> dict:
		p = pygame
		ctrl = p.KMOD_LCTRL
		return {
			Combo(ctrl, p.K_o): Config.getInstance().readFromFile,
			Combo(ctrl, p.K_s): Config.getInstance().saveToFile,
			Combo(ctrl, p.K_t): TextBlock, # HOOOOOOOOOOOOOOOO class is function mazafaka HAAAAAAAAAAA
			Combo(ctrl, p.K_i): ImageBlock, # HOOOOOOOOOOOOOOOO class is function mazafaka HAAAAAAAAAAA
			Combo(ctrl, p.K_f): cls.switchFullscreen,
			Combo(ctrl, p.K_EQUALS): cls.scaleUp,
			Combo(ctrl, p.K_MINUS): cls.scaleDown,
		}

	@staticmethod
	def scaleUp(screen): screen.setScaleKoef(screen.getScaleKoef * 1.5)
	@staticmethod
	def scaleDown(screen): screen.setScaleKoef(screen.getScaleKoef * (1.5**-1))

	@staticmethod
	def switchFullscreen(screen):
		if not screen.getIsFullscreen():
			screen.lastSize = screen.size()
			screen.size(Constants.MONITOR_RESOLUTION)
		else:
			screen.size(screen.lastSize)

		screen.setIsFullscreen(not screen.getIsFullscreen())
		screen.recalcSize()

	@overrides(AbstractHandler)
	def handleMouseEvent(self, event):
		mouseVector = self.getScreen().getScaledVector(self.getScreen().getCurMousePos(), event.pos)

		if event.type == pygame.MOUSEBUTTONDOWN:
			bitMask = pygame.key.get_mods() & (pygame.KMOD_ALT | pygame.KMOD_CTRL | pygame.KMOD_SHIFT)

			if event.button == 1: # scroll-up

				blockList = self.getScreen().getBlockInFrameList()
				absoluteMousePos = self.getScreen().calcMouseAbsolutePos(event.pos)
				pointedBlockList = [block for block in blockList if block.isPointed(absoluteMousePos)]
				self.getScreen().releaseFocusedBlock()
				if len(pointedBlockList):
					pointedBlockList[0].acquireFocus() # TODO: z-index

			elif event.button == 4 and bitMask & pygame.KMOD_LCTRL: # scroll-up
				self.getScreen().scale(+1)
			elif event.button == 5 and bitMask & pygame.KMOD_LCTRL: #scroll-down
				self.getScreen().scale(-1)


		elif event.type == pygame.MOUSEMOTION:

			if event.buttons[1] or event.buttons[2]: # middle mouse button hold
				self.getScreen().moveCam( vectorReverse(mouseVector) );

			self.getScreen().setCurMousePos(event.pos)

	@overrides(AbstractHandler)
	def handleSpecificEvent(self, event):
		if event.type==VIDEORESIZE:
			self.getScreen().size(event.dict['size'])
			self.getScreen().recalcSize()

		elif event.type == pygame.QUIT:
			sys.exit()

	def handleCustomEvent(self, event: dict):
		if event['eventType'] == 'frameRefreshed':
			if self.getScreen().getIsFullscreen():
				borderRect = self.getScreen().getCameraBorderRect()
				if not isPointInRect(self.getScreen().getCurMousePos(), borderRect):
					self.getScreen().moveCam( getVectorFromRectToPoint(borderRect, self.getScreen().getCurMousePos()) )

	def setTimerHandler(self, timerHandler):
		self.timerHandler = timerHandler

	def getTimerHandler(self):
		return self.timerHandler