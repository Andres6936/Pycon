from pathlib import Path

class Dictionary:
    def __init__(self, _key : str, _value : str):
        self.key = _key
        self.value = _value

class Convert:
    def __init__(self):
        self.__buffer = list()
        self.__tags = list()
        self.__translates = list()
        self.__commentHead = str()
        self.__metadataHead = str()

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
        self.__ExtractMetadataOfHead()
        self.__CreateListOfTranslates()
        self.__FormatTagsInTranslates()

    def __ExtractCommentOfHead(self):
        allCommentHeadHasBeenExtracted = False
        while not allCommentHeadHasBeenExtracted:
            if self.__buffer[0].startswith('#'):
                self.__commentHead += self.__buffer[0]
                self.__buffer.pop(0)
            else: allCommentHeadHasBeenExtracted = True

    def __ExtractMetadataOfHead(self):
        # Deleted the first msgid without use
        self.__buffer.pop(0)
        self.__metadataHead = self.__buffer.pop(0)

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

    def __CreateListOfTranslates(self):
        key , value = str(), str()
        for line in self.__buffer:
            if line.find('msgid ', 0, len('msgid ')) != -1:
                key += line
            elif line.find('msgstr ', 0, len('msgstr ')) != -1:
                value += line
                self.__translates.append(Dictionary(key, value))
                key, value = str(), str()

    def __FormatTagsInTranslates(self):
        for translate in self.__translates:
            keyTag = self.__ExtractNameOfTag(translate.key)
            translate.key = keyTag

    def __ExtractNameOfTag(self, _string : str) -> str:
        listOfWords = list()
        if self.__HaveXWords(5, _string):
            listOfWords = self.__ExtractXWordMoreGreater(5, _string)
        elif self.__HaveXWords(4, _string):
            listOfWords = self.__ExtractXWordMoreGreater(4, _string)
        elif self.__HaveXWords(3, _string):
            listOfWords = self.__ExtractXWordMoreGreater(3, _string)
        elif self.__HaveXWords(2, _string):
            listOfWords = self.__ExtractXWordMoreGreater(2, _string)
        # Only exist an word in this string
        else: listOfWords.append(_string)

        self.__CapitalizeWords(listOfWords)
        nameOfTag = self.__MergeWords(listOfWords)
        return nameOfTag

    @staticmethod
    def __CapitalizeWords(_words : list) -> None:
        index = 0
        while index < len(_words):
            _words[index] = _words[index].capitalize()
            index += 1

    @staticmethod
    def __MergeWords(_words : list) -> str:
        mergeWord = str()
        for word in _words:
            mergeWord += word

        return mergeWord

    @staticmethod
    def __HaveXWords( _x : int, _string : str) -> bool:
        return _string.count(' ') >= _x

    @staticmethod
    def __ExtractXWordMoreGreater(_x : int, _string : str) -> list:
        listOfWordsGreat = list()
        listOfWords = _string.split(' ')

        for i in range(_x):
            # Set that the word more great is the first of list
            lengthOfWordMoreGreat = len(listOfWords[0])
            index = 1
            indexWordMoreGreater = 1
            while index < len(listOfWords):
                if len(listOfWords[index]) > lengthOfWordMoreGreat:
                    lengthOfWordMoreGreat = len(listOfWords[index])
                    indexWordMoreGreater = index
                    index += 1
                else: index += 1

            # Added the word to the list of words greater
            listOfWordsGreat.append(listOfWords[indexWordMoreGreater])
            # Deleted the word of the list for avoid counter again
            listOfWords.pop(indexWordMoreGreater)

        return listOfWordsGreat


    @staticmethod
    def __DeletedCharactersInString(stringBuffer : str, character : str) -> str:
        return stringBuffer.replace(character, '')