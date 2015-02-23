from abc import ABCMeta, abstractmethod

from classes.Drawable.AbstractDrawable import AbstractDrawable


class AbstractTextfield(AbstractDrawable):
	
	__metaclass__ = ABCMeta
	
	@abstractmethod
	def scroll(self, n):
		raise NotImplementedError("Please Implement this method")
	
	@abstractmethod
	def insertIntoText(self, substr):
		raise NotImplementedError("Please Implement this method")
	
	@abstractmethod
	def deleteFromText(self, n):
		raise NotImplementedError("Please Implement this method")
	
	@abstractmethod
	def movePointer(self, n):
		raise NotImplementedError("Please Implement this method")
	
	@abstractmethod
	def movePar(self, n):
		raise NotImplementedError("Please Implement this method")

	@abstractmethod
	def getParagraphList(self):
		raise NotImplementedError("Please Implement this method")

