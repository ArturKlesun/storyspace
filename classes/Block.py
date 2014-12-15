#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from AbstractBlock import AbstractBlock
from classes.Fp import overrides, vectorSum
from classes.NullBlock import NullBlock

pygame.init()

PROJECT_FONT = pygame.font.Font("UbuntuMono-R.ttf", 10)
CHAR_WIDTH, CHAR_HEIGHT = PROJECT_FONT.size("w")

def isPointInRect(p, r):
	return p[0] > r[0] and p[1] > r[1] and p[0] < r[0] + r[2] and p[1] < r[1] + r[3]

class Block(AbstractBlock):
	FOCUSED_BLOCK = NullBlock(0)

	rate = 0
	width = 200
	height = 200
	left = 50
	top = 50

	pointerPos = 0
	pointerParagraph = 0
	scrollPos = 0

	def __init__(self, blockId = 0):
		self.paragraphList = ['']
		self.scrollPos = 0

	def drawOn(self, screen):
		print 'begin drawing'
		charInRowCount = self.width / CHAR_WIDTH
		rowCount = self.height / CHAR_HEIGHT

		row = 0
		par = 0

		frameColor = [0,255,0] if self == Block.FOCUSED_BLOCK else [127,127,127]
		frameSurface = pygame.Surface([self.width + 4, self.height + 4])
		frameSurface.fill(frameColor)
		
		contentSurface = pygame.Surface([self.width, self.height])
		contentSurface.fill([255,255,255])

		pointerRow = self.pointerPos / charInRowCount
		pointerCol = self.pointerPos % charInRowCount

		scrollLeft = self.scrollPos

		while row < rowCount and par < len(self.paragraphList):
			if (par == self.pointerParagraph and self == Block.FOCUSED_BLOCK):
				pygame.draw.line(contentSurface, [255,0,0], 
						(pointerCol * CHAR_WIDTH, (pointerRow + row) * CHAR_HEIGHT), 
						(pointerCol * CHAR_WIDTH, (pointerRow + row + 1) * CHAR_HEIGHT))
			textLeft = self.paragraphList[par]
			atLeastOne = True
			while (len(textLeft)  or atLeastOne) and row < rowCount:
				if (scrollLeft > 0):
					textLeft = textLeft[charInRowCount:]
					print 'texthuext = ' + textLeft
					scrollLeft -= 1
				else:
					atLeastOne = False # говнокод могёт
					label = PROJECT_FONT.render(textLeft[:charInRowCount], 1, [0,0,0])
					textLeft = textLeft[charInRowCount:]
					contentSurface.blit(label, [0, row*CHAR_HEIGHT])
					row += 1
			par += 1
		
		frameSurface.blit(contentSurface, (2,2,self.width,self.height))
		screen.blit(frameSurface, (self.left-2,self.top-2,self.width + 2,self.height + 2))

	def isPointed(self, pointerPos):
		return isPointInRect(pointerPos, (self.left, self.top, self.width, self.height))

	def acquireFocus(self):
		Block.FOCUSED_BLOCK = self

	# abstract block methods

	@overrides(AbstractBlock)
	def movePointer(self, n):
		pointerPos = self.pointerPos + n
		while pointerPos / (len(self.getCurPar()) + 1) > 0 and self.pointerParagraph != len(self.paragraphList) - 1:
			pointerPos -= len(self.getCurPar()) + 1 # + 1 for eol
			self.setPointerPar(self.pointerParagraph + 1)
		while pointerPos < 0 and self.pointerParagraph > 0:
			self.setPointerPar(self.pointerParagraph - 1)
			pointerPos += len(self.getCurPar()) + 1
		self.setPointerPos(pointerPos)

	@overrides(AbstractBlock)
	def insertIntoText(self, substr):
		substrLen = len(substr)
		newParagraphList = substr.split("\n")
		newParagraphList[0] = self.getCurPar()[:self.pointerPos] + newParagraphList[0]
		newParagraphList[-1] += self.getCurPar()[self.pointerPos:]

		parPos = self.pointerParagraph
		self.paragraphList[parPos] = newParagraphList.pop(0)
		for paragraph in newParagraphList:
			parPos += 1
			self.paragraphList.insert(parPos, paragraph)
		self.movePointer(substrLen)

	@overrides(AbstractBlock)
	def deleteFromText(self, n):
		if n < 0:
			appendToFirst = self.paragraphList[self.pointerParagraph][self.pointerPos:]
			self.paragraphList[self.pointerParagraph] = self.paragraphList[self.pointerParagraph][:self.pointerPos]
			endPar = self.pointerParagraph
			self.movePointer(n)
			while len(self.paragraphList[endPar]) + 1 + n <= 0 and endPar > 0:
				# TODO: doesn't work
				n += len(self.paragraphList[endPar]) + 1
				self.paragraphList.pop(endPar)
				endPar -= 1
			print 'backspace n=' + str(n)
			self.paragraphList[endPar] = self.paragraphList[endPar][:len(self.getCurPar()) + n] + appendToFirst
		elif n > 0:
			prependToLast = self.paragraphList[self.pointerParagraph][:self.pointerPos]
			self.paragraphList[self.pointerParagraph] = self.paragraphList[self.pointerParagraph][self.pointerPos:]
			while len(self.getCurPar()) + 1 - n <= 0 and self.pointerParagraph != len(self.paragraphList) - 1:
				n -= len(self.getCurPar()) + 1
				self.paragraphList.pop(self.pointerParagraph)
			self.paragraphList[self.pointerParagraph] = prependToLast + self.paragraphList[self.pointerParagraph][n:]

	@overrides(AbstractBlock)
	def scroll(self, n):
		self.scrollPos += n
		if self.scrollPos < 0: self.scrollPos = 0
		if self.scrollPos >= len(self.paragraphList) - 1: self.scrollPos = len(self.paragraphList) - 1

	@staticmethod
	def releaseFocus():
		Block.FOCUSED_BLOCK = NullBlock(0)

	# getters/setters

	def getCurPar(self):
		return self.paragraphList[self.pointerParagraph]

	def setPointerPos(self, pointerPos):
		print pointerPos
		if pointerPos < 0: pointerPos = 0
		if pointerPos > len(self.getCurPar()): pointerPos = len(self.getCurPar())
		self.pointerPos = pointerPos
		
	def setPointerPar(self, pointerPar):
		if pointerPar < 0: pointerPar = 0
		if pointerPar >= len(self.paragraphList): pointerPar = len(self.paragraphList) - 1
		self.pointerParagraph = pointerPar
		
	def pos(self, value = None):
		if value:
			self.left = value[0]
			self.top = value[1]
		return self.left, self.top

	@overrides(AbstractBlock)
	def posAddVector(self, vector):
		self.pos( vectorSum(self.pos(), vector) )

	def getDataForFileSave(self):
		text = ''
		for par in self.paragraphList:
			text += par + '\n'
		return {'pos': self.pos(), 'rate': self.rate, 'text': text}

	def setDataFromFile(self, fileData):
		self.pos(fileData['pos'])
		self.rate = fileData['rate']
		self.insertIntoText(fileData['text'])
		self.pointerPos = 0
		self.pointerParagraph = 0
