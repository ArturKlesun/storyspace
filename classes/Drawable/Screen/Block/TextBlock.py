#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame

from classes.Drawable.Screen.Block.AbstractBlock import AbstractBlock
from classes.Drawable.Screen.Block.Textfield.AbstractInput import AbstractInput
from classes.Drawable.Screen.Block.Textfield.LabelInput import LabelInput
from classes.Fp import *
from classes.Drawable.Screen.Block.Textfield.Textfield import Textfield
from classes.Constants import Constants
from classes.Drawable.AbstractDrawable import AbstractDrawable
import classes as huj


class TextBlock(AbstractBlock):

	STATUS_BAR_HEIGHT = Constants.CHAR_HEIGHT

	DEFAULT_STATUS_STRING = '{"Имя": "Ираклий", "Оценка": "0", "Кратко": "гузно", "Каммент": "ВсёХуйняДавайСначала"}'

	rate = 0

	def __init__(self, parentScreen, blockData={}):
		self.childTextfield = None
		self.childStatusInput = None
		self.childLabelInput = None
		self.focusedInput = None

		super(TextBlock, self).__init__(parentScreen, blockData)

		self.getChildStatusInput().setTextBgColor([191,191,191])
		self.getChildStatusInput().setTextColor([127,63,0])
		self.focusedInput = self.getChildTextfield()


	def __str__(self):
		return 'Block: ' + str(self.getChildTextfield())

	def __repr__(self):
		return self.__str__() + '\n'


	@overrides(AbstractBlock)
	def recalcSurfaceInherited(self):
		self.getFocusedInput().pos([Constants.BLOCK_FRAME_WIDTH, Constants.BLOCK_FRAME_WIDTH])
		self.getFocusedInput().drawOnParent()
		if self.getFocusedInput() is not self.getChildTextfield():
			self.getChildTextfield().pos([Constants.BLOCK_FRAME_WIDTH, self.getFocusedInput().getHeight() + Constants.BLOCK_FRAME_WIDTH])
			self.getChildTextfield().drawOnParent()

	@overrides(AbstractBlock)
	def getObjectStateInherited(self):
		return {'rate': self.rate, 'statusString': self.getChildStatusInput().getParagraphTextList(),
				'paragraphTextList': self.getChildTextfield().getParagraphTextList(), 'labelList': self.getChildLabelInput().labelList}

	@overrides(AbstractBlock)
	def setObjectStateInherited(self, blockData):
		self.rate = blockData['rate'] if 'rate' in blockData else -1
		for parText in (blockData['paragraphTextList'] if 'paragraphTextList' in blockData else []):
			self.getChildTextfield().insertIntoText(parText + '\n')
		self.getChildTextfield().deleteFromText(-1)
		for parText in (blockData['statusString'] if 'statusString' in blockData else [TextBlock.DEFAULT_STATUS_STRING]):
			self.getChildStatusInput().insertIntoText(parText + '\n')
		self.getChildStatusInput().deleteFromText(-1)
		for label in  blockData['labelList'] if 'labelList' in blockData else []:
			self.getChildLabelInput().addLabel(label)
		self.getChildLabelInput().setPointer(0)
		self.getChildLabelInput().deleteLabel()

		self.getChildTextfield().setPointerPar(0)
		self.getChildTextfield().getCurPar().setPointerPos(0)

	@overrides(AbstractDrawable)
	def getEventHandler(self):
		""":rtype: classes.Drawable.Screen.Block.FocusedTextBlockEventHandler.FocusedTextBlockEventHandler"""
		return huj.Drawable.Screen.Block.FocusedTextBlockEventHandler.FocusedTextBlockEventHandler(self)

	@overrides(AbstractDrawable)
	def getFocusedChild(self) -> AbstractInput:
		return self.getFocusedInput()

	@overrides(AbstractDrawable)
	def getDefaultSize(self):
		return self.__class__.DEFAULT_SIZE

	# getters/setters

	def getChildTextfield(self):
		if self.childTextfield is None: self.childTextfield = Textfield(self)
		return self.childTextfield

	def getChildStatusInput(self):
		if self.childStatusInput is None: self.childStatusInput = Textfield(self)
		return self.childStatusInput

	def getChildLabelInput(self):
		if self.childLabelInput is None:
			self.childLabelInput = LabelInput(self)
		return self.childLabelInput

	def getFocusedInput(self):
		return self.focusedInput

	def switchFocus(self):
		if self.focusedInput is self.getChildTextfield():
			self.focusedInput = self.getChildStatusInput()
		elif self.focusedInput is self.getChildStatusInput():
			self.focusedInput = self.getChildLabelInput()
		else:
			self.focusedInput = self.getChildTextfield()

		self.getChildTextfield().recalcSize()
		self.recalcSurfaceBacursively()

	def calcTextfieldSize(self):
		return (self.getWidth() - self.getTextfieldRightIndent() - Constants.BLOCK_FRAME_WIDTH,
			self.getHeight() - (self.getFocusedInput().getHeight() if self.getFocusedInput() and self.getFocusedInput() is not self.childTextfield else 0) - Constants.BLOCK_FRAME_WIDTH * 2)

	def getTextfieldRightIndent(self):
		# TODO: if scrollbar + scrollbar
		return Constants.BLOCK_FRAME_WIDTH

