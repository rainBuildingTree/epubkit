from dataclasses import dataclass
from typing import Dict

@dataclass
class ManifestEntry:
    id: str
    href: str
    media_type: str
    properties: Dict[str, str]