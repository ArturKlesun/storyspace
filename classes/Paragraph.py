#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from classes.Fp import split
from classes.Constants import Constants
import re

class Paragraph(object):

	text = u''

	rowListChanged = True
	pointerPos = 0

	def __init__(self, parentTextfield, text):
		self.parentTextfield = parentTextfield
		self.setText(text)
		self.pointerPos = 0
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

	def cropToPointer(self):
		return self.crop(0, self.getPointerPos())

	def cropFromPointer(self):
		return self.crop(self.getPointerPos(), -1)

	def append(self, strToAppend):
		self.setText(self.getText() + strToAppend)
		self.rowListChanged = True

		return self

	def prepend(self, strToPrepend):
		self.setText(strToPrepend + self.getText())
		self.rowListChanged = True

		return self

	def getShiftToSpace(self, n):
		shift = 0
		if n > 0:
			shift = ([m.start() for m in re.finditer(u'[^(а-яА-Яa-zA-Z)]', self.getTextAfterPointer()[1:]) ] + [-1])[0] + 1
		if n < 0:
			shift = ([-1] + ([m.start() for m in re.finditer(u'[^(а-яА-Яa-zA-Z)]', self.getTextBeforePointer()[:-1]) ]))[-1] - len(self.getTextBeforePointer()) + 1

		return shift

	def recalcBitmap(self):
		self.getRowList()

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
		self.recalcBitmap()
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

	def getPointerRowIdx(self):
		return self.getPointerPos() / self.getParentTextfield().getCharInRowCount()

	def getPointerPos(self):
		return self.pointerPos

	def setPointerPos(self, pointerPos):
		if pointerPos < 0: pointerPos = 0
		if pointerPos > len(self.getText()): pointerPos = len(self.getText())
		self.pointerPos = pointerPos

	def getParentTextfield(self):
		return self.parentTextfield
		
	def setParentTextfield(self, value):
		self.parentTextfield = value
	
	def getTextLen(self):
		return len(self.getText()) + 1 # + 1 for eol

	def getText(self):
		return self.text
	
	def getTextAfterPointer(self):
		return self.text[self.getPointerPos():]

	def getTextBeforePointer(self):
		return self.text[:self.getPointerPos()]

	def cutReplaceAfterPointer(self, postStr):
		cut = self.getTextAfterPointer()
		self.cropToPointer()
		self.append(postStr)

		return cut

	def setText(self, value):
		self.text = value
		self.rowListChanged = True
