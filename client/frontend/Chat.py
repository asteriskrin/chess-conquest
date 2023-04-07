'''
Chat class
'''

import string


class Chat:
    def __init__(self, personName: string, message: string):
        self.personName = personName
        self.message = message

    def getPersonName(self):
        return self.personName

    def getMessage(self):
        return self.message