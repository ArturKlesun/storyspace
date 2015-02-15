from classes.Fp import overrides
from classes.AbstractBlock import AbstractBlock
from classes.NullTextfield import NullTextfield
from classes.AbstractDrawable import AbstractDrawable

class NullBlock(AbstractBlock):

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

	def getFocusedInput(self):
		return self.getChildTextfield()

	@overrides(AbstractDrawable)
	def recalcSize(self):
		pass
	
	def drawOnParent(self, shiftVector=[0,0]):
		pass