import os
import json

def generateEmbeddingUpsert(jsonFileName):
    with open(jsonFileName, 'r') as file:
        data = json.load(file)

    commands = []
    index_counter = 0 # Contatore globale per il numero incrementale

    for table in data["tables"]:
        table_name = table["name"]

        for column in table["columns"]:
            field_name = column["name"]
            type = column["type"]
            references = column["references"]
            description = column["description"]

            # Creazione del comando emb.upsert
            command = f'emb.upsert([({index_counter}, {{"tabella": "{table_name}", "campo": "{field_name}", "tipo": "{type}", "references": "{references}", "description": "{description}"}})])'

            commands.append(command)

            # Incrementa il contatore globale
            index_counter += 1

    return commands

if __name__ == "__main__":
    dir_path = os.path.dirname(os.path.realpath(__file__))
    json_file_path = os.path.join(dir_path, "..", "JSON")
    jsonFileName = os.path.join(json_file_path, "watches.json") # va cambiata ogni volta che vuoi cambiare file

    generated_commands = generateEmbeddingUpsert(jsonFileName)
    for command in generated_commands:
        print(command)