import sys

from pathlib import Path
from Source.Convert import Convert

class Pycon:
    def __init__(self):
        self.__filename = None
        self.__files = []
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
                sys.stderr.write('The command: {0} not has been processed\n'.format(command))

    def __GetListOfFilesPO(self, fromDirectory : Path) -> None:
        if fromDirectory.is_dir():
            files = fromDirectory.glob('**/*.po')
            for file in files:
                self.__files.append(file)
        else:
            sys.stderr.write('The path {0} not is directory\n'.format(fromDirectory))

    def __ProcessSingleFile(self):
        Convert().ConvertToXML(self.__filename)

    def __ProcessMultiplesFiles(self):
        pass

    @staticmethod
    def __VerifyThatFilenameIsPathValid(filename : Path):
        if not filename.exists():
            sys.stderr.write('The file {0} not exist\n'.format(filename))

if __name__ == '__main__':
    app = Pycon()