from classes.Constants import Constants
from classes.Drawable.AbstractDrawable import AbstractDrawable
from classes.Drawable.Screen.Dialog.IDialogCaller import IDialogCaller
import classes as huj

class Dialog(AbstractDrawable):

	def __init__(self, parent: AbstractDrawable, interceptor: IDialogCaller, params: dict):
		self.pointer = 0
		self.options = []
		self.interceptor = interceptor

		super(Dialog, self).__init__(parent)

		self.setWidth(params['width'])
		self.pos(params['pos'])
		self.options = params['options']
		self.setHeight(len(self.options) * Constants.CHAR_HEIGHT)

	def movePointer(self, n):
		self.setPointer(self.pointer + n)
		self.recalcSurfaceBacursively()

	def setPointer(self, value):
		if value < 0: value = 0
		if value >= len(self.options): value = len(self.options) - 1
		self.pointer = value

	def retrieveSelectedOption(self):
		selectedOption = self.options[self.pointer] if self.pointer < len(self.options) else ''
		self.interceptor.receiveDialogResult(selectedOption)

	def getFocusedChild(self):
		return None

	def recalcSurface(self):
		self.surface.fill([191,255,191])
		for idx in range(0, len(self.options)): self.surface.blit(Constants.PROJECT_FONT.render(
					self.options[idx], 1, [0,0,0],
					([191,191,255] if idx == self.pointer else [255,255,255])),
				[0,idx*Constants.CHAR_HEIGHT])

	def getDefaultSize(self):
		return [1,1]

	def recalcSize(self):
		pass

	def getEventHandler(self):
		""":rtype: huj.Drawable.Screen.Dialog.DialogEventHandler.DialogEventHandler"""
		return huj.Drawable.Screen.Dialog.DialogEventHandler.DialogEventHandler(self)