from pathlib import Path

class WriterDirectory:
    @staticmethod
    def CreateDirectory(_path : Path):
        if _path.exists():
            print('The path: "{}" already exist'.format(str(_path)))
        else:
            _path.mkdir()

    @staticmethod
    def ExistDirectory(_path: Path) -> bool:
        if _path.exists(): return True
        else: return False