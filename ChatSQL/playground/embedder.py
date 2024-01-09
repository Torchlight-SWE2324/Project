import logging
import os
import re
import threading

from txtai import Embeddings
from utils import loading_animation, generateEmbeddingUpsert

def emb(jsonFile):
    generated_commands = generateEmbeddingUpsert(jsonFile)
    logging.getLogger("transformers.modeling_utils").setLevel(logging.ERROR)

    # Start loading animation in a separate thread
    loading_thread = threading.Thread(target=loading_animation, args=(len(generated_commands) * 0.2,))
    loading_thread.start()

    # Initialize the Embeddings module with the specified model
    emb = Embeddings({"path": "sentence-transformers/stsb-roberta-large", "content": True})

    # Upsert the data into the txtai Embeddings
    for command in generated_commands:
        try:
            cmd = str(command)
            emb.upsert([cmd])
        except Exception as e:
            print(f"Error during upsert: {e}")

    # Wait for the loading animation thread to finish
    loading_thread.join()

    while True:
        user_query = input("\nEnter your query (type 'exit' to quit): ")

        if user_query.lower() == 'exit':
            break

        results = emb.search(f"select score,text,table,table-description,field,type,references,description from txtai where similar('{user_query}') limit 3")

        table_fields = {}

        print("\n\033[1mSCORE FOR DEBUGGING ONLY\033[0m")
        for result in results:
            print(f"Score: {result['score']}")

            text = result['text']
            match = re.search(r"\((\d+),", text)

            if match:
                id_value = int(match.group(1))
                table_name = generated_commands[id_value][1]["table"]
                field_name = generated_commands[id_value][1]["field"]

                # Add the field to the dictionary for the corresponding table
                if table_name in table_fields:
                    table_fields[table_name].append(field_name)
                else:
                    table_fields[table_name] = [field_name]

        # Print the result in the desired format
        print("\nThe database contains the following tables:")
        for table, fields in table_fields.items():
            field_str = ', '.join([f"'{field}'" for field in fields])
            print(f"'{table}' with fields {field_str};")
        

        show_message = False
        messages = []

        for command_result in results:
            command_id = int(re.search(r"\((\d+),", command_result['text']).group(1))
            references_value = generated_commands[command_id][1]["references"]

            if references_value:
                table_name = generated_commands[command_id][1]["table"]
                field_name = generated_commands[command_id][1]["field"]
                messages.append(f"'{table_name}.{field_name}' references '{references_value}';")

        # Check if there are messages to show
        if messages:
            show_message = True
            print("\nThe database contains the following relationships:")

        # Print messages if show_message is True
        for message in messages:
            print(message)

        """# Optionally, print a generic message if no messages were found
        if not show_message:
            print("No reference values found.")"""

        print(f"\nGenerate the SQL query equivalent to: {user_query}\n")


if __name__ == "__main__":
    dir_path = os.path.dirname(os.path.realpath(__file__))
    json_file_path = os.path.join(dir_path, "..", "JSON")
    jsonFileName = os.path.join(json_file_path, "movies.json") # Change this to the JSON file you want to use
    emb(jsonFileName)
