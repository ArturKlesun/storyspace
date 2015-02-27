from classes.Drawable.AbstractDrawable import AbstractDrawable
from classes.Drawable.Screen.Block.AbstractBlock import AbstractBlock
from classes.Fp import overrides
import classes as huj


class ImageBlock(AbstractBlock):

	def __init__(self, parentScreen, blockData=None):
		super(ImageBlock, self).__init__(parentScreen, blockData)

		if self.imagePath is None: self.imagePath = ''

	@overrides(AbstractBlock)
	def getObjectStateInherited(self):
		return {'imagePath': self.imagePath}

	@overrides(AbstractBlock)
	def setObjectStateInherited(self, blockData):
		self.imagePath = blockData['imagePath'] if 'imagePath' in blockData else ''

	@overrides(AbstractDrawable)
	def getFocusedChild(self):
		return None

	@overrides(AbstractDrawable)
	def getEventHandler(self):
		return huj.Drawable.Screen.Block.FocusedImageBlockEventHandler.FocusedImageBlockEventHandler(self)

	@overrides(AbstractDrawable)
	def recalcSurface(self):
		pass

	@overrides(AbstractDrawable)
	def getSurface(self):
		return

