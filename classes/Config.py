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
		fileObj = open('asd.json', 'w')
		fileContent= [];
		for block in classes.Drawable.Screen.Screen.getInstance().getChildBlockList():
			fileContent.append(block.getObjectState())
		fileObj.write(json.dumps(fileContent, ensure_ascii=False, indent=4).encode('utf8'))
		fileObj.close()

	def openFile(self):
		fileObj = open('asd.json', 'r')
		classes.Drawable.Screen.Screen.getInstance().reconstruct( json.loads(fileObj.read()) )
		fileObj.close()