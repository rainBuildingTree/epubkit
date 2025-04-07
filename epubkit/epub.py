import os
import zipfile

class Epub:
    def __init__(self, file_path: str):
        # Validate the file path and assign
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        if not os.path.isfile(file_path):
            raise ValueError(f"Invalid file path: {file_path}. Expected a file.")
        if not file_path.endswith('.epub'):
            raise ValueError(f"Invalid file type: {file_path}. Expected .epub file.")
        self.file_path = file_path

        # Load file contents
        self.contents = {}
        try:
            with zipfile.ZipFile(file_path, 'r') as zin:
                for name in zin.namelist():
                    self.contents[name] = zin.read(name)
        except zipfile.BadZipFile:
            raise ValueError(f"Invalid EPUB file: {file_path}. Cannot open as zip.")