import sys
import logging

from pathlib import Path
from Source.Convert import Convert

class Pycon:
    def __init__(self):
        self.__filename = None
        self.__files = []
        self.__logger = logging.getLogger('Pycon')
        self.__ProcessCommandLineArguments()
        self.__ProcessSingleFile()
        self.__ProcessMultiplesFiles()

    def __ProcessCommandLineArguments(self) -> None:
        commandLineArguments = sys.argv
        # Avoid added the name of file as first parameter
        commandLineArguments.pop(0)
        for command in commandLineArguments:
            if command.find('filename', 0, len('filename')) != -1:
                command = command.split('=')
                self.__filename = Path(command[-1])
                self.__VerifyThatFilenameIsPathValid(self.__filename)
            elif command.find('directory', 0, len('directory')) != -1:
                command = command.split('=')
                directory = Path(command[-1])
                self.__GetListOfFilesPO(directory)
            else:
                message = 'The command: {0} not has been processed'.format(command)
                self.__logger.error(message)

    def __GetListOfFilesPO(self, fromDirectory : Path) -> None:
        if fromDirectory.is_dir():
            files = fromDirectory.glob('**/*.po')
            for file in files:
                self.__files.append(file)
        else:
            message = 'The path {0} not is directory'.format(fromDirectory)
            self.__logger.error(message)

    def __ProcessSingleFile(self):
        Convert().ConvertToXML(self.__filename)

    def __ProcessMultiplesFiles(self):
        for file in self.__files:
            Convert().ConvertToXML(file)

    @staticmethod
    def __VerifyThatFilenameIsPathValid(filename : Path):
        if not filename.exists():
            message = 'The file {0} not exist\n'.format(filename)
            logging.getLogger('Pycon').error(message)

if __name__ == '__main__':
    app = Pycon()