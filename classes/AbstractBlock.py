from abc import ABCMeta, abstractmethod

class AbstractBlock(object):

	__metaclass__ = ABCMeta
	
	@abstractmethod
	def __init__(self, blockId):
		raise NotImplementedError("Please Implement this method")
	
	@abstractmethod
	def movePointer(self, n):
		raise NotImplementedError("Please Implement this method")

	@abstractmethod
	def posAddVector(self, vector):
		raise NotImplementedError("Please Implement this method")

	@abstractmethod
	def insertIntoText(self, substr):
		raise NotImplementedError("Please Implement this method")

	@abstractmethod
	def deleteFromText(self, n):
		raise NotImplementedError("Please Implement this method")

	@abstractmethod
	def scroll(self, n):
		raise NotImplementedError("Please Implement this method")
		