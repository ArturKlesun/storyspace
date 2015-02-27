#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tkinter import Tk
import pygame

from classes.ClassImporter import ClassImporter
from classes.Clipboard import Clipboard

ClassImporter.importAllClasses()

from classes.Config import Config
from classes.Drawable.Screen.Screen import Screen
from classes.TimerHandler import TimerHandler

Config.getInstance()
eventHandler = Screen.getInstance().getEventHandler()
timerHandler = TimerHandler(eventHandler)

while 1:
	timerHandler.handleFrame()