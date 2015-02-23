#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from classes.Fp import split, overrides
from classes.Constants import Constants
import re
from classes.Drawable.AbstractDrawable import AbstractDrawable
import classes as huj

class Paragraph(AbstractDrawable):

	@overrides(AbstractDrawable)
	def getEventHandler(self):
		return huj.Drawable.Screen.Block.Textfield.Paragraph.FocusedParagraphEventHandler.FocusedParagraphEventHandler(self)

	@overrides(AbstractDrawable)
	def getFocusedChild(self) -> AbstractDrawable:
		return None

	text = ''

	pointerPos = 0

	def __init__(self, parentTextfield, text):
		super(Paragraph, self).__init__(parentTextfield)

		self.setText(text)
		self.pointerPos = 0
		self.rowList = []
		
		self.recalcSize()

	def __str__(self):
		return 'Paragraph: |' + self.getText() + '|'

	def __repr__(self):
		return '\n\t\t' + self.__str__()

	def getParentTextfield(self):
		return self.getParent()
		
	def setParentTextfield(self, value):
		self.setParent(value)

	# operations with pointer

	def getPointerPos(self):
		return self.pointerPos

	def setPointerPos(self, pointerPos):
		if pointerPos < 0: pointerPos = 0
		if pointerPos > len(self.getText()): pointerPos = len(self.getText())
		self.pointerPos = pointerPos

	def cropToPointer(self):
		return self.crop(0, self.getPointerPos())

	def cropFromPointer(self):
		return self.crop(self.getPointerPos(), -1)
	
	def getTextAfterPointer(self):
		return self.text[self.getPointerPos():]

	def getTextBeforePointer(self):
		return self.text[:self.getPointerPos()]

	def cutReplaceAfterPointer(self, postStr):
		cut = self.getTextAfterPointer()
		self.cropToPointer()
		self.append(postStr)

		return cut

	# operations with text

	def crop(self, l, r = -1):
		r = self.getTextLen() + r if r < 0 else r
		self.setText(self.getText()[l:r])
		return self

	def append(self, strToAppend):
		self.setText(self.getText() + strToAppend)
		return self

	def prepend(self, strToPrepend):
		self.setText(strToPrepend + self.getText())
		return self

	def getShiftToSpace(self, n):
		shift = 0
		if n > 0:
			shift = ([m.start() for m in re.finditer('[^(а-яА-Яa-zA-ZёЁ)]', self.getTextAfterPointer()[1:]) ] + [-1])[0] + 1
		if n < 0:
			shift = ([-1] + ([m.start() for m in re.finditer('[^(а-яА-Яa-zA-ZёЁ)]', self.getTextBeforePointer()[:-1]) ]))[-1] - len(self.getTextBeforePointer()) + 1

		return shift if shift else n

	def getTextLen(self):
		return len(self.getText()) + 1 # + 1 for eol

	def getText(self):
		return self.text

	def setText(self, value):
		self.text = value
		self.recalcSurfaceBacursively()
		
	# bitmap operations

	def getPointerRowIdx(self):
		return self.getPointerPos() // self.getCharInRowCount()

	def getCharInRowCount(self):
		return self.getWidth() // Constants.CHAR_WIDTH

	def calcRowList(self):
		rowList = []
		charInRowCount = self.getCharInRowCount()
		textLeft = self.getText()
		while len(textLeft) > 0:
			row,textLeft = split(textLeft, charInRowCount)
			rowList.append(row)

		return rowList if len(rowList) > 0 else ['']

	@overrides(AbstractDrawable)
	def recalcSize(self):
		self.setWidth(self.getParentTextfield().size()[0])

	@overrides(AbstractDrawable)
	def getSurface(self, rowIdx=0):
		# TODO: make it like in all other drawables, so i could move this method implementation into abstract class
		self.recalcSurface()
		surface = pygame.Surface([
				self.surface.get_width(), 
				self.surface.get_height() - rowIdx * Constants.CHAR_HEIGHT])
		surface.fill([255,255,255])
		surface.blit(self.surface, [0, -rowIdx * Constants.CHAR_HEIGHT])
		pygame.draw.line(surface, [255,230,230], [0, 0], [surface.get_width(), 0])
		return surface

	def genBitmap(self):
		surface = pygame.Surface([
				self.getWidth(),
				len(self.getRowList()) * Constants.CHAR_HEIGHT])
		surface.fill(self.getParentTextfield().getTextBgColor())
		i = 0
		for row in self.getRowList():
			label = Constants.PROJECT_FONT.render(row, 1,
					self.getParentTextfield().getTextColor(),
					self.getParentTextfield().getTextBgColor())
			surface.blit(label, [0, i * Constants.CHAR_HEIGHT])
			i += 1
		
		return surface

	@overrides(AbstractDrawable)
	def recalcSurface(self):
		self.getRowList()

	def getRowList(self):
		if self.surfaceChanged:
			self.rowList = self.calcRowList()
			self.surfaceChanged = False
			self.surface = self.genBitmap()
		
		return self.rowList
