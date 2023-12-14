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

            # Create the emb.upsert command
            dictionary = {"table": table_name, "field": field_name, "type": type, "references": references, "description": description}
            command = (index_counter, dictionary)

            commands.append(command)

            index_counter += 1

    return commands

if __name__ == "__main__":
    dir_path = os.path.dirname(os.path.realpath(__file__))
    json_file_path = os.path.join(dir_path, "..", "JSON")
    jsonFileName = os.path.join(json_file_path, "watches.json")

    generated_commands = generateEmbeddingUpsert(jsonFileName)

    for command in generated_commands:
        #print(command)
        dictionary = command[1]
        #print(dictionary["table"])
        print(f"Table name: {dictionary['table']}")
        print(f"Field name: {dictionary['field']}")
        print(f"Field type: {dictionary['type']}")
        print(f"References: {dictionary['references']}")
        print(f"Description: {dictionary['description']}\n")

    index_to_print = 1

    # Check if the index is valid
    if 0 <= index_to_print < len(generated_commands):
        selected_command = generated_commands[index_to_print]
        selected_dictionary = selected_command[1]

        print(f"Selected Command at Index {index_to_print}:")
        print(f"Table name: {selected_dictionary['table']}")
        print(f"Field name: {selected_dictionary['field']}")
        print(f"Field type: {selected_dictionary['type']}")
        print(f"References: {selected_dictionary['references']}")
        print(f"Description: {selected_dictionary['description']}\n")
    else:
        print("Invalid index. Please enter a valid index.")
