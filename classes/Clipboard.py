#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import Tk
from sys import platform as _platform
import pygame
from pygame.constants import SCRAP_TEXT

if _platform == "linux" or _platform == "linux2":
	pass
# elif _platform == "win32" or _platform == "win64":
	# import win32clipboard
	# Windows...


class Clipboard(object):

	tinker = None

	@staticmethod
	def add(str): # TODO: for linux adds some bad data, that breaks program (breaks even editor), but for windows worked
		if _platform == "win32" or _platform == "win64":
			r = Tk()
			r.withdraw()
			r.clipboard_clear()
			r.clipboard_append('i can has clipboardz?')
			r.destroy()

	@staticmethod
	def get():
		r = Tk()
		r.withdraw()
		returnValue = r.selection_get(selection = "CLIPBOARD")
		r.destroy()

		return returnValue if returnValue else ''