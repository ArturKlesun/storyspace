import json

import pygame

import classes
from classes.Constants import Constants


class Config(object):

	FILE_NAME = 'config.json'

	instance = None

	params = {}
	contentFolderPath = 'guzno'

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

		self.contentFolderPath = self.params['contentFolderPath']
		self.imageDict = {}

	def getImageByName(self, imageName):
		imgPath = self.contentFolderPath + 'images/' + imageName
		if imageName not in self.imageDict:
			try:
				img = pygame.image.load(imgPath)
				self.imageDict[imageName] = img
			except pygame.error as err:
				self.imageDict[imageName] = Constants.PROJECT_FONT.render('invalid file ' + imageName, True, [255,0,0])

		return self.imageDict[imageName]

	def saveToFile(self):
		fileObj = open(self.contentFolderPath + 'storyspaceContent.json', 'w', encoding='utf-8')
		fileContent= [];
		for block in classes.Drawable.Screen.Screen.Screen.getInstance().getChildBlockList():
			fileContent.append(block.getObjectState())
		fileObj.write(json.dumps(fileContent, ensure_ascii=False, indent=2))
		fileObj.close()

	def readDataFromFile(self):
		fileObj = open(self.contentFolderPath + 'storyspaceContent.json', 'r', encoding='utf-8')
		huj = fileObj.read()
		fileObj.close()
		data = json.loads(huj)
		return data
