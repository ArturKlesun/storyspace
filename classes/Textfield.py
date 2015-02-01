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
		print 'Gonna to delete text'
		if n < 0:
			appendToFirst = self.getCurPar().getText()[self.pointerPos:]
			self.getCurPar().setText( self.getCurPar().getText()[:self.pointerPos] )
			endPar = self.pointerParagraph
			self.movePointer(n)
			while self.paragraphList[endPar].getTextLen() + n <= 0 and endPar > 0:
				# TODO: doesn't work
				n += self.paragraphList[endPar].getTextLen()
				self.paragraphList.pop(endPar)
				endPar -= 1
			self.paragraphList[endPar].setText( self.paragraphList[endPar].getText()[self.getCurPar().getTextLen() - 1 + n] + appendToFirst ) # TODO: definitely mistake
		elif n > 0:
			print('was: ' + self.getCurPar().getText());
			prependToLast = self.getCurPar().getText()[:self.pointerPos]
			print('prependToLast: ' + prependToLast);
			self.getCurPar().crop(self.pointerPos, -1)
			print('is: ' + self.getCurPar().getText());
			while self.getCurPar().getTextLen() - n <= 0 and self.pointerParagraph != len(self.paragraphList) - 1:
				n -= self.getCurPar().getTextLen()
				self.paragraphList.pop(self.pointerParagraph)
			print('is: ' + self.getCurPar().getText());
			self.getCurPar().crop(n, -1);
			print('is: ' + self.getCurPar().getText());
			self.getCurPar().prepend(prependToLast)
			print('became: ' + self.getCurPar().getText());
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
		
		# deadlock if contains some text
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

	# please, don't use me!
# 	def getTextfieldBitmap(self):
# 		
# 		if self.textFieldBitmapChanged:
# 			# ���� ��� ������ - ������� ��� �� �����
# 			charInRowCount = self.width / Constants.CHAR_WIDTH
# 			rowCount = self.height / Constants.CHAR_HEIGHT
# 	
# 			row = 0
# 			par = 0
# 	
# 			contentSurface = pygame.Surface([self.width, self.height])
# 			contentSurface.fill([255,255,255])
# 	
# 			pointerRow = self.pointerPos / charInRowCount
# 			pointerCol = self.pointerPos % charInRowCount
# 	
# 			scrollLeft = self.scrollPos
# 	
# 			while row < rowCount and par < len(self.paragraphList):
# 				if (par == self.pointerParagraph): # ��� ����� ��������?
# 					pointerRow += row
# 				#textLeft = self.paragraphList[par]
# 				parRowList = self.paragraphList[par].gerRowList()
# 				atLeastOne = True
# 				while (len(textLeft) or atLeastOne) and row < rowCount:
# 					atLeastOne = False # �������� ����
# 					if (scrollLeft > 0):
# 						# ���� ��� ������. � �� ������ ����������� ���� �����
# 						textLeft = textLeft[charInRowCount:]
# 						scrollLeft -= 1
# 						if (par == self.pointerParagraph): # �������� ����!
# 							pointerRow -= 1
# 							#pointerScrolling = scrollLeft
# 					else:
# 						label = Constants.PROJECT_FONT.render(textLeft[:charInRowCount], 1, [0,0,0])
# 						textLeft = textLeft[charInRowCount:]
# 						contentSurface.blit(label, [0, row*Constants.CHAR_HEIGHT])
# 						row += 1
# 				par += 1
# 	
# 			pygame.draw.line(contentSurface, [255,0,0], 
# 							[pointerCol * Constants.CHAR_WIDTH, (pointerRow) * Constants.CHAR_HEIGHT], 
# 							[pointerCol * Constants.CHAR_WIDTH, (pointerRow + 1) * Constants.CHAR_HEIGHT])
# 			
# 			self.textfieldBitmap = contentSurface
# 			self.textFieldBitmapChanged = False
# 		
# 		return self.textfieldBitmap

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
	