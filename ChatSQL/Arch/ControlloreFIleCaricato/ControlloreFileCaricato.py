from JSONSchemaAdapter import Request_validate


class ControlloreFileCaricato:
    def __init__(self, path):
        self.path = path

    def Request_validate(self) -> bool:
        pass
    
if __name__ == "__main__":
    percorsoFile = "ChatSQL/JSON/library.json"
    schema = "C:/Users/Marco/Desktop/swe/progetto/ChatSQL/ChatSQL/code/schema.json"

    print(Request_validate(percorsoFile, schema))