#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import json
import sys
from classes.Block import Block
from classes.Fp import vectorDiff
from classes.Clipboard import Clipboard
from classes.Screen import Screen
from pygame.constants import *

pygame.init()

class EventHandler(object):

	IS_RESIZING = False
	IS_MOUSE_DOWN = False
	CUR_MOUSE_POS = [0,0]

	@staticmethod
	def handlePygame(blockList):
		for event in pygame.event.get():
			# TODO: KeyHold
			if event.type == pygame.KEYDOWN:
				EventHandler.handleKeydown(event, blockList)

			elif event.type == pygame.MOUSEBUTTONDOWN:
				EventHandler.CUR_MOUSE_POS = event.pos;
				for block in blockList:
					if block.isPointed(event.pos):
						block.acquireFocus()
						if block.isResizeCornerPointed(event.pos):
							EventHandler.IS_RESIZING = True
						break
					Block.releaseFocus()
				EventHandler.IS_MOUSE_DOWN = True

			elif event.type == pygame.MOUSEBUTTONUP:
				EventHandler.IS_MOUSE_DOWN = False
				if EventHandler.IS_RESIZING:
					for par in Block.FOCUSED_BLOCK.getChildTextfield().getParagraphList(): #: :type par: Paragraph
						par.rowListChanged = True
					Block.FOCUSED_BLOCK.getChildTextfield().rowListChanged = True
					EventHandler.IS_RESIZING = False

			elif event.type == pygame.MOUSEMOTION:
				
				if EventHandler.IS_MOUSE_DOWN:
					if EventHandler.IS_RESIZING:
						Block.FOCUSED_BLOCK.sizeAddVector( vectorDiff(event.pos, EventHandler.CUR_MOUSE_POS) )
					else:
						Block.FOCUSED_BLOCK.posAddVector( vectorDiff(event.pos, EventHandler.CUR_MOUSE_POS) )
				EventHandler.CUR_MOUSE_POS = event.pos

			elif event.type==VIDEORESIZE:
				Screen.setScreen(pygame.display.set_mode(event.dict['size'],HWSURFACE|DOUBLEBUF|RESIZABLE))
			
			elif event.type == pygame.QUIT:
				sys.exit()

	@staticmethod
	def handleKeydown(event, blockList):
		
		# excluding capslocks, numlocks, etc...
		bitMask = event.mod & (pygame.KMOD_ALT | pygame.KMOD_CTRL | pygame.KMOD_SHIFT)
		
		if bitMask & pygame.KMOD_LCTRL:
			if event.key == pygame.K_s:
				fileObj = open('asd.json', 'w')
				fileContent= [];
				for block in blockList:
					fileContent.append(block.getDataForFileSave())
				fileObj.write(json.dumps(fileContent, ensure_ascii=False, indent=4).encode('utf8'))
				fileObj.close()
			elif event.key == pygame.K_o:
				fileObj = open('asd.json', 'r')
				fileContent = json.loads(fileObj.read())
				del blockList[:]
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
				Block.FOCUSED_BLOCK.getChildTextfield().insertIntoText(Clipboard.get())

			elif event.key == pygame.K_UP:
				Block.FOCUSED_BLOCK.getChildTextfield().scroll(-1)
			elif event.key == pygame.K_DOWN:
				Block.FOCUSED_BLOCK.getChildTextfield().scroll(1)
			
			elif event.key == pygame.K_i:
				print blockList

			elif event.key == pygame.K_LEFT:
				Block.FOCUSED_BLOCK.getChildTextfield().ctrlMovePointer(-1)
			elif event.key == pygame.K_RIGHT:
				Block.FOCUSED_BLOCK.getChildTextfield().ctrlMovePointer(1)

			elif event.key == pygame.K_BACKSPACE:
				Block.FOCUSED_BLOCK.getChildTextfield().ctrlDeleteFromText(-1)
			elif event.key == pygame.K_DELETE:
				Block.FOCUSED_BLOCK.getChildTextfield().ctrlDeleteFromText(1)

		elif not bitMask: 
			
			if event.key == pygame.K_LEFT:
				Block.FOCUSED_BLOCK.getChildTextfield().movePointer(-1)
				
			elif event.key == pygame.K_RIGHT:
				Block.FOCUSED_BLOCK.getChildTextfield().movePointer(1)
				
			elif event.key == pygame.K_DOWN:
				Block.FOCUSED_BLOCK.getChildTextfield().movePointerInRows(1)
				
			elif event.key == pygame.K_UP:
				Block.FOCUSED_BLOCK.getChildTextfield().movePointerInRows(-1)
			
			elif event.key == pygame.K_BACKSPACE:
				Block.FOCUSED_BLOCK.getChildTextfield().deleteFromText(-1)

			elif event.key == pygame.K_DELETE:
				Block.FOCUSED_BLOCK.getChildTextfield().deleteFromText(1)

			elif event.key == pygame.K_RETURN:
				Block.FOCUSED_BLOCK.getChildTextfield().insertIntoText('\n')

			elif len(event.unicode):
				Block.FOCUSED_BLOCK.getChildTextfield().insertIntoText(event.unicode)