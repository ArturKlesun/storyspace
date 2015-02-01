from classes.Fp import overrides
from classes.AbstractBlock import AbstractBlock
from classes.NullTextfield import NullTextfield

class NullBlock(AbstractBlock):

	@overrides(AbstractBlock)
	def __init__(self):
		pass

	@overrides(AbstractBlock)
	def isResizeCornerPointed(self):
		return False

	@overrides(AbstractBlock)
	def sizeAddVector(self, vector):
		pass
	
	@overrides(AbstractBlock)
	def posAddVector(self, vector):
		pass

	@overrides(AbstractBlock)
	def getChildTextfield(self):
		return NullTextfield()