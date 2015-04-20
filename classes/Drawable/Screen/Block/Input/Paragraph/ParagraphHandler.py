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
		actionDict = {
			Combo(0, p.K_LEFT): paragraphClass.focusBack,
			Combo(0, p.K_RIGHT): paragraphClass.focusNext,
			Combo(0, p.K_BACKSPACE): paragraphClass.deleteBack,
			Combo(0, p.K_DELETE): paragraphClass.deleteNext,
			Combo(0, p.K_UP): paragraphClass.rowDown,
			Combo(0, p.K_DOWN): paragraphClass.rowUp,
			Combo(0, p.K_RETURN): lambda par: par.insertIntoText('\n'),

			Combo(ctrl, p.K_LEFT): paragraphClass.focusBackWord,
			Combo(ctrl, p.K_RIGHT): paragraphClass.focusNextWord,
			Combo(ctrl, p.K_c): lambda par: Clipboard.add(par.getText()),
			Combo(ctrl, p.K_v): lambda par: par.insertIntoText(Clipboard.get()),
		}
		for i in range(pygame.K_0, pygame.K_9 + 1):
			actionDict.update({Combo(ctrl, i): lambda par: par.setScore(i - p.K_0)})

		return actionDict

	@overrides(AbstractHandler)
	def handleSpecificEvent(self, event: dict):
		pass

	@overrides(AbstractHandler)
	def handleMouseEvent(self, event: dict):
		pass

