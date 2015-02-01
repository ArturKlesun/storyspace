#!/usr/bin/env python
# -*- coding: utf-8 -*-

from classes.Fp import split

class Paragraph(object):

	text = u''

	def __init__(self, parentTextfield, text):
		self.parentTextfield = parentTextfield
		self.setText(text)

	def __str__(self):
		return 'Paragraph: |' + self.getText() + '|'

	def __repr__(self):
		return '\n\t\t' + self.__str__()

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

	def getRowList(self):
		rowList = []
		charInRowCount = self.getParentTextfield().getCharInRowCount()
		textLeft = self.getText()
		while len(textLeft) > 0:
			row, textLeft = split(textLeft, charInRowCount)
			rowList.append(row)
		return rowList if len(rowList) > 0 else ['']
	
	def getParentTextfield(self):
		return self.parentTextfield
		
	def setParentTextfield(self, value):
		self.parentTextfield = value
	
	def getTextLen(self):
		return len(self.getText()) + 1 # + 1 for eol

	def getText(self):
		return self.text

	def setText(self, value):
		self.text = value
