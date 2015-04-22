import pygame

from classes.Drawable.Combo import Combo
from classes.Drawable.Screen.Block.Input.LabelInputHandler import LabelInputHandler
from classes.Fp import overrides


class TextfieldHandler(LabelInputHandler):

	SCROLL_STEP = 4

	def getTextfield(self):
		""":rtype: classes.Drawable.Screen.Block.Input.Textfield.Textfield"""
		return self.getContext()

	@classmethod
	@overrides(LabelInputHandler)
	def calcActionDict(cls, textfieldClass) -> dict:
		p = pygame
		ctrl = p.KMOD_LCTRL
		return {
			Combo(0, p.K_LEFT): textfieldClass.focusBack,
			Combo(0, p.K_RIGHT): textfieldClass.focusNext,
			Combo(0, p.K_UP): textfieldClass.scrollUp,
			Combo(0, p.K_DOWN): textfieldClass.rowDown,
			Combo(0, p.K_BACKSPACE): textfieldClass.mergeBack,
			Combo(0, p.K_DELETE): textfieldClass.mergeNext,
			# TODO: broken
			Combo(0, p.K_PAGEUP): lambda textfield: textfield.movePointerInRows(-textfield.getPrintedRowCount() // 2 ),
			Combo(0, p.K_PAGEDOWN): lambda textfield: textfield.movePointerInRows(textfield.getPrintedRowCount() // 2 ),

			Combo(ctrl, p.K_UP): textfieldClass.scrollUp,
			Combo(ctrl, p.K_DOWN): textfieldClass.scrollDown,
			Combo(ctrl, p.K_LEFT): textfieldClass.focusNext,
			Combo(ctrl, p.K_RIGHT): textfieldClass.focusBack,
			Combo(ctrl, p.K_BACKSPACE): textfieldClass.mergeBack,
			Combo(ctrl, p.K_DELETE): textfieldClass.mergeNext,
		}

	@overrides(LabelInputHandler)
	def handleMouseEvent(self, event: dict):
		if event.type == pygame.MOUSEBUTTONUP:

			if event.button == 4: self.getTextfield().scrollUp()
			elif event.button == 5: self.getTextfield().scrollDown()
