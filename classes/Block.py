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

class Block(AbstractBlock):
	STATUS_BAR_HEIGHT = Constants.CHAR_HEIGHT
	FOCUSED_BLOCK = NullBlock() # AbstractBlock

	rate = 0

	def __init__(self, blockData=None):
		super(Block, self).__init__()
		self.size([200,200])
		self.pos([50,50])
		
		self.childTextfield = Textfield(self)
		self.childList.append(self.childTextfield)
		if blockData != None:
			self.setDataFromFile(blockData)
	
	def __str__(self):
		return 'Block: ' + str(self.getChildTextfield())

	def __repr__(self):
		return self.__str__() + '\n'

	@overrides(AbstractDrawable)
	def drawOn(self, screen):
		# TODO: сделать, чтоб рама была внутри блока
		screen.blit(
				self.getBitmap(), 
				(self.left - Constants.BLOCK_FRAME_WIDTH, 
				self.top - Constants.BLOCK_FRAME_WIDTH, 
				self.width + Constants.BLOCK_FRAME_WIDTH, 
				self.height + Constants.BLOCK_FRAME_WIDTH))

	@overrides(AbstractDrawable)
	def getBitmap(self):
		frameColor = [0,255,0] if self == Block.FOCUSED_BLOCK else [127,127,127]
		frameSurface = pygame.Surface([self.width + Constants.BLOCK_FRAME_WIDTH*2, self.height + Constants.BLOCK_FRAME_WIDTH*2])
		frameSurface.fill(frameColor)
		
		contentSurface = self.getChildTextfield().getTextfieldBitmap()

		# TODO: рисовать по-нормальному, чтоб не закрывало текст
		if (self.isResizeCornerPointed(classes.EventHandler.EventHandler.CUR_MOUSE_POS) and self.isPointed(classes.EventHandler.EventHandler.CUR_MOUSE_POS)): 
			pygame.draw.circle(contentSurface, [0,0,255], [self.width, self.height - self.getTextfieldTopIndent()], Constants.RESIZE_CORNER_RADIUS, 0)
		else:
			pygame.draw.circle(contentSurface, [255,255,255], [self.width, self.height - self.getTextfieldTopIndent()], Constants.RESIZE_CORNER_RADIUS, 0)
		
		frameSurface.blit(contentSurface, [
				Constants.BLOCK_FRAME_WIDTH, 
				Constants.BLOCK_FRAME_WIDTH + self.getTextfieldTopIndent(), 
				self.getWidth(), 
				self.getHeight()])
		
		return frameSurface

	@staticmethod
	def releaseFocus():
		Block.FOCUSED_BLOCK = NullBlock()
	
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

	def calcTextfieldSize(self):
		return (self.getWidth(), self.getHeight() - self.getTextfieldTopIndent())

	def getTextfieldTopIndent(self):
		# TODO: if show statusbar
		return self.STATUS_BAR_HEIGHT

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
		self.getChildTextfield().getCurPar().setPointerPos(0)
