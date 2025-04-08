import os
import zipfile
from .metadata._extractor import _MetadataExtractor
from .manifest._extractor import _ManifestExtractor
from .errors import InvalidEpubError
from xml.etree import ElementTree as ET

class _Reader:
    def __init__(self, path):
        # 1. Load File Contents
        file_contents = {}
        with zipfile.ZipFile(path, 'r') as zin:
            for name in zin.namelist():
                file_contents[name] = zin.read(name)
        
        # 2. Check Minetype
        minetype_bytes = file_contents.get('mimetype')
        if minetype_bytes is None:
            raise InvalidEpubError("The EPUB file is missing the 'mimetype' file.")
        content = minetype_bytes.decode('utf-8').strip()
        if content != 'application/epub+zip':
            raise InvalidEpubError(f"Invalid mimetype content: expected 'application/epub+zip', found '{content}'.")
        
        # 3. Check Container
        container_path = 'META-INF/container.xml'
        if container_path not in file_contents:
            raise InvalidEpubError("The 'META-INF/container.xml' file is missing or could not be read.")
        container_content = file_contents[container_path].decode('utf-8')
        container_tree = ET.fromstring(container_content)
        container_namespace = {'container': 'urn:oasis:names:tc:opendocument:xmlns:container'}
        rootfile = container_tree.find('.//container:rootfile', container_namespace)
        if rootfile is None:
            raise InvalidEpubError("The OPF file path defined in 'container.xml' is missing or invalid.")
        
        # 4. Check OPF
        opf_path = rootfile.get('full-path')
        if opf_path is None:
            raise InvalidEpubError("The OPF file path defined in 'container.xml' is missing or invalid.")
        
        # 5. Load Version
        try:
            xml = file_contents[opf_path].decode("utf-8")
            root = ET.fromstring(xml)
            version = root.get("version")
            if not version:
                raise InvalidEpubError("EPUB version attribute not found in OPF package element")
            self.version = version
        except Exception as e:
            raise InvalidEpubError("Failed to parse OPF for version") from e
        
        # 6. Load Metadata
        self.metadata = _MetadataExtractor(opf_path, file_contents).extract()

        # 7. Load Manifest
        self.manifest = _ManifestExtractor(opf_path, file_contents).extract()
        



        
        

