#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from AbstractBlock import AbstractBlock
from classes.Fp import *
from classes.NullBlock import NullBlock
import classes
from classes.Textfield import Textfield
from classes.Constants import Constants
from classes.AbstractDrawable import AbstractDrawable
from classes.Screen import Screen

class TextBlock(AbstractBlock):

	STATUS_BAR_HEIGHT = Constants.CHAR_HEIGHT
	DISPLAY_STATUS_BAR = False
	FOCUSED_BLOCK = NullBlock(Screen.getInstance()) # AbstractBlock

	DEFAULT_SIZE = [200,200]
	DEFAULT_POS = [50,50]
	DEFAULT_STATUS_STRING = u'{"Имя": "Ираклий", "Оценка": "0", "Кратко": "гузно", "Каммент": "ВсёХуйняДавайСначала"}'

	rate = 0

	def __init__(self, blockData=None):
		super(TextBlock, self).__init__(Screen.getInstance())
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
			frameColor = [0,255,0] if self == TextBlock.FOCUSED_BLOCK else [127,127,127]
			frameSurface = pygame.Surface([self.width, self.height])
			frameSurface.fill(frameColor)

			frameSurface.blit(self.getChildStatusInput().getSurface(),
					[Constants.BLOCK_FRAME_WIDTH, Constants.BLOCK_FRAME_WIDTH])

			frameSurface.blit(self.getChildTextfield().getSurface(), 
					[Constants.BLOCK_FRAME_WIDTH, self.getTextfieldTopIndent()])
				
			self.surface = frameSurface
			self.surfaceChanged = False

		if self.isResizeCornerPointed() and self.isPointed(classes.Screen.Screen.getInstance().calcMouseAbsolutePos()):
			pygame.draw.circle(self.surface, [0,0,255], [self.width, self.height], Constants.RESIZE_CORNER_RADIUS, 0)
		else:
			pygame.draw.circle(self.surface, [255,255,255], [self.width, self.height], Constants.RESIZE_CORNER_RADIUS, 0)


		return self.surface

	@overrides(AbstractDrawable)
	def recalcSurface(self):
		pass

	@overrides(AbstractDrawable)
	def recalcSize(self):
		pass

	@staticmethod
	def releaseFocus():
		defocused = TextBlock.FOCUSED_BLOCK
		TextBlock.FOCUSED_BLOCK = NullBlock(Screen.getInstance())
		defocused.recalcSurfaceBacursively()
		if isinstance(defocused, TextBlock): defocused.getSurface()
	
	def acquireFocus(self):
		defocused = TextBlock.FOCUSED_BLOCK
		TextBlock.FOCUSED_BLOCK = self
		defocused.recalcSurfaceBacursively()
		if isinstance(defocused, TextBlock): defocused.getSurface()
		self.recalcSurfaceBacursively()

	# abstract block methods

	@overrides(AbstractBlock)
	def isResizeCornerPointed(self):
		mousePos = classes.Screen.Screen.getInstance().calcMouseAbsolutePos()
		cornerPos = vectorSum(self.pos(), [self.width, self.height])
		return distanceBetween(mousePos, cornerPos) <= Constants.RESIZE_CORNER_RADIUS

	# getters/setters

	def getChildStatusInput(self):
		return self.childStatusInput

	def getFocusedInput(self):
		return self.getChildStatusInput() if TextBlock.DISPLAY_STATUS_BAR else self.getChildTextfield()

	@overrides(AbstractBlock)
	def getChildTextfield(self):
		return self.childTextfield

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
				'paragraphTextList': self.getChildTextfield().getParagraphTextList()}

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
