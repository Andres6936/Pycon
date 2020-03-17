import re
import random

from pathlib import Path

from Source.Dictionary import Dictionary
from Source.WriterXML import WriterXML

class Convert (WriterXML):
    def __init__(self):
        super().__init__()
        self.__tags = list()
        self.__buffer = list()
        self.__translates = list()
        self.__license = str()
        self.__filename = str()
        self.__commentHead = str()
        self.__translators = str()
        self.__metadataHead = str()

    def ConvertToXML(self, filename : Path):
        with filename.open() as file:
            self.__buffer = file.read()
            self.__buffer = self.__buffer.splitlines()
            file.close()
        self.__ExtractCommentOfHead()
        self.__ExtractPossibleFilename()
        self.__DeletedEmptyLinesInBuffer()
        self.__DeletedCommentsInBuffer()
        self.__DeletedCharactersUnusedInBuffer()
        self.__DeletedEmptyLinesInBuffer()
        self.__MergeTagsSeparatedForNewLine()
        self.__ExtractMetadataOfHead()
        self.__ExtractPossibleFilenameOfMetadata()
        self.__ExtractLicense()
        self.__ExtractTranslators()
        self.__CreateListOfTranslates()
        self.__FormatTagsInTranslates()
        self.__FormatValueInTranslates()
        self.SetFilename(self.__filename)
        self.Write(self.__translates)

    def __ExtractCommentOfHead(self):
        allCommentHeadHasBeenExtracted = False
        while not allCommentHeadHasBeenExtracted:
            if self.__buffer[0].startswith('#'):
                self.__commentHead += self.__buffer[0]
                self.__buffer.pop(0)
            else: allCommentHeadHasBeenExtracted = True

    def __ExtractPossibleFilename(self) -> None:
        # For avoid unnecessary calculus
        if len(self.__commentHead) == 0:
            self.__GenerateRandomFilename()
            return

        pattern = re.compile(r'\w+\s([Tt])ranslation\sfor\s')
        result = pattern.search(self.__commentHead)
        if result:
            section = result.string[result.start():result.end()]
            pattern = re.compile(r'\w+')
            result = pattern.search(section)
            if result:
                self.__filename = result.string[result.start():result.end()] + '.xml'
                return
        else:
            pattern = re.compile(r'([Tt])ranslation\sof\s(\S+)\sto\s\w+')
            result = pattern.search(self.__commentHead)
            if result:
                section = result.string[result.start():result.end()]
                section = section.split(' ')
                self.__filename = section[-1] + '.xml'
                return
        # Can't determine an possible filename, generate an filename random
        self.__GenerateRandomFilename()

    def __GenerateRandomFilename(self):
        self.__filename = 'Output{}.xml'.format(random.randint(1, 6936))

    def __ExtractPossibleFilenameOfMetadata(self):
        # If the filename have an name distinct of Output.xml, mean
        # that was possible determine an valid filename, otherwise
        # need determine the filename in this function
        if self.__filename.find('Output', 0, len('Output')) != -1:
            pattern = re.compile(r'Language-Team\s(\S+)')
            result = pattern.search(self.__metadataHead)
            if result:
                filename = result.string[result.start():result.end()]
                filename = filename.split(' ')
                self.__filename = filename[-1] + '.xml'
                return

    def __ExtractMetadataOfHead(self):
        # Deleted the first msgid without use
        self.__buffer.pop(0)
        self.__metadataHead = self.__buffer.pop(0)

    def __ExtractLicense(self):
        # The license is divided in three parts
        for i in range(3):
            self.__buffer.pop(0)
            self.__license += self.__buffer.pop(0)

    def __ExtractTranslators(self):
        self.__buffer.pop(0)
        self.__translators += self.__buffer.pop(0)

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
            self.__buffer[i] = self.__DeletedCharactersInString(self.__buffer[i], "'")
            self.__buffer[i] = self.__DeletedCharactersInString(self.__buffer[i], '.')
            self.__buffer[i] = self.__DeletedCharactersInString(self.__buffer[i], ';')
            self.__buffer[i] = self.__DeletedCharactersInString(self.__buffer[i], '?')
            self.__buffer[i] = self.__DeletedCharactersInString(self.__buffer[i], '_')
            self.__buffer[i] = self.__DeletedCharactersInString(self.__buffer[i], '|')
            self.__buffer[i] = self.__DeletedCharactersInString(self.__buffer[i], '(')
            self.__buffer[i] = self.__DeletedCharactersInString(self.__buffer[i], ')')
            self.__buffer[i] = self.__DeletedCharactersInString(self.__buffer[i], ':')
            self.__buffer[i] = self.__DeletedCharactersInString(self.__buffer[i], '%')
            self.__buffer[i] = self.__DeletedCharactersInString(self.__buffer[i], '--')
            self.__buffer[i] = self.__DeletedCharactersInString(self.__buffer[i], '\\n')

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
            translate.key = translate.key.replace('msgid ', '')
            keyTag = self.__ExtractNameOfTag(translate.key)
            translate.key = keyTag

    def __FormatValueInTranslates(self):
        for translate in self.__translates:
            translate.value = translate.value.replace('msgstr ', '')

    def __ExtractNameOfTag(self, _string : str) -> str:
        listOfWords = list()

        if self.__HaveXWords(4, _string):
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
        return _string.count(' ') >= _x - 1

    @staticmethod
    def __ExtractXWordMoreGreater(_x : int, _string : str) -> list:
        listOfWords = _string.split(' ')

        while len(listOfWords) > _x:
            index = len(listOfWords) - 1
            # Set that the word more shorter is the last of list
            lengthWordMoreShorter = len(listOfWords[index])
            indexWordMoreShorter = index
            # Decrease in 1 for avoid pass for the word above looking
            index -= 1
            while index > 0:
                lengthOfThisWord = len(listOfWords[index])
                if lengthOfThisWord < lengthWordMoreShorter:
                    lengthWordMoreShorter = lengthOfThisWord
                    indexWordMoreShorter = index
                    index -= 1
                else:
                    index -= 1

            # Deleted the word more shorter
            listOfWords.pop(indexWordMoreShorter)

        return listOfWords


    @staticmethod
    def __DeletedCharactersInString(stringBuffer : str, character : str) -> str:
        return stringBuffer.replace(character, '')