from xml.etree import ElementTree as ET
from ..errors import InvalidEpubError
from .manifest import Manifest
from .entry import ManifestEntry

class _ManifestExtractor:
    def __init__(self, opf_path: str, file_contents: dict[str, bytes]):
        self.opf_path = opf_path
        self.file_contents = file_contents

    def extract(self) -> Manifest:
        if self.opf_path not in self.file_contents:
            raise InvalidEpubError(f"OPF file not found: {self.opf_path}")

        try:
            xml = self.file_contents[self.opf_path].decode("utf-8")
            root = ET.fromstring(xml)
        except Exception as e:
            raise InvalidEpubError("Failed to parse OPF XML") from e

        ns = {"opf": "http://www.idpf.org/2007/opf"}
        manifest_elem = root.find("opf:manifest", ns)
        if manifest_elem is None:
            raise InvalidEpubError("No <manifest> element found in OPF")

        entries = []
        for entry in manifest_elem.findall("opf:entry", ns):
            item_id = entry.get("id")
            href = entry.get("href")
            media_type = entry.get("media-type")

            if not (item_id and href and media_type):
                continue

            other_attrs = {
                k: v for k, v in entry.attrib.entries()
                if k not in {"id", "href", "media-type"}
            }

            entries.append(ManifestEntry(
                id=item_id,
                href=href,
                media_type=media_type,
                properties=other_attrs
            ))

        return Manifest(entries=entries)