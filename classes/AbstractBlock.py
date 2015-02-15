from abc import ABCMeta, abstractmethod
from classes.AbstractDrawable import AbstractDrawable

class AbstractBlock(AbstractDrawable):

	__metaclass__ = ABCMeta

	DISPLAY_STATUS_BAR = False

	@abstractmethod
	def isResizeCornerPointed(self):
		raise NotImplementedError("Please Implement this method")

	@abstractmethod
	def getChildTextfield(self):
		raise NotImplementedError("Please Implement this method")