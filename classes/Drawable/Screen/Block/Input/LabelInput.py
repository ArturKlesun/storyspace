from classes.Constants import Constants
from classes.Drawable.AbstractDrawable import AbstractDrawable
from classes.Drawable.Screen.Block.Input.LabelInputHandler import LabelInputHandler
from classes.Drawable.Screen.Block.Input.Paragraph.Paragraph import Paragraph
from classes.Drawable.Screen.Dialog.IDialogCaller import IDialogCaller
from classes.Fp import overrides, vectorSum

class LabelInput(AbstractDrawable, IDialogCaller):

	KNOWN_LABELS = {'Гузно': {'name': 'Гузно', 'bgColor': [0,255,0], 'textColor': [255,0,0]},
					'Грёзы': {'name': 'Грёзы', 'bgColor': [0,0,255], 'textColor': [255,255,0]},
					'Грязь': {'name': 'Грязь', 'bgColor': [0,255,0], 'textColor': [255,0,255]},
					'Горечь': {'name': 'Горечь', 'bgColor': [0,0,0], 'textColor': [255,255,255]},
					'Гусь': {'name': 'Гусь', 'bgColor': [255,255,0], 'textColor': [0,0,255]}}

	def __init__(self, parentBlock):
		super(LabelInput, self).__init__(parentBlock)

		self.labelList = []
		self.pointer = 0
		self.setFocusedLabel({'name': '', 'bgColor': [0,255,0], 'textColor': [255,0,0]})
		self.matchedLabels = []

	@overrides(IDialogCaller)
	def receiveDialogResult(self, selectedOption):
		self.setFocusedLabel(self.__class__.KNOWN_LABELS[selectedOption].copy())

	def insertIntoText(self, substr):
		if ord(substr) == 13: return
		if self.getFocusedLabel() is None:
			self.labelList.append({'name': '', 'strength': 0, 'bgColor': [0,0,255], 'textColor': [255,255,255]})

		if substr == '+':
			self.changeLabelStrength(+1)
		elif substr == '-':
			self.changeLabelStrength(-1)
		else:
			self.getFocusedLabel()['name'] += substr
			self.updateDialog()

		self.recalcSurfaceBacursively()

	def getObjectState(self):
		return {'labelList': self.labelList}

	@overrides(AbstractDrawable)
	def setObjectState(self, labelList):
		if self.getRootParent().jsonStructureFormatVersion == Constants.PARAGRAPH_NOT_OBJECT_FORMAT_VERSION: # legacy
			for label in labelList:
				self.addLabel(label)
		else:
			for label in labelList['labelList']:
				self.addLabel(label)
		self.setPointer(0)
		self.deleteLabel() # потому что знаю =P

	@overrides(AbstractDrawable)
	def getChildList(self): return []

	def getFocusedLabel(self):
		return self.labelList[self.pointer] if self.pointer in range(0, len(self.labelList)) else None

	def setFocusedLabel(self, value: dict):
		if len(self.labelList) <= self.pointer:
			self.labelList.append(value)
		else:
			self.labelList[self.pointer] = value
		self.recalcSurfaceBacursively()

	def changeLabelStrength(self, n):
		if not 'strength' in self.getFocusedLabel(): self.getFocusedLabel().update({'strength': 0})
		self.getFocusedLabel()['strength'] += n
		self.__class__.KNOWN_LABELS.update({self.labelList[self.pointer]['name']: self.labelList[self.pointer]})

		if self.getRootParent().getDialog():
			self.getRootParent().getDialog().destroy()

	def addLabel(self, label: dict):
		self.movePointer(9999) # зарплату не платят =(
		self.setFocusedLabel(label)
		self.changeLabelStrength(0)

	def deleteLabel(self):
		if len(self.labelList) > 1:
			self.labelList.pop(0)

	def updateDialog(self):
		matchedLabels = [k for k,v in self.__class__.KNOWN_LABELS.items() if k.lower().startswith(self.getFocusedLabel()['name'].lower())]
		if len(matchedLabels):
			self.getRootParent().interceptDialog(self, {
					'pos': vectorSum(self.getAbsolutePos(), [0,self.getHeight()]),
					'options': matchedLabels,
					'width': self.getWidth()})
		else:
			if self.getRootParent().getDialog():
				self.getRootParent().getDialog().destroy()

	def movePointer(self, n):
		if self.pointer < len(self.labelList):
			self.__class__.KNOWN_LABELS.update({self.labelList[self.pointer]['name']: self.labelList[self.pointer]})
		self.setPointer(self.pointer + n)

	def setPointer(self, value):
		if value < 0: value = 0
		if value > len(self.labelList): value = len(self.labelList)
		self.pointer = value

		if self.getRootParent().getDialog() is not None:
			self.getRootParent().getDialog().destroy()
		self.recalcSurfaceBacursively()

	@overrides(AbstractDrawable)
	def recalcSurface(self):
		self.recalcSize()
		self.surface.fill([0,255,255])

		charInRowCount = self.getWidth() // Constants.CHAR_WIDTH
		spaceLeft = charInRowCount
		colIdx = 0
		rowIdx = 0
		for label in self.labelList:
			if spaceLeft <= len(label['name']) + 1:
				rowIdx += 1
				colIdx = 0
				spaceLeft = charInRowCount
			self.surface.blit(Constants.PROJECT_FONT.render(
				label['name'] + '|', 1,
				label['textColor'], label['bgColor']),
			[colIdx * Constants.CHAR_WIDTH,rowIdx * Constants.CHAR_HEIGHT])
			colIdx += len(label['name']) + 1
			spaceLeft -= len(label['name']) + 1

		# self.surface.blit(self.getParagraph().getSurface(), [0,0])

	@overrides(AbstractDrawable)
	def getFocusedChild(self):
		return None

	@overrides(AbstractDrawable)
	def makeHandler(self):
		return LabelInputHandler(self) # нда...

	@overrides(AbstractDrawable)
	def recalcSize(self):
		textLen = 0
		for label in self.labelList:
			textLen += len(label['name']) + 1
		self.size([self.getParent().calcTextfieldSize()[0], textLen // (self.getParent().calcTextfieldSize()[0] // Constants.CHAR_WIDTH) * Constants.CHAR_HEIGHT])

	@overrides(AbstractDrawable)
	def getDefaultSize(self):
		return [Constants.CHAR_WIDTH, Constants.CHAR_HEIGHT]

	# event handles

	def deleteBack(self): return self.deleteFromText(-1)
	def deleteNext(self): return self.deleteFromText(+1)

	def deleteFromText(self, n):
		if self.getFocusedLabel() is None:
			self.labelList.append({'name': '', 'strength': 0, 'bgColor': [0,0,255], 'textColor': [255,255,255]})
		if len(self.getFocusedLabel()['name']) > 0:
			self.getFocusedLabel()['name'] = self.getFocusedLabel()['name'][:-1]
		self.updateDialog()
		self.recalcSurfaceBacursively()