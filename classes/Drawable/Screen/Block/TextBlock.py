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

	DEFAULT_SIZE = [200,200]
	DEFAULT_POS = [50,50]
	DEFAULT_STATUS_STRING = '{"Имя": "Ираклий", "Оценка": "0", "Кратко": "гузно", "Каммент": "ВсёХуйняДавайСначала"}'

	rate = 0

	def __init__(self, parentScreen, blockData=None):
		super(TextBlock, self).__init__(parentScreen)
		self.size(TextBlock.DEFAULT_SIZE)
		self.pos(TextBlock.DEFAULT_POS)

		self.childTextfield = Textfield(self)
		self.childStatusInput = Textfield(self) # TODO: create separate class
		self.getChildStatusInput().setTextBgColor([191,191,191])
		self.getChildStatusInput().setTextColor([127,63,0])

		if blockData is not None:
			self.setObjectState(blockData)

	def __str__(self):
		return 'Block: ' + str(self.getChildTextfield())

	def __repr__(self):
		return self.__str__() + '\n'

	@overrides(AbstractDrawable)
	def getSurface(self):
		if self.surfaceChanged:
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

		if self.isResizeCornerPointed() and self.isPointed(self.getParent().calcMouseAbsolutePos()):
			pygame.draw.circle(self.surface, [0,0,255], [self.width, self.height], Constants.RESIZE_CORNER_RADIUS, 0)
		else:
			pygame.draw.circle(self.surface, [255,255,255], [self.width, self.height], Constants.RESIZE_CORNER_RADIUS, 0)


		return self.surface

	@overrides(AbstractDrawable)
	def recalcSurface(self):
		pass

	@overrides(AbstractDrawable)
	def getEventHandler(self):
		""":rtype: classes.Drawable.Screen.Block.FocusedBlockEventHandler.FocusedBlockEventHandler"""
		return huj.Drawable.Screen.Block.FocusedBlockEventHandler.FocusedBlockEventHandler(self)

	@overrides(AbstractDrawable)
	def getFocusedChild(self) -> AbstractTextfield:
		return self.getFocusedInput()

	# getters/setters

	def getChildTextfield(self):
		return self.childTextfield

	def getChildStatusInput(self):
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

	def getObjectState(self):
		return {'rate': self.rate, 'pos': self.pos(), 'size': self.size(),
				'statusString': self.getChildStatusInput().getParagraphTextList(),
				'paragraphTextList': self.getChildTextfield().getParagraphTextList(),
				'blockClass': self.__class__.__name__}

	def setObjectState(self, fileData):
		self.pos(fileData['pos'] if 'pos' in fileData else TextBlock.DEFAULT_POS)
		self.size(fileData['size'] if 'size' in fileData else TextBlock.DEFAULT_SIZE)
		self.rate = fileData['rate'] if 'rate' in fileData else -1
		for parText in (fileData['paragraphTextList'] if 'paragraphTextList' in fileData else []):
			self.getChildTextfield().insertIntoText(parText + '\n')
		for parText in (fileData['statusString'] if 'statusString' in fileData else [TextBlock.DEFAULT_STATUS_STRING]):
			self.getChildStatusInput().insertIntoText(parText + '\n')

		self.getChildTextfield().setPointerPar(0)
		self.getChildTextfield().getCurPar().setPointerPos(0)
