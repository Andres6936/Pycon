import xml.etree.ElementTree as ET

class WriterXML:
    def __init__(self):
        self.__filename = str()
        self.__document = None
        self.__elementRoot = None

    def Write(self, translates : list):
        self.__elementRoot = ET.Element('LanguageInject')
        for translate in translates:
            element = ET.SubElement(self.__elementRoot, translate.key)
            element.text = translate.value

        self.__document = ET.ElementTree(self.__elementRoot)
        # Filename of Output, Encoding and Xml Declaration
        self.__document.write('Out.xml', 'UTF-8', True)