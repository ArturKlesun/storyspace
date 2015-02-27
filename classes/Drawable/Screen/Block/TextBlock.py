#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame

from classes.Drawable.Screen.Block.AbstractBlock import AbstractBlock
from classes.Drawable.Screen.Block.Textfield.AbstractTextfield import AbstractTextfield
from classes.Fp import *
from classes.Drawable.Screen.Block.Textfield.Textfield import Textfield
from classes.Constants import Constants
from classes.Drawable.AbstractDrawable import AbstractDrawable
import classes as huj


class TextBlock(AbstractBlock):

	STATUS_BAR_HEIGHT = Constants.CHAR_HEIGHT
	DISPLAY_STATUS_BAR = False

	DEFAULT_STATUS_STRING = '{"Имя": "Ираклий", "Оценка": "0", "Кратко": "гузно", "Каммент": "ВсёХуйняДавайСначала"}'

	rate = 0

	def __init__(self, parentScreen, blockData={}):
		self.childTextfield = None
		self.childStatusInput = None

		super(TextBlock, self).__init__(parentScreen, blockData)

		self.getChildStatusInput().setTextBgColor([191,191,191])
		self.getChildStatusInput().setTextColor([127,63,0])


	def __str__(self):
		return 'Block: ' + str(self.getChildTextfield())

	def __repr__(self):
		return self.__str__() + '\n'

	@overrides(AbstractDrawable)
	def getSurface(self):
		if self.surfaceChanged:
			self.recalcSurface()

		if self.calcIsResizeCornerPointed() and self.isPointed(self.getParent().calcMouseAbsolutePos()):
			pygame.draw.circle(self.surface, [0,0,255], [self.width, self.height], Constants.RESIZE_CORNER_RADIUS, 0)
		else:
			pygame.draw.circle(self.surface, [255,255,255], [self.width, self.height], Constants.RESIZE_CORNER_RADIUS, 0)


		return self.surface

	@overrides(AbstractDrawable)
	def recalcSurface(self):
		# TODO: draw frame from parent screen context, cause we store focused block there
		frameColor = [0,255,0] if self is self.getParent().getFocusedBlock() else [127,127,127]
		frameSurface = pygame.Surface([self.width, self.height])
		frameSurface.fill(frameColor)

		frameSurface.blit(self.getChildStatusInput().getSurface(),
				[Constants.BLOCK_FRAME_WIDTH, Constants.BLOCK_FRAME_WIDTH])

		frameSurface.blit(self.getChildTextfield().getSurface(),
				[Constants.BLOCK_FRAME_WIDTH, self.getTextfieldTopIndent()])

		self.surface = frameSurface
		self.surfaceChanged = False

	@overrides(AbstractDrawable)
	def getEventHandler(self):
		""":rtype: classes.Drawable.Screen.Block.FocusedTextBlockEventHandler.FocusedTextBlockEventHandler"""
		return huj.Drawable.Screen.Block.FocusedTextBlockEventHandler.FocusedTextBlockEventHandler(self)

	@overrides(AbstractDrawable)
	def getFocusedChild(self) -> AbstractTextfield:
		return self.getFocusedInput()

	@overrides(AbstractDrawable)
	def getDefaultSize(self):
		return self.__class__.DEFAULT_SIZE

	# getters/setters

	def getChildTextfield(self):
		if self.childTextfield is None: self.childTextfield = Textfield(self)
		return self.childTextfield

	def getChildStatusInput(self):
		if self.childStatusInput is None: self.childStatusInput = Textfield(self)
		return self.childStatusInput

	def getFocusedInput(self):
		return self.getChildStatusInput() if TextBlock.DISPLAY_STATUS_BAR else self.getChildTextfield()

	def calcTextfieldSize(self):
		return (self.getWidth() - self.getTextfieldRightIndent() - Constants.BLOCK_FRAME_WIDTH,
			self.getHeight() - self.getTextfieldTopIndent() - Constants.BLOCK_FRAME_WIDTH)

	def getTextfieldTopIndent(self):
		return Constants.BLOCK_FRAME_WIDTH + (TextBlock.STATUS_BAR_HEIGHT if TextBlock.DISPLAY_STATUS_BAR else 0)

	def getTextfieldRightIndent(self):
		# TODO: if scrollbar + scrollbar
		return Constants.BLOCK_FRAME_WIDTH

	@overrides(AbstractBlock)
	def getObjectStateInherited(self):
		return {'rate': self.rate, 'statusString': self.getChildStatusInput().getParagraphTextList(),
				'paragraphTextList': self.getChildTextfield().getParagraphTextList()}

	@overrides(AbstractBlock)
	def setObjectStateInherited(self, blockData):
		self.rate = blockData['rate'] if 'rate' in blockData else -1
		for parText in (blockData['paragraphTextList'] if 'paragraphTextList' in blockData else []):
			self.getChildTextfield().insertIntoText(parText + '\n')
		for parText in (blockData['statusString'] if 'statusString' in blockData else [TextBlock.DEFAULT_STATUS_STRING]):
			self.getChildStatusInput().insertIntoText(parText + '\n')

		self.getChildTextfield().setPointerPar(0)
		self.getChildTextfield().getCurPar().setPointerPos(0)
