#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import json
import sys
from classes.Block import Block
from classes.Fp import vectorDiff
from Tkinter import Tk
from classes.Clipboard import Clipboard

pygame.init()

class EventHandler(object):

	IS_MOUSE_DOWN = False
	LAST_DRAG_POS = (0,0)

	@staticmethod
	def handlePygame(blockList):
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				
				if event.mod & event.mod == pygame.KMOD_LCTRL: # ONLY lctr
					
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
							block = Block()
							block.setDataFromFile(blockData)
							blockList.append(block)
						fileObj.close()

					elif event.key == pygame.K_n:
						blockList.append(Block())

					elif event.key == pygame.K_c:
						Clipboard.add('huj')
					elif event.key == pygame.K_v:
						Block.FOCUSED_BLOCK.insertIntoText(Clipboard.get())

					elif event.key == pygame.K_UP:
						Block.FOCUSED_BLOCK.scroll(-1)
					elif event.key == pygame.K_DOWN:
						Block.FOCUSED_BLOCK.scroll(1)
	
				elif event.key == pygame.K_LEFT:
					Block.FOCUSED_BLOCK.movePointer(-1)
				elif event.key == pygame.K_RIGHT:
					Block.FOCUSED_BLOCK.movePointer(1)

				elif not event.mod: 
					
					if event.key == pygame.K_BACKSPACE:
						Block.FOCUSED_BLOCK.deleteFromText(-1)

					elif event.key == pygame.K_DELETE:
						Block.FOCUSED_BLOCK.deleteFromText(1)

					elif event.key == pygame.K_RETURN:
						Block.FOCUSED_BLOCK.insertIntoText('\n')

					elif len(event.unicode):
						Block.FOCUSED_BLOCK.insertIntoText(event.unicode)

			if event.type == pygame.MOUSEBUTTONDOWN:
				EventHandler.LAST_DRAG_POS = event.pos;
				for block in blockList:
					if block.isPointed(event.pos):
						block.acquireFocus()
						break
					Block.releaseFocus()
				EventHandler.IS_MOUSE_DOWN = True

			if event.type == pygame.MOUSEBUTTONUP:
				EventHandler.IS_MOUSE_DOWN = False

			if event.type == pygame.MOUSEMOTION:
				if EventHandler.IS_MOUSE_DOWN: Block.FOCUSED_BLOCK.posAddVector( vectorDiff(event.pos, EventHandler.LAST_DRAG_POS) )
				
				EventHandler.LAST_DRAG_POS = event.pos

			if event.type == pygame.QUIT:
				sys.exit()
		
