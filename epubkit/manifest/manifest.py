from dataclasses import dataclass, field
from .entry import ManifestEntry
from typing import List

@dataclass
class Manifest:
    entries: List[ManifestEntry] = field(default_factory=list)

    def get_item_by_id(self, entry_id: str) -> ManifestEntry | None:
        for entry in self.entries:
            if entry.id == entry_id:
                return entry
        return None