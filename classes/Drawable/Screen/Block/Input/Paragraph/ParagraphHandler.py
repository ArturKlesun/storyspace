import random
import pygame
from classes.Clipboard import Clipboard
from classes.Drawable.AbstractHandler import AbstractHandler
from classes.Drawable.Combo import Combo
from classes.Fp import overrides

class ParagraphHandler(AbstractHandler):

	@classmethod
	@overrides(AbstractHandler)
	def calcActionDict(cls, paragraphClass) -> dict:
		p = pygame
		ctrl = pygame.KMOD_LCTRL
		# TODO: for some reason repeats 4 times - fuck
		actionDict = {
			# debug
			Combo(ctrl, p.K_u): lambda textfield: print(textfield.surfaceChanged, textfield.getSurface().get_width(), textfield.getSurface().get_height()),

			Combo(0, p.K_LEFT): paragraphClass.focusBack,
			Combo(0, p.K_RIGHT): paragraphClass.focusNext,
			Combo(0, p.K_BACKSPACE): paragraphClass.deleteBack, # does not work
			Combo(0, p.K_DELETE): paragraphClass.deleteNext,
			Combo(0, p.K_UP): paragraphClass.rowUp,
			Combo(0, p.K_DOWN): paragraphClass.rowDown,
			Combo(0, p.K_RETURN): lambda par: par.insertIntoText('\n'),

			Combo(ctrl, p.K_LEFT): paragraphClass.focusBackWord,
			Combo(ctrl, p.K_RIGHT): paragraphClass.focusNextWord,
			Combo(ctrl, p.K_c): lambda par: Clipboard.add(par.getText()),
			Combo(ctrl, p.K_v): lambda par: par.insertIntoText(Clipboard.get()),
		}
		for i in range(pygame.K_0, pygame.K_9 + 1):
			actionDict.update({Combo(ctrl, i): lambda par: par.setScore(i - p.K_0)})

		shift = p.KMOD_RSHIFT
		# character input
		for code in Combo.getCharacterKeycodeList():
			actionDict.update({
				Combo(0, code): lambda par, code=code: par.insertIntoText(chr(code)),
				Combo(shift, code): lambda par, code=code: par.insertIntoText(chr(code).upper()),
			})

		return actionDict

