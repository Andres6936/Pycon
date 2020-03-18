from pathlib import Path

class WriterDirectory:
    @staticmethod
    def CreateDirectory(_path : Path):
        if _path.exists():
            print('The path: "{}" already exist'.format(str(_path)))
        else:
            _path.mkdir()