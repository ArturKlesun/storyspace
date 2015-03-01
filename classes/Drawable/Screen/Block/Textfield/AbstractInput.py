from abc import abstractmethod
from classes.Drawable.AbstractDrawable import AbstractDrawable


class AbstractInput(AbstractDrawable):

	@abstractmethod
	def insertIntoText(self, substr):
		raise NotImplementedError("Please Implement this method for " + self.__class__.__name__)

	@abstractmethod
	def deleteFromText(self, n):
		raise NotImplementedError("Please Implement this method for " + self.__class__.__name__)

	@abstractmethod
	def movePointer(self, n):
		raise NotImplementedError("Please Implement this method for " + self.__class__.__name__)

	def scroll(self, n):
		self.setScrollPos(self.scrollPos + n)

	def setScrollPos(self, value):
		self.scrollPos = value
		if self.scrollPos < 0: self.scrollPos = 0
		if self.scrollPos >= self.getFullRowCount(): self.scrollPos = self.getFullRowCount() - 1
		self.recalcSurfaceBacursively()
