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

	@overrides(AbstractBlock)
	def initDescendant(self):
		super(TextBlock, self).initDescendant()
		Textfield(self)
		Header(self)
		LabelInput(self)
		self.setFocusedIndex(0)

	@overrides(AbstractBlock)
	def recalcSurfaceInherited(self):
		self.getFocusedChild().pos([Constants.BLOCK_FRAME_WIDTH, Constants.BLOCK_FRAME_WIDTH])
		self.getFocusedChild().drawOnParent()
		# if self.getFocusedInput() is not self.getChildTextfield():
		# 	self.getChildTextfield().pos([Constants.BLOCK_FRAME_WIDTH, self.getFocusedInput().getHeight() + Constants.BLOCK_FRAME_WIDTH])
		# 	self.getChildTextfield().drawOnParent()

	@overrides(AbstractBlock)
	def getObjectStateSuccessored(self):
		state = {'rate': self.rate}
		for child in self.getChildList(): state.update({child.__class__.__name__: child.getObjectState()})
		return state

	@overrides(AbstractBlock)
	def setObjectStateSuccessored(self, blockData):
		self.clearChildList()
		self.rate = blockData['rate'] if 'rate' in blockData else -1
		if self.getRootParent().jsonStructureFormatVersion == Constants.PARAGRAPH_NOT_OBJECT_FORMAT_VERSION: # legacy
			Textfield(self).setObjectState(blockData['paragraphTextList'])
			Header(self).setObjectState(blockData['statusString'])
			LabelInput(self).setObjectState(blockData['labelList'])
		else:
			Textfield(self).setObjectState(blockData[Textfield.__name__])
			Header(self).setObjectState(blockData[Header.__name__])
			LabelInput(self).setObjectState(blockData[LabelInput.__name__])

	@overrides(AbstractDrawable)
	def makeHandler(self): return TextBlockHandler(self)

	# TODO: final it in AbstractDrawable mazafaka
	@overrides(AbstractDrawable)
	def getChildList(self):
		""":rtype: list of AbstractDrawable"""
		return self.childList

	@overrides(AbstractDrawable)
	def getDefaultSize(self): return self.__class__.DEFAULT_SIZE

	@overrides(AbstractDrawable)
	def recalcSize(self): self.surface = self.surface = pygame.Surface(self.size())

	# getters/setters

	def switchFocus(self): return self.focusNext() or self.setFocusedIndex(0) is not None # despicable me

	def calcTextfieldSize(self):
		return (self.getWidth() - Constants.BLOCK_FRAME_WIDTH * 2,
			self.getHeight() - Constants.BLOCK_FRAME_WIDTH * 2)

class TextBlockHandler(AbstractBlockHandler):
	@classmethod
	@overrides(AbstractBlockHandler)
	def calcActionDict(cls, textBlockClass):
		actionDict = AbstractBlockHandler.calcActionDict(textBlockClass)
		actionDict.update({ Combo(pygame.KMOD_LCTRL, pygame.K_SLASH): textBlockClass.switchFocus, })
		return actionDict
