import os
from utils import generateEmbeddingUpsert

if __name__ == "__main__":
    dir_path = os.path.dirname(os.path.realpath(__file__))
    json_file_path = os.path.join(dir_path, "..", "JSON")
    jsonFileName = os.path.join(json_file_path, "movies.json")

    generated_commands = generateEmbeddingUpsert(jsonFileName)

    for command in generated_commands:
        #print(command)
        dictionary = command[1]
        #print(dictionary["table"])
        print(f"Table name: {dictionary['table']}")
        print(f"Table description: {dictionary['table-description']}")
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
        print(f"Table description: {selected_dictionary['table-description']}")
        print(f"Field name: {selected_dictionary['field']}")
        print(f"Field type: {selected_dictionary['type']}")
        print(f"References: {selected_dictionary['references']}")
        print(f"Description: {selected_dictionary['description']}\n")
    else:
        print("Invalid index. Please enter a valid index.")
