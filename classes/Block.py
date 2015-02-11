#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from AbstractBlock import AbstractBlock
from classes.Fp import overrides, vectorSum, vectorDiff, isPointInRect,\
	distanceBetween
from classes.NullBlock import NullBlock
import classes
from classes.Textfield import Textfield
from classes.Constants import Constants

class Block(AbstractBlock):
	FOCUSED_BLOCK = NullBlock() # AbstractBlock

	rate = 0
	width = 200
	height = 200
	left = 50
	top = 50

	def __init__(self, blockData=None):
		self.childTextfield = Textfield(self)
		if blockData != None:
			self.setDataFromFile(blockData)
	
	def __str__(self):
		return 'Block: ' + str(self.getChildTextfield())

	def __repr__(self):
		return self.__str__() + '\n'

	def drawOn(self, screen):
		frameColor = [0,255,0] if self == Block.FOCUSED_BLOCK else [127,127,127]
		frameSurface = pygame.Surface([self.width + Constants.BLOCK_FRAME_WIDTH*2, self.height + Constants.BLOCK_FRAME_WIDTH*2])
		frameSurface.fill(frameColor)
		
		contentSurface = self.getChildTextfield().getTextfieldBitmap()

		# TODO: рисовать по-нормальному, чтоб не закрывало текст
		if (self.isResizeCornerPointed(classes.EventHandler.EventHandler.CUR_MOUSE_POS) and self.isPointed(classes.EventHandler.EventHandler.CUR_MOUSE_POS)): 
			pygame.draw.circle(contentSurface, [0,0,255], [self.width, self.height], Constants.RESIZE_CORNER_RADIUS, 0)
		else:
			pygame.draw.circle(contentSurface, [255,255,255], [self.width, self.height], Constants.RESIZE_CORNER_RADIUS, 0)
		
		frameSurface.blit(contentSurface, [Constants.BLOCK_FRAME_WIDTH, Constants.BLOCK_FRAME_WIDTH, self.getWidth(), self.getHeight()]) # self.width, self.height))
		screen.blit(
				frameSurface, 
				(self.left - Constants.BLOCK_FRAME_WIDTH, 
				self.top - Constants.BLOCK_FRAME_WIDTH, 
				self.width + Constants.BLOCK_FRAME_WIDTH, 
				self.height + Constants.BLOCK_FRAME_WIDTH))

	@staticmethod
	def releaseFocus():
		Block.FOCUSED_BLOCK = NullBlock()

	def isPointed(self, pointerPos):
		return isPointInRect(pointerPos, (self.left, self.top, self.width, self.height))
	
	def acquireFocus(self):
		Block.FOCUSED_BLOCK = self

	# abstract block methods
	
	@overrides(AbstractBlock)
	def isResizeCornerPointed(self, mousePos):
		cornerPos = vectorSum(self.pos(), [self.width, self.height])
		return distanceBetween(mousePos, cornerPos) <= Constants.RESIZE_CORNER_RADIUS

	# getters/setters

	@overrides(AbstractBlock)
	def getChildTextfield(self):
		return self.childTextfield

	def size(self, value = None):
		if value != None:
			self.width = max(value[0], Constants.CHAR_WIDTH)
			self.height = max(value[1], Constants.CHAR_HEIGHT)
			self.getChildTextfield().recalcSize()
		return self.width, self.height
			
	def pos(self, value = None):
		if value:
			self.left = value[0]
			self.top = value[1]
		return self.left, self.top

	@overrides(AbstractBlock)
	def sizeAddVector(self, vector):
		self.size( vectorSum(self.size(), vector) )

	@overrides(AbstractBlock)
	def posAddVector(self, vector):
		self.pos( vectorSum(self.pos(), vector) )

	def getDataForFileSave(self):
		paragraphTextList = map(lambda par: par.getText(), self.getChildTextfield().getParagraphList())
		return {'pos': self.pos(), 'size': self.size(), 'rate': self.rate, 'paragraphTextList': paragraphTextList}

	def setDataFromFile(self, fileData):
		self.pos(fileData['pos'])
		self.size(fileData['size'])
		self.rate = fileData['rate']
		for parText in fileData['paragraphTextList']:
			self.getChildTextfield().insertIntoText(parText + '\n')
			
		self.getChildTextfield().setPointerPar(0)
		self.getChildTextfield().setPointerPos(0)
	
	def getWidth(self):
		return self.size()[0]

	def getHeight(self):
		return self.size()[1]