from classes.Fp import overrides
from classes.AbstractBlock import AbstractBlock
from classes.NullTextfield import NullTextfield
from classes.AbstractDrawable import AbstractDrawable

class NullBlock(AbstractBlock):

	@overrides(AbstractDrawable)
	def calcSurface(self):
		pass

	@overrides(AbstractBlock)
	def isResizeCornerPointed(self):
		return False

	@overrides(AbstractBlock)
	def getChildTextfield(self):
		return NullTextfield()

	def getFocusedInput(self):
		return self.getChildTextfield()

	@overrides(AbstractDrawable)
	def recalcSize(self):
		pass

	@overrides(AbstractDrawable)
	def drawOnParent(self, shiftVector=[0,0]):
		pass