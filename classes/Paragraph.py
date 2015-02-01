#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from classes.Fp import split
from classes.Constants import Constants

class Paragraph(object):

	text = u''

	rowListChanged = True

	def __init__(self, parentTextfield, text):
		self.parentTextfield = parentTextfield
		self.setText(text)
		self.rowList = []
		self.bitmap = pygame.Surface([1, 1])
		self.rowListChanged = True

	def __str__(self):
		return 'Paragraph: |' + self.getText() + '|'

	def __repr__(self):
		return '\n\t\t' + self.__str__()

	def crop(self, l, r = -1):
		r = self.getTextLen() + r if r < 0 else r
		self.setText(self.getText()[l:r])
		self.rowListChanged = True

		return self

	def append(self, strToAppend):
		self.setText(self.getText() + strToAppend)
		self.rowListChanged = True

		return self

	def prepend(self, strToPrepend):
		self.setText(strToPrepend + self.getText())
		self.rowListChanged = True

		return self

	def getRowList(self):
		if self.rowListChanged:
			self.rowList = self.calcRowList()
			self.rowListChanged = False
			self.bitmap = self.genBitmap()
		
		return self.rowList

	def calcRowList(self):
		rowList = []
		charInRowCount = self.getParentTextfield().getCharInRowCount()
		textLeft = self.getText()
		while len(textLeft) > 0:
			row, textLeft = split(textLeft, charInRowCount)
			rowList.append(row)

		return rowList if len(rowList) > 0 else ['']

	def getBitmap(self, rowIdx=0):
		print('huj ' + str(self.bitmap.get_height()) + str(rowIdx))
		self.getRowList()
		bitmap = pygame.Surface([
				self.bitmap.get_width(), 
				self.bitmap.get_height() - rowIdx * Constants.CHAR_HEIGHT])
		bitmap.fill([255,255,255])
		bitmap.blit(self.bitmap, [0, -rowIdx * Constants.CHAR_HEIGHT])
		return bitmap

	def genBitmap(self):
		surface = pygame.Surface([
				self.getParentTextfield().getCharInRowCount() * Constants.CHAR_WIDTH,
				len(self.getRowList()) * Constants.CHAR_HEIGHT])
		surface.fill([255,255,255])
		i = 0
		for row in self.getRowList():
			label = Constants.PROJECT_FONT.render(row, 1, [0,0,0], [255,255,255])
			surface.blit(label, [0, i * Constants.CHAR_HEIGHT])
			i += 1
		
		return surface

	def getParentTextfield(self):
		return self.parentTextfield
		
	def setParentTextfield(self, value):
		self.parentTextfield = value
	
	def getTextLen(self):
		return len(self.getText()) + 1 # + 1 for eol

	def getText(self):
		return self.text

	def setText(self, value):
		self.text = value
		self.rowListChanged = True
