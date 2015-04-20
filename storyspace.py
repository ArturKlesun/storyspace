#!/usr/bin/env python
# -*- coding: utf-8 -*-

from classes.Config import Config
from classes.Drawable.Screen.Screen import Screen
from classes.TimerHandler import TimerHandler

Config.getInstance()
eventHandler = Screen.getInstance().makeHandler()
timerHandler = TimerHandler(eventHandler)

while True:
	timerHandler.handleFrame()