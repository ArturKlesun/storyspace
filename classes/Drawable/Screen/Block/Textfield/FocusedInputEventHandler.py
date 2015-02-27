import pygame

from classes.Clipboard import Clipboard
from classes.Drawable.AbstractEventHandler import AbstractEventHandler
from classes.Drawable.Screen.Block.Textfield import AbstractTextfield
from classes.Fp import overrides


class FocusedInputEventHandler(AbstractEventHandler):

	MOUSE_SCROLL_STEP_SIZE = 4

	def getInput(self) -> AbstractTextfield:
		return self.getContext()

	@overrides(AbstractEventHandler)
	def handleMouseEvent(self, event: dict, paramsFromParent: dict):
		if event.type == pygame.MOUSEBUTTONUP:

			if event.button == 4: # scroll-up
				self.getInput().scroll(-self.MOUSE_SCROLL_STEP_SIZE)
			elif event.button == 5: #scroll-down
				self.getInput().scroll(self.MOUSE_SCROLL_STEP_SIZE)

		return {}

	@overrides(AbstractEventHandler)
	def handleKeydown(self, event, paramsFromParent: dict):

		# excluding capslocks, numlocks, etc...
		bitMask = event.mod & (pygame.KMOD_ALT | pygame.KMOD_CTRL | pygame.KMOD_SHIFT)
		if bitMask & pygame.KMOD_LCTRL:

			if event.key == pygame.K_c:
				Clipboard.add('huj')
			elif event.key == pygame.K_v:
				self.getInput().insertIntoText(Clipboard.get())

			elif event.key == pygame.K_UP:
				self.getInput().scroll(-1)
			elif event.key == pygame.K_DOWN:
				self.getInput().scroll(1)

			elif event.key == pygame.K_LEFT:
				self.getInput().ctrlMovePointer(-1)
			elif event.key == pygame.K_RIGHT:
				self.getInput().ctrlMovePointer(1)

			elif event.key == pygame.K_BACKSPACE:
				self.getInput().ctrlDeleteFromText(-1)
			elif event.key == pygame.K_DELETE:
				self.getInput().ctrlDeleteFromText(1)

		elif not bitMask or bitMask == pygame.KMOD_LSHIFT or bitMask == pygame.KMOD_RSHIFT:

			if event.key == pygame.K_LEFT:
				self.getInput().movePointer(-1)

			elif event.key == pygame.K_RIGHT:
				self.getInput().movePointer(1)

			elif event.key == pygame.K_DOWN:
				self.getInput().movePointerInRows(1)

			elif event.key == pygame.K_UP:
				self.getInput().movePointerInRows(-1)

			elif event.key == pygame.K_BACKSPACE:
				self.getInput().deleteFromText(-1)

			elif event.key == pygame.K_DELETE:
				self.getInput().deleteFromText(1)

			elif event.key == pygame.K_RETURN:
				self.getInput().insertIntoText('\n')

			elif event.key == pygame.K_PAGEUP:
				self.getInput().movePointerInRows( - self.getInput().getPrintedRowCount() // 2 )
			elif event.key == pygame.K_PAGEDOWN:
				self.getInput().movePointerInRows( self.getInput().getPrintedRowCount() // 2 )

			elif len(event.unicode):
				self.getInput().insertIntoText(event.unicode)

		return {}

	@overrides(AbstractEventHandler)
	def handleSpecificEvent(self, event: dict, paramsFromParent: dict):
		return {}
