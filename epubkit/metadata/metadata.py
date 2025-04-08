from .entry import MetaEntry
from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class Metadata:
    titles: List[MetaEntry] = field(default_factory=list)
    creators: List[MetaEntry] = field(default_factory=list)
    languages: List[MetaEntry] = field(default_factory=list)
    identifiers: List[MetaEntry] = field(default_factory=list)
    publishers: List[MetaEntry] = field(default_factory=list)
    dates: List[MetaEntry] = field(default_factory=list)
    descriptions: List[MetaEntry] = field(default_factory=list)
    subjects: List[MetaEntry] = field(default_factory=list)
    rights: List[MetaEntry] = field(default_factory=list)
    contributors: List[MetaEntry] = field(default_factory=list)

    meta: Dict[str, List[MetaEntry]] = field(default_factory=dict)