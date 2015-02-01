#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from classes.Paragraph import Paragraph
from classes.Constants import Constants
from classes.Fp import overrides
from classes.AbstractTextfield import AbstractTextfield

class Textfield(object):

	pointerPos = 0
	pointerParagraph = 0
	scrollPos = 0

	textFieldBitmapChanged = False
	textfieldBitmap = pygame.Surface([1, 1])
	
	def __init__(self, parentBlock):
		self.parentBlock = parentBlock
		
		self.paragraphList = [Paragraph(self, '')]
		self.scrollPos = 0

	def __str__(self):
		return '\n\t' + 'Textfield: ' + str(self.getParagraphList())

	def movePointer(self, n):
		pointerPos = self.pointerPos + n
		while pointerPos / self.getCurPar().getTextLen() > 0 and self.pointerParagraph != len(self.paragraphList) - 1:
			pointerPos -= self.getCurPar().getTextLen()
			self.setPointerPar(self.pointerParagraph + 1)
		while pointerPos < 0 and self.pointerParagraph > 0:
			self.setPointerPar(self.pointerParagraph - 1)
			pointerPos += self.getCurPar().getTextLen()
		self.setPointerPos(pointerPos)
		self.textFieldBitmapChanged = True

	def movePar(self, n):
		self.setPointerPar(self.pointerParagraph + n)
		self.setPointerPos(self.pointerPos)
		self.textFieldBitmapChanged = True

	# may have memory leaks
	@overrides(AbstractTextfield)
	def insertIntoText(self, substr): # TODO: most certainly consists of bugs
		substrLen = len(substr)
		newParTextList = substr.split("\n")
		newParTextList[0] = self.getCurPar().getText()[:self.pointerPos] + newParTextList[0]
		newParTextList[-1] += self.getCurPar().getText()[self.pointerPos:]

		parPos = self.pointerParagraph
		self.paragraphList[parPos] = Paragraph(self, newParTextList.pop(0))
		for parText in newParTextList:
			parPos += 1
			self.paragraphList.insert(parPos, Paragraph(self, parText))
		self.movePointer(substrLen)
		self.textFieldBitmapChanged = True

	def deleteFromText(self, n):
		if n < 0:
			appendToFirst = self.getCurPar().getText()[self.pointerPos:]
			self.getCurPar().crop(0, self.pointerPos)
			firstPar = self.pointerParagraph
			self.movePointer(n)
			while self.paragraphList[firstPar].getTextLen() + n <= 0 and firstPar > 0:
				n += self.paragraphList[firstPar].getTextLen()
				self.paragraphList.pop(firstPar)
				firstPar -= 1
			self.paragraphList[firstPar].crop(0, n - 1).append(appendToFirst)
		elif n > 0:
			prependToLast = self.getCurPar().getText()[:self.pointerPos]
			self.getCurPar().crop(self.pointerPos, -1)
			while self.getCurPar().getTextLen() - n <= 0 and self.pointerParagraph != len(self.paragraphList) - 1:
				n -= self.getCurPar().getTextLen()
				self.paragraphList.pop(self.pointerParagraph)
			self.getCurPar().crop(n, -1).prepend(prependToLast)
		self.textFieldBitmapChanged = True

	def scroll(self, n):
		self.scrollPos += n
		if self.scrollPos < 0: self.scrollPos = 0
		if self.scrollPos >= self.getFullRowCount(): self.scrollPos = self.getFullRowCount() - 1
		self.textFieldBitmapChanged = True

	def recalcSize(self):
		# self.width = self.getParentBlock().width - epsilon
		self.textFieldBitmapChanged = True

	def getFullRowCount(self): # TODO: may be wrong
		return len(self.getFullRowList())

	def getFullRowList(self):
		rowList = []
		for par in self.getParagraphList():
			rowList += par.getRowList()
		return rowList

	def getPointerRowAndCol(self):
		resultRow = 0
		skippedParList = self.getParagraphList()[:self.pointerParagraph]
		for par in skippedParList:
			resultRow += len(par.getRowList())
		
		pointerRow = self.pointerPos / self.getCharInRowCount()
		pointerShift = self.pointerPos % self.getCharInRowCount()
		
		return [resultRow + pointerRow, pointerShift]

	def getPrintedRowCount(self):
		return self.getHeight() / Constants.CHAR_HEIGHT

	def getCharInRowCount(self):
		return self.getWidth() / Constants.CHAR_WIDTH
	
	def size(self, value=None):
		return self.getParentBlock().size(value)
	
	def getWidth(self):
		# ?
		return self.getParentBlock().getWidth() # minus epsilon
	
	def getHeight(self):
		# ?
		return self.getParentBlock().getHeight() # minus epsilon

	def getTextfieldBitmap(self):
		contentSurface = pygame.Surface(self.size())
		contentSurface.fill([255,255,255])
		
		rowListToPrint = self.getFullRowList()[self.scrollPos : self.scrollPos + self.getPrintedRowCount()]

		i = 0
		for row in rowListToPrint:
			label = Constants.PROJECT_FONT.render(row, 1, [0,0,0])
			contentSurface.blit(label, [0, i * Constants.CHAR_HEIGHT])
			i += 1

		pointerRow, pointerCol = self.getPointerRowAndCol()
		if (pointerRow >= self.scrollPos and pointerRow < self.scrollPos + self.getPrintedRowCount()):
			printedRow = pointerRow - self.scrollPos
			pygame.draw.line(contentSurface, [255,0,0], 
							[pointerCol * Constants.CHAR_WIDTH, (printedRow) * Constants.CHAR_HEIGHT], 
							[pointerCol * Constants.CHAR_WIDTH, (printedRow + 1) * Constants.CHAR_HEIGHT])
		
		return contentSurface

	def getParagraphList(self):
		return self.paragraphList
	
	def getCurPar(self):
		':rtype Paragraph'
		return self.paragraphList[self.pointerParagraph]
	
	def setPointerPos(self, pointerPos):
		if pointerPos < 0: pointerPos = 0
		if pointerPos > len(self.getCurPar().getText()): pointerPos = len(self.getCurPar().getText())
		self.pointerPos = pointerPos
		
	def setPointerPar(self, pointerPar):
		if pointerPar < 0: pointerPar = 0
		if pointerPar >= len(self.paragraphList): pointerPar = len(self.paragraphList) - 1
		self.pointerParagraph = pointerPar
		
	def getParentBlock(self):
		':rtype Block'
		return self.parentBlock
	
	def setParentBlock(self, value):
		self.parentBlock = value
	