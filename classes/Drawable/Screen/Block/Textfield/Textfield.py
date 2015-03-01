#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from classes.Drawable.Screen.Block.Textfield.AbstractInput import AbstractInput

from classes.Drawable.Screen.Block.Textfield.Paragraph.Paragraph import Paragraph
from classes.Constants import Constants
from classes.Fp import overrides
from classes.Drawable.AbstractDrawable import AbstractDrawable
import classes as huj


class Textfield(AbstractInput):

	pointerParagraph = 0
	scrollPos = 0

	textfieldBitmap = pygame.Surface([1, 1])

	textColor = [255,255,255]
	textBgColor = [255,255,255]
	
	def __init__(self, parentBlock):
		super(Textfield, self).__init__(parentBlock)

		self.recalcSize()
		
		self.paragraphList = [Paragraph(self, '')]
		self.scrollPos = 0

		self.setTextColor([0,0,0])
		self.setTextBgColor([255,255,255])

	def __str__(self):
		return '\n\t' + 'Textfield: ' + str(self.getParagraphList())

	# abstract method implementation

	@overrides(AbstractInput)
	def insertIntoText(self, substr):
		substrLen = len(substr)
		newParTextList = substr.split("\n")
		appendToLast = self.getCurPar().cutReplaceAfterPointer(newParTextList.pop(0))
		if len(newParTextList):
			newParTextList[-1] += appendToLast
			parPos = self.pointerParagraph
			for parText in newParTextList:
				parPos += 1
				self.paragraphList.insert(parPos, Paragraph(self, parText))
		else:
			self.getCurPar().append(appendToLast)

		self.movePointer(substrLen)

	@overrides(AbstractInput)
	def movePointer(self, n):
		pointerPos = self.getCurPar().getPointerPos() + n
		while pointerPos // self.getCurPar().getTextLen() > 0 and self.pointerParagraph != len(self.paragraphList) - 1:
			pointerPos -= self.getCurPar().getTextLen()
			self.setPointerPar(self.pointerParagraph + 1)
		while pointerPos < 0 < self.pointerParagraph:
			self.setPointerPar(self.pointerParagraph - 1)
			pointerPos += self.getCurPar().getTextLen()

		self.getCurPar().setPointerPos(pointerPos)
		self.moveScrollToPointer()

	@overrides(AbstractDrawable)
	def recalcSize(self):
		self.size(self.getParentBlock().calcTextfieldSize())

	@overrides(AbstractDrawable)
	def getFocusedChild(self) -> Paragraph:
		return self.getCurPar()

	@overrides(AbstractDrawable)
	def getEventHandler(self):
		return huj.Drawable.Screen.Block.Textfield.FocusedInputEventHandler.FocusedInputEventHandler(self)

	@overrides(AbstractDrawable)
	def getDefaultSize(self):
		return [Constants.CHAR_WIDTH, Constants.CHAR_HEIGHT]

	# operations with text

	def deleteFromText(self, n):
		if n < 0:
			appendToFirst = self.getCurPar().getTextAfterPointer()
			self.getCurPar().cropToPointer()
			firstPar = self.pointerParagraph
			self.movePointer(n)
			while self.paragraphList[firstPar].getTextLen() + n <= 0 and firstPar > 0:
				n += self.paragraphList[firstPar].getTextLen()
				self.paragraphList.pop(firstPar)
				firstPar -= 1
			self.paragraphList[firstPar].crop(0, n - 1).append(appendToFirst)
		elif n > 0:
			prependToLast = self.getCurPar().getTextBeforePointer()
			self.getCurPar().cropFromPointer()
			while self.getCurPar().getTextLen() - n <= 0 and self.pointerParagraph != len(self.paragraphList) - 1:
				n -= self.getCurPar().getTextLen()
				self.paragraphList.pop(self.pointerParagraph)
			self.getCurPar().crop(n, -1).prepend(prependToLast)


	def getParagraphList(self):
		return self.paragraphList

	def getParagraphTextList(self):
		return [par.getText() for par in self.getParagraphList()]
	
	def getCurPar(self):
		':rtype Paragraph'
		return self.paragraphList[self.pointerParagraph]

	# operations with pointer

	def ctrlMovePointer(self, n):
		self.movePointer(self.getCurPar().getShiftToSpace(n))
	def ctrlDeleteFromText(self, n):
		self.deleteFromText(self.getCurPar().getShiftToSpace(n))
	
	def movePointerInRows(self, rowCount):
		# maybe not the bestt approach to deal with deeds, but works
		for i in range(0, rowCount):
			if len(self.getCurPar().getTextAfterPointer()) > self.getCharInRowCount():
				self.movePointer(self.getCharInRowCount())
			elif self.getCurPar().getPointerRowIdx() < len(self.getCurPar().getRowList()) - 1:
				self.getCurPar().setPointerPos(self.getCurPar().getTextLen() - 1)
			else:
				pointerShift = self.getPointerRowAndCol()[1]
				self.movePar(1)
				self.getCurPar().setPointerPos(pointerShift)
		for i in range(rowCount, 0):
			if len(self.getCurPar().getTextBeforePointer()) >= self.getCharInRowCount():
				self.movePointer(-self.getCharInRowCount())
			else:
				pointerShift = self.getPointerRowAndCol()[1]
				self.movePar(-1)				
				self.getCurPar().setPointerPos( (len(self.getCurPar().getRowList()) - 1) * self.getCharInRowCount() + pointerShift )
		self.moveScrollToPointer()
		self.recalcSurfaceBacursively()


	def movePar(self, n):
		self.setPointerPar(self.pointerParagraph + n)

	def getPointerRowAndCol(self):
		resultRow = 0
		skippedParList = self.getParagraphList()[:self.pointerParagraph]
		for par in skippedParList:
			resultRow += len(par.getRowList())
		
		pointerRow = self.getCurPar().getPointerRowIdx()
		pointerShift = self.getCurPar().getPointerPos() % self.getCharInRowCount()
		
		return [resultRow + pointerRow, pointerShift]
		
	def setPointerPar(self, pointerPar):
		if pointerPar < 0: pointerPar = 0
		if pointerPar >= len(self.paragraphList): pointerPar = len(self.paragraphList) - 1
		self.pointerParagraph = pointerPar

	# scroll operations

	def moveScrollToPointer(self):
		pointerRow = self.getPointerRowAndCol()[0]
		if (pointerRow < self.scrollPos):
			self.setScrollPos(pointerRow)
		elif pointerRow >= self.scrollPos  + self.getPrintedRowCount():
			self.setScrollPos(pointerRow - self.getPrintedRowCount() + 1)

	# operations with bitmap

	def setTextColor(self, value):
		self.textColor = value

	def getTextColor(self):
		return self.textColor 

	def setTextBgColor(self, value):
		self.textBgColor = value

	def getTextBgColor(self):
		return self.textBgColor 

	def getParIdxAndRowIdxToPrintFrom(self):
		scrollPos = self.scrollPos
		parIdx = 0
		rowIdx = 0
		while scrollPos > 0:
			scrollPos -= len(self.paragraphList[parIdx].getRowList())
			parIdx += 1
		if scrollPos < 0:
			parIdx -= 1
			rowIdx = len(self.paragraphList[parIdx].getRowList()) + scrollPos
		
		return parIdx, rowIdx;

	def getFullRowCount(self): # TODO: may be wrong
		return len(self.getFullRowList())

	def getFullRowList(self):
		rowList = []
		for par in self.getParagraphList():
			rowList += par.getRowList()
		return rowList

	def getPrintedRowCount(self):
		return self.getHeight() // Constants.CHAR_HEIGHT

	def getCharInRowCount(self):
		return self.getWidth() // Constants.CHAR_WIDTH

	@overrides(AbstractDrawable)
	def recalcSurface(self):
		self.surface.fill([255,255,255])
		parIdx, rowIdx = self.getParIdxAndRowIdxToPrintFrom()
		
		y = - rowIdx * Constants.CHAR_HEIGHT
		while y < self.getHeight() and parIdx < len(self.getParagraphList()):
			bitmapHeight = len(self.paragraphList[parIdx].getRowList()) * Constants.CHAR_HEIGHT
			self.paragraphList[parIdx].setTop(y)
			self.paragraphList[parIdx].drawOnParent()
			y += bitmapHeight
			parIdx += 1

	# model operations

	def getParentBlock(self):
		':rtype huj.Drawable.Screen.Block.TextBlock'
		return self.getParent()
	
	def setParentBlock(self, value):
		self.setParent(value)
	
