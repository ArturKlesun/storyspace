from classes.Drawable.Screen.Block.AbstractBlock import AbstractBlock
from classes.Fp import overrides


class SheetMusicBlock(AbstractBlock):

	@overrides(AbstractBlock)
	def recalcSurfaceInherited(self):
		pass

	@overrides(AbstractBlock)
	def getObjectStateSuccessored(self):
		return {}

	@overrides(AbstractBlock)
	def setObjectStateSuccessored(self, blockData: dict):
		pass

	@overrides(AbstractBlock)
	def getFocusedChild(self):
		return None

	@overrides(AbstractBlock)
	def makeHandler(self):
		return None
