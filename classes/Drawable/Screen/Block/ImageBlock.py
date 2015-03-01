from classes.Config import Config
import pygame
from classes.Constants import Constants
from classes.Drawable.AbstractDrawable import AbstractDrawable
from classes.Drawable.Screen.Block.AbstractBlock import AbstractBlock
from classes.Fp import overrides
import classes as huj


class ImageBlock(AbstractBlock):

	def __init__(self, parentScreen, blockData=None):
		self.imageSurface = None
		self.imageName = ''

		super(ImageBlock, self).__init__(parentScreen, blockData)

	@overrides(AbstractBlock)
	def getObjectStateInherited(self):
		return {'imageName': self.imageName}

	@overrides(AbstractBlock)
	def setObjectStateInherited(self, blockData):
		size = self.size()
		self.setImageName(blockData['imageName'] if 'imageName' in blockData else '')
		self.size(size)

	@overrides(AbstractDrawable)
	def getFocusedChild(self):
		return None

	@overrides(AbstractDrawable)
	def getEventHandler(self):
		return huj.Drawable.Screen.Block.FocusedImageBlockEventHandler.FocusedImageBlockEventHandler(self)

	@overrides(AbstractBlock)
	def recalcSurfaceInherited(self):
		if not self.imageSurface is None:
			self.surface.blit(
					pygame.transform.smoothscale(self.imageSurface, self.getImageSize()),
					[Constants.BLOCK_FRAME_WIDTH, Constants.BLOCK_FRAME_WIDTH])

	# getters/setters

	def setImageName(self, value):
		self.imageName = value
		self.imageSurface = Config.getInstance().getImageByName(self.imageName)
		self.size([self.imageSurface.get_width() + Constants.BLOCK_FRAME_WIDTH * 2, self.imageSurface.get_height() + Constants.BLOCK_FRAME_WIDTH * 2])

	def getImageName(self):
		return self.imageName

	def getImageSize(self):
		return self.size()[0] - Constants.BLOCK_FRAME_WIDTH * 2, self.size()[1] - Constants.BLOCK_FRAME_WIDTH * 2