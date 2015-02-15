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

class Block(AbstractBlock):
	
	STATUS_BAR_HEIGHT = Constants.CHAR_HEIGHT
	DISPLAY_STATUS_BAR = False
	FOCUSED_BLOCK = NullBlock(Screen.getInstance()) # AbstractBlock

	rate = 0

	def __init__(self, blockData=None):
		super(Block, self).__init__(Screen.getInstance())
		self.size([200,200])
		self.pos([50,50])
		
		self.childTextfield = Textfield(self)
		self.childStatusInput = Textfield(self) # TODO: create separate class
		self.getChildStatusInput().setTextBgColor([191,191,191])
		self.getChildStatusInput().setTextColor([127,63,0])

		if blockData != None:
			self.setObjectState(blockData)
	
	def __str__(self):
		return 'Block: ' + str(self.getChildTextfield())

	def __repr__(self):
		return self.__str__() + '\n'

	@overrides(AbstractDrawable)
	def getSurface(self):
		if self.surfaceChanged:
			frameColor = [0,255,0] if self == Block.FOCUSED_BLOCK else [127,127,127]
			frameSurface = pygame.Surface([self.width, self.height])
			frameSurface.fill(frameColor)

			frameSurface.blit(self.getChildStatusInput().getSurface(),
					[Constants.BLOCK_FRAME_WIDTH, Constants.BLOCK_FRAME_WIDTH])

			frameSurface.blit(self.getChildTextfield().getSurface(), 
					[Constants.BLOCK_FRAME_WIDTH, self.getTextfieldTopIndent()])
				
			self.surface = frameSurface
			self.surfaceChanged = False

		if (self.isResizeCornerPointed() and self.isPointed(classes.Screen.Screen.CUR_MOUSE_POS)):
			pygame.draw.circle(self.surface, [0,0,255], [self.width, self.height], Constants.RESIZE_CORNER_RADIUS, 0)
		else:
			pygame.draw.circle(self.surface, [255,255,255], [self.width, self.height], Constants.RESIZE_CORNER_RADIUS, 0)


		return self.surface

	@overrides(AbstractDrawable)
	def recalcSize(self):
		pass

	@staticmethod
	def releaseFocus():
		defocused = Block.FOCUSED_BLOCK
		Block.FOCUSED_BLOCK = NullBlock(Screen.getInstance())
		defocused.recalcSurfaceBacursively()
		if isinstance(defocused, Block): defocused.getSurface()
	
	def acquireFocus(self):
		defocused = Block.FOCUSED_BLOCK 
		Block.FOCUSED_BLOCK = self
		defocused.recalcSurfaceBacursively()
		if isinstance(defocused, Block): defocused.getSurface()
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
		return self.getChildStatusInput() if Block.DISPLAY_STATUS_BAR else self.getChildTextfield()

	@overrides(AbstractBlock)
	def getChildTextfield(self):
		return self.childTextfield

	def calcTextfieldSize(self):
		return (self.getWidth() - self.getTextfieldRightIndent() - Constants.BLOCK_FRAME_WIDTH, 
			self.getHeight() - self.getTextfieldTopIndent() - Constants.BLOCK_FRAME_WIDTH)

	def getTextfieldTopIndent(self):
		# TODO: if show statusbar
		return Constants.BLOCK_FRAME_WIDTH + (Block.STATUS_BAR_HEIGHT if Block.DISPLAY_STATUS_BAR else 0)

	def getTextfieldRightIndent(self):
		# TODO: if scrollbar + scrollbar
		return Constants.BLOCK_FRAME_WIDTH

	def getObjectState(self):
		return {'rate': self.rate, 'pos': self.pos(), 'size': self.size(), 
				'statusString': self.getChildStatusInput().getParagraphTextList(), 
				'paragraphTextList': self.getChildTextfield().getParagraphTextList()}

	def setObjectState(self, fileData):
		self.pos(fileData['pos'])
		self.size(fileData['size'])
		self.rate = fileData['rate']
		for parText in (fileData['paragraphTextList'] if 'paragraphTextList' in fileData else []):
			self.getChildTextfield().insertIntoText(parText + '\n')
		for parText in (fileData['statusString'] if 'statusString' in fileData else []):
			self.getChildStatusInput().insertIntoText(parText + '\n')
			
		self.getChildTextfield().setPointerPar(0)
		self.getChildTextfield().getCurPar().setPointerPos(0)
