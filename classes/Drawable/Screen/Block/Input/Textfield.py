#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from pygame.surface import Surface
from classes.Drawable.Screen.Block.Input.TextfieldHandler import TextfieldHandler

from classes.Drawable.Screen.Block.Input.Paragraph.Paragraph import Paragraph
from classes.Constants import Constants
from classes.Fp import overrides
from classes.Drawable.AbstractDrawable import AbstractDrawable


class Textfield(AbstractDrawable):

	textfieldBitmap = pygame.Surface([1, 1])

	textColor = [255,255,255]
	textBgColor = [255,255,255]
	
	def __init__(self, parentBlock):
		self.scrollPos = 0

		super(Textfield, self).__init__(parentBlock)

		self.paragraphList = []
		self.scrollPos = 0

		self.setTextColor([0,0,0])
		self.setTextBgColor([255,255,255])

	def __str__(self):
		return '\n\t' + 'Textfield: ' + str(self.getParagraphList())

	# abstract method implementation

	@overrides(AbstractDrawable)
	def size(self, value = None):
		return self.getParentBlock().calcTextfieldSize()

	@overrides(AbstractDrawable)
	def getChildList(self):
		return self.getParagraphList()

	@overrides(AbstractDrawable)
	def makeHandler(self): return TextfieldHandler(self)

	@overrides(AbstractDrawable)
	def getDefaultSize(self):
		return [Constants.CHAR_WIDTH, Constants.CHAR_HEIGHT]

	def getObjectState(self):
		return {'paragraphDataList': [par.getObjectState() for par in self.getParagraphList()]}

	@overrides(AbstractDrawable)
	def setObjectState(self, paragraphDataList):
		if self.getRootParent().jsonStructureFormatVersion == Constants.PARAGRAPH_NOT_OBJECT_FORMAT_VERSION: # legacy
			for parText in paragraphDataList:
				self.insertIntoText(parText + '\n')
			self.deleteFromText(-1) # -_-
		else:
			for paragraphData in paragraphDataList['paragraphDataList'][::-1]:
				Paragraph(self).setObjectState(paragraphData)
		self.setPointerPar(0)
		self.getCurPar().setPointerPos(0)
		self.moveScrollToPointer()

	@overrides(AbstractDrawable)
	def recalcSize(self):
		self.surface = Surface(self.size())

	# operations with text

	def getParagraphList(self):
		return self.paragraphList
	
	def getCurPar(self):
		':rtype: Paragraph'
		return self.getFocusedChild()

	# operations with pointer

	def movePar(self, n):
		self.setPointerPar(self.getFocusedIndex() + n)

	def getPointerRowAndCol(self):
		resultRow = 0
		skippedParList = self.getParagraphList()[:self.getFocusedIndex()]
		for par in skippedParList:
			resultRow += len(par.getRowList())
		
		pointerRow = self.getCurPar().getPointerRowIdx()
		pointerShift = self.getCurPar().getPointerPos() % self.getCharInRowCount()
		
		return [resultRow + pointerRow, pointerShift]
		
	def setPointerPar(self, pointerPar: int):
		self.setFocusedIndex(pointerPar)

	def moveScrollToPointer(self):
		pointerRow = self.getPointerRowAndCol()[0]
		if pointerRow < self.scrollPos:
			self.setScrollPos(pointerRow)
		elif pointerRow >= self.scrollPos  + self.getPrintedRowCount():
			self.setScrollPos(pointerRow - self.getPrintedRowCount() + 1)

	# operations with bitmap

	def getParIdxAndRowIdxToPrintFrom(self):
		scrollPos = self.scrollPos
		parIdx = 0
		rowIdx = 0
		while scrollPos > 0 and parIdx < len(self.getParagraphList()):
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
		# not resized correctly lol
		self.surface.fill([255,255,255])
		parIdx, rowIdx = self.getParIdxAndRowIdxToPrintFrom()
		
		y = - rowIdx * Constants.CHAR_HEIGHT
		while y < self.getHeight() and parIdx < len(self.getParagraphList()):
			bitmapHeight = len(self.paragraphList[parIdx].getRowList()) * Constants.CHAR_HEIGHT
			self.paragraphList[parIdx].setTop(y)
			self.paragraphList[parIdx].drawOnParent()
			y += bitmapHeight
			parIdx += 1

	# field getters/setters

	def getParentBlock(self):
		""":rtype: classes.Drawable.Screen.Block.TextBlock"""
		return self.getParent()

	def setTextColor(self, value):
		self.textColor = value

	def getTextColor(self):
		return self.textColor

	def setTextBgColor(self, value):
		self.textBgColor = value

	def getTextBgColor(self):
		return self.textBgColor

	def setScrollPos(self, value):
		self.scrollPos = value
		if self.scrollPos < 0: self.scrollPos = 0
		if self.scrollPos >= self.getFullRowCount(): self.scrollPos = self.getFullRowCount() - 1
		self.recalcSurfaceBacursively()

	# event handles

	SCROLL_STEP = 4

	def scrollUp(self): self.setScrollPos(self.scrollPos - Textfield.SCROLL_STEP)
	def scrollDown(self): self.setScrollPos(self.scrollPos + Textfield.SCROLL_STEP)

	def mergeBack(self):
		if self.getFocusedIndex() > 0:
			textToAppend = self.getCurPar().getText()
			self.setFocusedIndex(self.getFocusedIndex() - 1).getParagraphList().remove(self.getFocusedIndex() + 1)
			self.getCurPar().append(textToAppend)
			return True
		else: return False
	def mergeNext(self):
		if self.getFocusedIndex() < self.getParagraphList() - 1:
			textToPrepend = self.getCurPar().getText()
			self.getParagraphList().remove(self.getFocusedIndex())
			self.getCurPar().prepend(textToPrepend)
			return True
		else: return False

	def rowUp(self):
		pointerShift = self.getPointerRowAndCol()[1]
		self.focusBack()
		self.getCurPar().setPointerPos( (len(self.getCurPar().getRowList()) - 1) * self.getCharInRowCount() + pointerShift )
	def rowDown(self):
		pointerShift = self.getPointerRowAndCol()[1]
		self.movePar(1)
		self.getCurPar().setPointerPos(pointerShift)


