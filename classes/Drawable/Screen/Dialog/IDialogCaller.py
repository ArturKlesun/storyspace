from abc import ABCMeta, abstractmethod


class IDialogCaller(metaclass=ABCMeta):

	@abstractmethod
	def receiveDialogResult(self):
		raise NotImplementedError("Please Implement this method for " + self.__class__.__name__)
