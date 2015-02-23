#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import Tk
from sys import platform as _platform
if _platform == "linux" or _platform == "linux2":
	from gi.repository import Gtk as gtk
elif _platform == "win32" or _platform == "win64":
	import win32clipboard
	# Windows...


class Clipboard(object):

	@staticmethod
	def add(str): # TODO: for linux adds some bad data, that breaks program (breaks even editor), but for windows works
		r = Tk()
		r.withdraw()
		r.clipboard_clear()
		r.clipboard_append('i can has clipboardz?')
		r.destroy()

	@staticmethod
	def get():
		returnValue = ''
		if _platform == "linux" or _platform == "linux2":
			cb = gtk.clipboard_get()
			returnValue = cb.wait_for_text()   
		elif _platform == "win32" or _platform == "win64":
			win32clipboard.OpenClipboard()
			winString = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
			returnValue = winString
			win32clipboard.CloseClipboard()
		else:
			# sorry, Mac
			returnValue = ''

		return returnValue if returnValue else ''