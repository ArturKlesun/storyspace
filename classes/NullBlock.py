from classes.Fp import overrides
from classes.AbstractBlock import AbstractBlock

class NullBlock(AbstractBlock):

	@overrides(AbstractBlock)
	def __init__(self, blockId):
		pass

	@overrides(AbstractBlock)
	def movePointer(self, n):
		pass

	@overrides(AbstractBlock)
	def posAddVector(self, vector):
		pass

	@overrides(AbstractBlock)
	def insertIntoText(self, substr):
		pass

	@overrides(AbstractBlock)
	def deleteFromText(self, n):
		pass

	@overrides(AbstractBlock)
	def scroll(self, n):
		pass
		