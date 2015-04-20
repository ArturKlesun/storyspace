#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from classes.Drawable.Combo import Combo

from classes.Drawable.Screen.Block.AbstractBlock import AbstractBlock
from classes.Drawable.Screen.Block.AbstractBlockHandler import AbstractBlockHandler
from classes.Drawable.Screen.Block.Input.Header import Header
from classes.Drawable.Screen.Block.Input.LabelInput import LabelInput
from classes.Fp import *
from classes.Drawable.Screen.Block.Input.Textfield import Textfield
from classes.Constants import Constants
from classes.Drawable.AbstractDrawable import AbstractDrawable


class TextBlock(AbstractBlock):

	STATUS_BAR_HEIGHT = Constants.CHAR_HEIGHT

	DEFAULT_STATUS_STRING = '{"Имя": "Ираклий", "Оценка": "0", "Кратко": "гузно", "Каммент": "ВсёХуйняДавайСначала"}'

	rate = 0

	def __init__(self, parentScreen):
		self.childTextfield = None
		self.childHeader = None
		self.childLabelInput = None

		super(TextBlock, self).__init__(parentScreen)

		self.childTextfield = Textfield(self)
		self.childHeader = Header(self)
		self.childLabelInput = LabelInput(self)
		self.setFocusedIndex(self.getChildList().index(self.childTextfield))

	@overrides(AbstractBlock)
	def recalcSurfaceInherited(self):
		self.getFocusedInput().pos([Constants.BLOCK_FRAME_WIDTH, Constants.BLOCK_FRAME_WIDTH])
		self.getFocusedInput().drawOnParent()
		if self.getFocusedInput() is not self.getChildTextfield():
			self.getChildTextfield().pos([Constants.BLOCK_FRAME_WIDTH, self.getFocusedInput().getHeight() + Constants.BLOCK_FRAME_WIDTH])
			self.getChildTextfield().drawOnParent()

	@overrides(AbstractBlock)
	def getObjectStateSuccessored(self):
		return {'rate': self.rate, 'headerData': self.getChildHeader().getObjectState(),
				'textfieldData': self.getChildTextfield().getObjectState(), 'labelInputData': self.getChildLabelInput().getObjectState()}

	@overrides(AbstractBlock)
	def setObjectStateSuccessored(self, blockData):
		self.rate = blockData['rate'] if 'rate' in blockData else -1
		if self.getRootParent().jsonStructureFormatVersion == Constants.PARAGRAPH_NOT_OBJECT_FORMAT_VERSION: # legacy
			self.getChildTextfield().setObjectState(blockData['paragraphTextList'])
			self.getChildHeader().setObjectState(blockData['statusString'])
			self.getChildLabelInput().setObjectState(blockData['labelList'])
		else:
			self.getChildTextfield().setObjectState(blockData['textfieldData'])
			self.getChildHeader().setObjectState(blockData['headerData'])
			self.getChildLabelInput().setObjectState(blockData['labelInputData'])

	@overrides(AbstractDrawable)
	def makeHandler(self): return TextBlockHandler(self)

	@overrides(AbstractDrawable)
	def getChildList(self):
		return [self.getChildTextfield(), self.getChildHeader(), self.getChildLabelInput()]

	@overrides(AbstractDrawable)
	def getDefaultSize(self):
		return self.__class__.DEFAULT_SIZE

	@overrides(AbstractDrawable)
	def recalcSize(self):
		self.surface = self.surface = pygame.Surface(self.size())

	# getters/setters

	def getChildTextfield(self) -> Textfield: return self.childTextfield
	def getChildHeader(self) -> Header: return self.childHeader
	def getChildLabelInput(self) -> LabelInput: return self.childLabelInput

	def getFocusedInput(self): return self.getFocusedChild()

	def switchFocus(self):
		if self.getFocusedIndex() == self.setFocusedIndex(self.getFocusedIndex() + 1):
			self.setFocusedIndex(0)
		return True

	def calcTextfieldSize(self):
		return (self.getWidth() - self.getTextfieldRightIndent() - Constants.BLOCK_FRAME_WIDTH,
			self.getHeight() - Constants.BLOCK_FRAME_WIDTH * 2)

	def getTextfieldRightIndent(self):
		# TODO: if scrollbar + scrollbar
		return Constants.BLOCK_FRAME_WIDTH

class TextBlockHandler(AbstractBlockHandler):
	@classmethod
	@overrides(AbstractBlockHandler)
	def calcActionDict(cls, textBlockClass):
		actionDict = AbstractBlockHandler.calcActionDict(textBlockClass)
		actionDict.update({ Combo(pygame.KMOD_LCTRL, pygame.K_SLASH): textBlockClass.switchFocus, })
		return actionDict
