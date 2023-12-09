import os
import sys
import json

dirPath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(dirPath, '..')))

json_file_path = os.path.join(dirPath, "..", "JSON")

FileDB = os.path.join(json_file_path,"movies.json") #va cambiata ogni volta che vuoi cambiare file

def generate_emb_upsert_commands(json_file_path):
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    commands = []
    index_counter = 0  # Contatore globale per il numero incrementale

    for table in data["tables"]:
        table_name = table["name"]

        for column in table["columns"]:
            field_name = column["name"]
            description = column["description"]

            # Creazione del comando emb.upsert
            command = f'emb.upsert([({index_counter}, {{"text": "{description}", "campo": "{field_name}", "tabella": "{table_name}"}})])'
            commands.append(command)

            # Incrementa il contatore globale
            index_counter += 1
    return commands

generated_commands = generate_emb_upsert_commands(FileDB)

# Stampa i comandi generati
for command in generated_commands:
    print(command)
