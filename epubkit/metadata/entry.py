class MetaEntry:
    def __init__(self, value: str, attributes: dict[str, str]):
        self.value = value
        self.attributes = attributes

    def __repr__(self):
        return f"MetaEntry(value={self.value!r}, attributes={self.attributes})"