from ._reader import _Reader
from ._builder import _Builder
from .manifest import Manifest
from .metadata import Metadata
from .spine import Spine
from .toc import TOC

class Epub:
    def __init__(self, path):
        reader = _Reader(path)
        self.version: str = reader.version
        self.metadata: Metadata = reader.metadata
        self.manifest: Manifest = reader.manifest
        self.spine: Spine = reader.get_spine()
        self.toc: TOC = reader.get_toc()