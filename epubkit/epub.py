import os
import zipfile

class Epub:
    def __init__(self, file_path: str):
        # Initialize Members
        self.file_path: str = None
        self.contents: dict = None

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

if __name__ == "__main__":
    try:
        epub = Epub("test.epub")
        print("EPUB file loaded successfully.")
        for name in epub.contents.keys():
            print(f"File: {name}")
    except Exception as e:
        print(f"Error: {e}")