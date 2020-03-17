import xml.etree.ElementTree as ET

from Source.Dictionary import Dictionary

class WriterXML:
    def __init__(self):
        self.__filename = str()
        self.__document = None

    def Write(self, translates : list):
        self.__document = ET.Element('LanguageInject')
        ET.dump(self.__document)