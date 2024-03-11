from jsonschema import validate
import json

def Request_validate(percorsoFile: str, schema: str) -> bool:
    json_data = json.load(open(percorsoFile))	
    json_schema = json.load(open(schema))
    try:
        validate(instance = json_data, schema = json_schema) #validate funzione interna di jsonschema
        return True
    except Exception as e:
        print(e)
        return False

if __name__ == "__main__":    
    percorsoFile = "ChatSQL/JSON/notCompliantFile.json"
    schema = "C:/Users/Marco/Desktop/swe/progetto/ChatSQL/ChatSQL/code/schema.json"

    print(Request_validate(percorsoFile, schema))