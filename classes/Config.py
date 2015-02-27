import json

import pygame

import classes


class Config(object):

	FILE_NAME = 'config.json'

	instance = None

	params = {}
	contentFilePath = 'guzno'

	@staticmethod
	def getInstance():
		if Config.instance is None:
			Config.instance = Config()
		return Config.instance

	def __init__(self):
		pygame.init()
		pygame.key.set_repeat(150, 5)

		configFile = open(Config.FILE_NAME, 'r')
		self.params = json.loads(configFile.read())
		configFile.close()

		self.contentFilePath = self.params['contentFilePath']

	def saveToFile(self):
		fileObj = open(self.contentFilePath, 'w')
		fileContent= [];
		for block in classes.Drawable.Screen.Screen.Screen.getInstance().getChildBlockList():
			fileContent.append(block.getObjectState())
		fileObj.write(json.dumps(fileContent, ensure_ascii=False, indent=2))
		fileObj.close()

	def readDataFromFile(self):
		fileObj = open(self.contentFilePath, 'r', encoding='utf-8')
		huj = fileObj.read()
		fileObj.close()
		data = json.loads(huj)
		return data
