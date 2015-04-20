import pygame
from classes.Drawable.AbstractHandler import AbstractHandler
from classes.Drawable.Combo import Combo
from classes.Fp import overrides

class LabelInputHandler(AbstractHandler):

	@classmethod
	@overrides(AbstractHandler)
	def calcActionDict(cls, inputClass) -> dict:
		p = pygame
		actionDict = {
			Combo(0, p.K_LEFT): inputClass.focusBack,
			Combo(0, p.K_RIGHT): inputClass.focusNext,
			Combo(0, p.K_BACKSPACE): inputClass.deleteBack,
			Combo(0, p.K_DELETE): inputClass.deleteNext,
		}

		shift = p.KMOD_SHIFT
		# character input
		for code in Combo.getCharacterKeycodeList():
			actionDict.update({
				Combo(0, code): lambda someInput: someInput.insertIntoText(chr(code)),
				Combo(shift, code): lambda someInput: someInput.insertIntoText(chr(code).upper()),
			})

		return actionDict
