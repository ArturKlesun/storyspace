from classes.Clipboard import Clipboard
from classes.Config import Config
import pygame
from classes.Constants import Constants
from classes.Drawable.AbstractDrawable import AbstractDrawable
from classes.Drawable.Combo import Combo
from classes.Drawable.Screen.Block.AbstractBlock import AbstractBlock
from classes.Drawable.Screen.Block.AbstractBlockHandler import AbstractBlockHandler
from classes.Fp import overrides


class ImageBlock(AbstractBlock):

	def __init__(self, parentScreen):
		self.imageSurface = None
		self.imageName = ''

		super(ImageBlock, self).__init__(parentScreen)

	@overrides(AbstractDrawable)
	def getChildList(self): return []
	@overrides(AbstractDrawable)
	def getFocusedChild(self): return None

	@overrides(AbstractDrawable)
	def makeHandler(self): return ImageBlockHandler(self)

	@overrides(AbstractBlock)
	def recalcSurfaceInherited(self):
		if not self.imageSurface is None:
			self.surface.blit(
					pygame.transform.smoothscale(self.imageSurface, self.getImageSize()),
					[Constants.BLOCK_FRAME_WIDTH, Constants.BLOCK_FRAME_WIDTH])

	@overrides(AbstractBlock)
	def getObjectStateSuccessored(self):
		return {'imageName': self.imageName}

	@overrides(AbstractBlock)
	def setObjectStateSuccessored(self, blockData):
		size = self.size()
		self.setImageNameFromClipboard(blockData['imageName'] if 'imageName' in blockData else '')
		self.size(size)

	# getters/setters

	def setImageNameFromClipboard(self):
		self.imageName = Clipboard.get()
		self.imageSurface = Config.getInstance().getImageByName(self.imageName)
		self.size([self.imageSurface.get_width() + Constants.BLOCK_FRAME_WIDTH * 2, self.imageSurface.get_height() + Constants.BLOCK_FRAME_WIDTH * 2])

	def getImageName(self):
		return self.imageName

	def getImageSize(self):
		return self.size()[0] - Constants.BLOCK_FRAME_WIDTH * 2, self.size()[1] - Constants.BLOCK_FRAME_WIDTH * 2

class ImageBlockHandler(AbstractBlockHandler):
	@classmethod
	@overrides(AbstractBlockHandler)
	def calcActionDict(cls, imageBlockClass):
		actionDict = super(ImageBlockHandler).calcActionDict(imageBlockClass)
		actionDict.update({ Combo(pygame.KMOD_LCTRL, pygame.K_v): imageBlockClass.setImageNameFromClipboard, })
		return actionDict
