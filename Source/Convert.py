from pathlib import Path

class Dictionary:
    def __init__(self, _key : str, _value : str):
        self.key = _key
        self.value = _value

class Convert:
    def __init__(self):
        self.__buffer = list()
        self.__tags = list()
        self.__commentHead = str()

    def ConvertToXML(self, filename : Path):
        with filename.open() as file:
            self.__buffer = file.read()
            self.__buffer = self.__buffer.splitlines()
            file.close()
        self.__ExtractCommentOfHead()
        self.__DeletedEmptyLinesInBuffer()
        self.__DeletedCommentsInBuffer()
        self.__DeletedCharactersUnusedInBuffer()
        self.__MergeTagsSeparatedForNewLine()
        self.__CreateListOfTagsAndTranslates()

    def __ExtractCommentOfHead(self):
        allCommentHeadHasBeenExtracted = False
        while not allCommentHeadHasBeenExtracted:
            if self.__buffer[0].startswith('#'):
                self.__commentHead += self.__buffer[0]
                self.__buffer.pop(0)
            else: allCommentHeadHasBeenExtracted = True

    def __DeletedEmptyLinesInBuffer(self):
        index = 0
        for line in self.__buffer:
            if len(line) == 0:
                self.__buffer.pop(index)
            index += 1

    def __DeletedCommentsInBuffer(self):
        index = 0
        while index < len(self.__buffer):
            if self.__buffer[index].startswith('#'):
                self.__buffer.pop(index)
                continue
            index += 1

    def __DeletedCharactersUnusedInBuffer(self):
        for i in range(len(self.__buffer)):
            self.__buffer[i] = self.__DeletedCharactersInString(self.__buffer[i], '"')

    def __MergeTagsSeparatedForNewLine(self):
        index = 0
        for line in self.__buffer:
            if line.find('msgid ', 0, len('msgid ')) != -1:
                while index + 1 < len(self.__buffer):
                    if self.__buffer[index + 1].find('msgstr ', 0, len('msgstr ')) == -1:
                        line += self.__buffer[index + 1]
                        self.__buffer.pop(index + 1)
                    else:
                        self.__buffer[index] = line
                        break
            elif line.find('msgstr ', 0, len('msgstr ')) != -1:
                while index + 1 < len(self.__buffer):
                    if self.__buffer[index + 1].find('msgid ', 0, len('msgid ')) == -1:
                        line += self.__buffer[index + 1]
                        self.__buffer.pop(index + 1)
                    else:
                        self.__buffer[index] = line
                        break
            index += 1

    def __CreateListOfTagsAndTranslates(self):
        key , value = str(), str()
        for line in self.__buffer:
            if line.find('msgid ', 0, len('msgid ')) != -1:
                key += line

    @staticmethod
    def __DeletedCharactersInString(stringBuffer : str, character : str) -> str:
        return stringBuffer.replace(character, '')