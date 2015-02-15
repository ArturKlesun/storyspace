#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import json
import sys
from classes.Block import Block
from classes.Fp import vectorDiff, vectorSum
from classes.Clipboard import Clipboard
from classes.Screen import Screen
from pygame.constants import *

pygame.init()

class EventHandler(object):

	IS_RESIZING = False
	IS_MOUSE_DOWN = False

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
					Block.releaseFocus()
				EventHandler.IS_MOUSE_DOWN = True

			elif event.type == pygame.MOUSEBUTTONUP:
				EventHandler.IS_MOUSE_DOWN = False
				if EventHandler.IS_RESIZING:
					Block.FOCUSED_BLOCK.recalcSurfaceRecursively(-1)
					EventHandler.IS_RESIZING = False

			elif event.type == pygame.MOUSEMOTION:
				
				if EventHandler.IS_MOUSE_DOWN:
					if EventHandler.IS_RESIZING:
						Block.FOCUSED_BLOCK.sizeAddVector( vectorDiff(event.pos, Screen.CUR_MOUSE_POS) )
						Block.FOCUSED_BLOCK.recalcSurfaceRecursively(1)
					else:
						Block.FOCUSED_BLOCK.posAddVector( vectorDiff(event.pos, Screen.CUR_MOUSE_POS) )
				Screen.CUR_MOUSE_POS = event.pos

			elif event.type==VIDEORESIZE:
				Screen.getInstance().size(event.dict['size'])
				Screen.getInstance().recalcScreen()
			
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
					blockList.append(Block(blockData))
				fileObj.close()

			elif event.key == pygame.K_n:
				block = Block()
				blockList.append(block)
				block.acquireFocus()

			elif event.key == pygame.K_c:
				Clipboard.add('huj')
			elif event.key == pygame.K_v:
				Block.FOCUSED_BLOCK.getFocusedInput().insertIntoText(Clipboard.get())

			elif event.key == pygame.K_UP:
				Block.FOCUSED_BLOCK.getFocusedInput().scroll(-1)
			elif event.key == pygame.K_DOWN:
				Block.FOCUSED_BLOCK.getFocusedInput().scroll(1)
			
			elif event.key == pygame.K_i:
				print blockList

			elif event.key == pygame.K_LEFT:
				Block.FOCUSED_BLOCK.getFocusedInput().ctrlMovePointer(-1)
			elif event.key == pygame.K_RIGHT:
				Block.FOCUSED_BLOCK.getFocusedInput().ctrlMovePointer(1)

			elif event.key == pygame.K_BACKSPACE:
				Block.FOCUSED_BLOCK.getFocusedInput().ctrlDeleteFromText(-1)
			elif event.key == pygame.K_DELETE:
				Block.FOCUSED_BLOCK.getFocusedInput().ctrlDeleteFromText(1)

			elif event.key == pygame.K_SLASH:
				Block.DISPLAY_STATUS_BAR = not Block.DISPLAY_STATUS_BAR
				for block in blockList:
					block.size(block.size())
					block.recalcSurfaceRecursively(1)

			elif event.key == pygame.K_f:
				Screen.getInstance().switchFullscreen()

		elif not bitMask or bitMask == pygame.KMOD_LSHIFT or bitMask == pygame.KMOD_RSHIFT: 
			
			if event.key == pygame.K_LEFT:
				Block.FOCUSED_BLOCK.getFocusedInput().movePointer(-1)
				
			elif event.key == pygame.K_RIGHT:
				Block.FOCUSED_BLOCK.getFocusedInput().movePointer(1)
				
			elif event.key == pygame.K_DOWN:
				Block.FOCUSED_BLOCK.getFocusedInput().movePointerInRows(1)
				
			elif event.key == pygame.K_UP:
				Block.FOCUSED_BLOCK.getFocusedInput().movePointerInRows(-1)
			
			elif event.key == pygame.K_BACKSPACE:
				Block.FOCUSED_BLOCK.getFocusedInput().deleteFromText(-1)

			elif event.key == pygame.K_DELETE:
				Block.FOCUSED_BLOCK.getFocusedInput().deleteFromText(1)

			elif event.key == pygame.K_RETURN:
				Block.FOCUSED_BLOCK.getFocusedInput().insertIntoText('\n')

			elif event.key == pygame.K_PAGEUP:
				textfield = Block.FOCUSED_BLOCK.getFocusedInput()
				textfield.movePointerInRows( - textfield.getPrintedRowCount() / 2 )
			elif event.key == pygame.K_PAGEDOWN:
				textfield = Block.FOCUSED_BLOCK.getFocusedInput()
				textfield.movePointerInRows( textfield.getPrintedRowCount() / 2 )

			elif len(event.unicode):
				Block.FOCUSED_BLOCK.getFocusedInput().insertIntoText(event.unicode)