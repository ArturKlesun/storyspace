#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import json
import sys
from classes.TextBlock import TextBlock
from classes.Fp import vectorDiff, vectorSum, vectorReverse
from classes.Clipboard import Clipboard
from classes.Screen import Screen
from pygame.constants import *

pygame.init()

class EventHandler(object):

	IS_RESIZING = False
	MOUSE_SCROLL_STEP_SIZE = 4

	@staticmethod
	def handlePygame():
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				EventHandler.handleKeydown(event)

			elif event.type == pygame.MOUSEBUTTONDOWN:
				Screen.CUR_MOUSE_POS = event.pos
				for block in Screen.getInstance().getBlockInFrameList():
					if block.isPointed(Screen.getInstance().calcMouseAbsolutePos()):
						block.acquireFocus()
						if block.isResizeCornerPointed():
							EventHandler.IS_RESIZING = True
						break
					TextBlock.releaseFocus()

			elif event.type == pygame.MOUSEBUTTONUP:
				if EventHandler.IS_RESIZING:
					TextBlock.FOCUSED_BLOCK.recalcSurfaceRecursively(-1)
					EventHandler.IS_RESIZING = False

				if event.button == 4: # scroll-up
					TextBlock.FOCUSED_BLOCK.getFocusedInput().scroll(-EventHandler.MOUSE_SCROLL_STEP_SIZE)
				elif event.button == 5: #scroll-down
					TextBlock.FOCUSED_BLOCK.getFocusedInput().scroll(EventHandler.MOUSE_SCROLL_STEP_SIZE)

			elif event.type == pygame.MOUSEMOTION:

				displaceVector = vectorDiff(event.pos, Screen.CUR_MOUSE_POS)

				if event.buttons[0]: # left mouse button hold
					if EventHandler.IS_RESIZING:
						TextBlock.FOCUSED_BLOCK.sizeAddVector( displaceVector )
						TextBlock.FOCUSED_BLOCK.recalcSurfaceRecursively(1)
					else:
						TextBlock.FOCUSED_BLOCK.posAddVector( displaceVector )

				if event.buttons[1] or event.buttons[2]: # middle mouse button hold
					Screen.getInstance().moveCam( vectorReverse(displaceVector) );

				Screen.CUR_MOUSE_POS = event.pos

			elif event.type==VIDEORESIZE:
				Screen.getInstance().size(event.dict['size'])
				Screen.getInstance().recalcSize()
			
			elif event.type == pygame.QUIT:
				sys.exit()

	@staticmethod
	def handleKeydown(event):
		blockList = Screen.getInstance().getChildBlockList()

		# excluding capslocks, numlocks, etc...
		bitMask = event.mod & (pygame.KMOD_ALT | pygame.KMOD_CTRL | pygame.KMOD_SHIFT)
		
		if bitMask & pygame.KMOD_LCTRL:
			if event.key == pygame.K_s:
				fileObj = open('asd.json', 'w')
				fileContent= [];
				for block in blockList:
					fileContent.append(block.getObjectState())
				fileObj.write(json.dumps(fileContent, ensure_ascii=False, indent=4).encode('utf8'))
				fileObj.close()
			elif event.key == pygame.K_o:
				fileObj = open('asd.json', 'r')
				fileContent = json.loads(fileObj.read())
				Screen.getInstance().clearBlockList()
				for blockData in fileContent:
					blockList.append(TextBlock(blockData))
				fileObj.close()

			elif event.key == pygame.K_n:
				block = TextBlock({'pos': Screen.getInstance().camPos()}) # TODO: spawn in mouse pos
				blockList.append(block)
				block.acquireFocus()

			elif event.key == pygame.K_c:
				Clipboard.add('huj')
			elif event.key == pygame.K_v:
				TextBlock.FOCUSED_BLOCK.getFocusedInput().insertIntoText(Clipboard.get())

			elif event.key == pygame.K_UP:
				TextBlock.FOCUSED_BLOCK.getFocusedInput().scroll(-1)
			elif event.key == pygame.K_DOWN:
				TextBlock.FOCUSED_BLOCK.getFocusedInput().scroll(1)
			
			elif event.key == pygame.K_i:
				print blockList

			elif event.key == pygame.K_LEFT:
				TextBlock.FOCUSED_BLOCK.getFocusedInput().ctrlMovePointer(-1)
			elif event.key == pygame.K_RIGHT:
				TextBlock.FOCUSED_BLOCK.getFocusedInput().ctrlMovePointer(1)

			elif event.key == pygame.K_BACKSPACE:
				TextBlock.FOCUSED_BLOCK.getFocusedInput().ctrlDeleteFromText(-1)
			elif event.key == pygame.K_DELETE:
				TextBlock.FOCUSED_BLOCK.getFocusedInput().ctrlDeleteFromText(1)

			elif event.key == pygame.K_SLASH:
				TextBlock.DISPLAY_STATUS_BAR = not TextBlock.DISPLAY_STATUS_BAR
				for block in blockList:
					block.size(block.size())
					block.recalcSurfaceRecursively(1)

			elif event.key == pygame.K_EQUALS:
				Screen.getInstance().scale(+1)
			elif event.key == pygame.K_MINUS:
				Screen.getInstance().scale(-1)

			elif event.key == pygame.K_f:
				Screen.getInstance().switchFullscreen()

		elif not bitMask or bitMask == pygame.KMOD_LSHIFT or bitMask == pygame.KMOD_RSHIFT: 
			
			if event.key == pygame.K_LEFT:
				TextBlock.FOCUSED_BLOCK.getFocusedInput().movePointer(-1)
				
			elif event.key == pygame.K_RIGHT:
				TextBlock.FOCUSED_BLOCK.getFocusedInput().movePointer(1)
				
			elif event.key == pygame.K_DOWN:
				TextBlock.FOCUSED_BLOCK.getFocusedInput().movePointerInRows(1)
				
			elif event.key == pygame.K_UP:
				TextBlock.FOCUSED_BLOCK.getFocusedInput().movePointerInRows(-1)
			
			elif event.key == pygame.K_BACKSPACE:
				TextBlock.FOCUSED_BLOCK.getFocusedInput().deleteFromText(-1)

			elif event.key == pygame.K_DELETE:
				TextBlock.FOCUSED_BLOCK.getFocusedInput().deleteFromText(1)

			elif event.key == pygame.K_RETURN:
				TextBlock.FOCUSED_BLOCK.getFocusedInput().insertIntoText('\n')

			elif event.key == pygame.K_PAGEUP:
				textfield = TextBlock.FOCUSED_BLOCK.getFocusedInput()
				textfield.movePointerInRows( - textfield.getPrintedRowCount() / 2 )
			elif event.key == pygame.K_PAGEDOWN:
				textfield = TextBlock.FOCUSED_BLOCK.getFocusedInput()
				textfield.movePointerInRows( textfield.getPrintedRowCount() / 2 )

			elif len(event.unicode):
				TextBlock.FOCUSED_BLOCK.getFocusedInput().insertIntoText(event.unicode)