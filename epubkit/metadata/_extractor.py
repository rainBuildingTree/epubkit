from .metadata import Metadata
from .entry import MetaEntry
from ..errors import InvalidEpubError
from xml.etree import ElementTree as ET

class _MetadataExtractor:
    def __init__(self, opf_path: str, file_contents: dict[str, bytes]):
        self.opf_path = opf_path
        self.file_contents = file_contents
    
    def extract(self) -> Metadata:
        if self.opf_path not in self.file_contents:
            raise InvalidEpubError(f"OPF file not found at path: {self.opf_path}")
        
        try:
            xml_content = self.file_contents[self.opf_path].decode('utf-8')
            tree = ET.fromstring(xml_content)
        except Exception as e:
            raise InvalidEpubError("Failed to parse OPF XML") from e
        
        namespace = {
            'opf': 'http://www.idpf.org/2007/opf',
            'dc': 'http://purl.org/dc/elements/1.1/'
        }

        metadata_elements = tree.find("opf:metadata", namespace)
        if metadata_elements is None:
            raise InvalidEpubError("No <metadata> section found in OPF.")
        
        def extract_all(tag: str) -> list[str]:
            return [
                MetaEntry(element.text.strip(), dict(element.attrib))
                for element in metadata_elements.findall(f"dc:{tag}", namespace)
                if element.text and element.text.strip()
            ]
        
        titles = extract_all("title")
        creators = extract_all("creator")
        languages = extract_all("language")
        identifiers = extract_all("identifier")
        publishers = extract_all("publisher")
        dates = extract_all("date")
        descriptions = extract_all("description")
        subjects = extract_all("subject")
        rights = extract_all("rights")
        contributors = extract_all("contributor")

        meta_dict: dict[str, list[MetaEntry]] = {}

        for meta in metadata_elements.findall("opf:meta", namespace):
            attrib = dict(meta.attrib)
            key = attrib.get("property") or attrib.get("name")
            if not key:
                continue

            value = attrib.get("content") or (meta.text.strip() if meta.text else "")
            entry = MetaEntry(value, attrib)
            meta_dict.setdefault(key, []).append(entry)
        
        return Metadata(
            titles=titles,
            creators=creators,
            languages=languages,
            identifiers=identifiers,
            publishers=publishers,
            dates=dates,
            descriptions=descriptions,
            subjects=subjects,
            rights=rights,
            contributors=contributors,
            meta=meta_dict,
        )