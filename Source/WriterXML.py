import xml.etree.ElementTree as ET

from pathlib import Path

from Source.WriterDirectory import WriterDirectory

class WriterXML (WriterDirectory):
    def __init__(self):
        self.__filename = str()
        self.__document = None
        self.__elementRoot = None
        self.__directoryOutput = Path('./Output/')

    def Write(self, translates : list):
        if not self.ExistDirectory(self.__directoryOutput):
            self.CreateDirectory(self.__directoryOutput)
        self.__elementRoot = ET.Element('LanguageInject')
        for translate in translates:
            element = ET.SubElement(self.__elementRoot, translate.key)
            element.text = translate.value

        self.__document = ET.ElementTree(self.__elementRoot)
        # Filename of Output, Encoding and Xml Declaration
        self.__document.write(self.__filename, 'UTF-8', True)
        self.__MoveFile()

    def __MoveFile(self):
        pathParent = self.__directoryOutput.parent
        pathFile = Path(pathParent / self.__filename)
        try:
            pathFile.rename(self.__directoryOutput / self.__filename)
        except FileExistsError:
            pathFile.replace(self.__directoryOutput)

    def SetFilename(self, _filename : str) -> None:
        self.__filename = _filename