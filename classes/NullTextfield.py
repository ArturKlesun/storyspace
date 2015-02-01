from classes.AbstractTextfield import AbstractTextfield
from classes.Fp import overrides

class NullTextfield(AbstractTextfield):

    @overrides(AbstractTextfield)
    def __init__(self):
        pass

    @overrides(AbstractTextfield)
    def movePointer(self, n):
        pass
    
    @overrides(AbstractTextfield)
    def movePar(self, n):
        pass

    @overrides(AbstractTextfield)
    def insertIntoText(self, substr):
        pass

    @overrides(AbstractTextfield)
    def deleteFromText(self, n):
        pass

    @overrides(AbstractTextfield)
    def scroll(self, n):
        pass
