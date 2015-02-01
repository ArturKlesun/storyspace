from abc import ABCMeta, abstractmethod

class AbstractBlock(object):

	__metaclass__ = ABCMeta
	
	@abstractmethod
	def __init__(self, blockId):
		raise NotImplementedError("Please Implement this method")

	@abstractmethod
	def isResizeCornerPointed(self):
		raise NotImplementedError("Please Implement this method")

	@abstractmethod
	def sizeAddVector(self, vector):
		raise NotImplementedError("Please Implement this method")

	@abstractmethod
	def posAddVector(self, vector):
		raise NotImplementedError("Please Implement this method")

	@abstractmethod
	def getChildTextfield(self):
		raise NotImplementedError("Please Implement this method")