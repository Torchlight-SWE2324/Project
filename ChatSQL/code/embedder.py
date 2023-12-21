import os
import re
import threading
import logging

from txtai import Embeddings
from utils import loading_animation, generateEmbeddingUpsert

def emb(jsonFile):
    generated_commands = generateEmbeddingUpsert(jsonFile)
    logging.getLogger("transformers.modeling_utils").setLevel(logging.ERROR)

    # Start loading animation in a separate thread
    loading_thread = threading.Thread(target=loading_animation, args=(len(generated_commands) * 0.2,))
    loading_thread.start()

    # Initialize the Embeddings module with the specified model
    emb = Embeddings({"path": "roberta-base", "content": True})

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

        for result in results:
            print(f"\nScore: {result['score']}")
            
            text = result['text']
            match = re.search(r"\((\d+),", text)

            if match:
                id_value = int(match.group(1))
                print("ID:", id_value)

                # Access specific data from generated_commands using the ID
                print("Field name: " + generated_commands[id_value][1]["field"])
                print("Field type: " + generated_commands[id_value][1]["type"])
                print("Table name: " + generated_commands[id_value][1]["table"])
                references_value = generated_commands[id_value][1]["references"]
                print("Table description: " + generated_commands[id_value][1]["table-description"]) #ADDED
                print("References: " + str(references_value) if references_value is not None else "References: None")
                print("Field description: " + generated_commands[id_value][1]["description"])

            else:
                print("ID not found in the given text.")

if __name__ == "__main__":
    dir_path = os.path.dirname(os.path.realpath(__file__))
    json_file_path = os.path.join(dir_path, "..", "JSON")
    jsonFileName = os.path.join(json_file_path, "movies.json")  # Change this to the JSON file you want to use
    emb(jsonFileName)
