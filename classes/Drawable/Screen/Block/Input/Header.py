import pygame
from classes.Constants import Constants
from classes.Drawable.AbstractDrawable import AbstractDrawable
from classes.Drawable.Screen.Block.Input.HeaderHandler import HeaderHandler
from classes.Fp import overrides


class Header(AbstractDrawable):

	@overrides(AbstractDrawable)
	def __init__(self, parent):
		self.legacyStatusString = '';
		super(Header, self).__init__(parent)

	def getObjectState(self):
		return {'legacyStatusString': self.legacyStatusString}

	@overrides(AbstractDrawable)
	def setObjectState(self, headerData):
		if self.getRootParent().jsonStructureFormatVersion == Constants.PARAGRAPH_NOT_OBJECT_FORMAT_VERSION: # legacy
			self.legacyStatusString = headerData
		else:
			self.legacyStatusString = headerData['legacyStatusString']

	@overrides(AbstractDrawable)
	def size(self, value = None): return self.getParent().size()

	@overrides(AbstractDrawable)
	def recalcSurface(self): self.surface = pygame.Surface(self.size())

	@overrides(AbstractDrawable)
	def getDefaultSize(self): return [Constants.CHAR_WIDTH, Constants.CHAR_HEIGHT]

	@overrides(AbstractDrawable)
	def makeHandler(self): return HeaderHandler(self)

	@overrides(AbstractDrawable)
	def getChildList(self): return []
	@overrides(AbstractDrawable)
	def getFocusedChild(self): return None
	@overrides(AbstractDrawable)
	def recalcSize(self): pass