import os
from txtai import Embeddings
from fromJsonToEmb import generateEmbeddingUpsert

def emb(jsonFile):
    generated_commands = generateEmbeddingUpsert(jsonFile)
                                                 
    # Inizializza il modulo Embeddings con il modello specificato
    emb = Embeddings({"path": "efederici/sentence-BERTino", "content": True})

    # Utilizza i comandi generati dinamicamente per emb.upsert
    for command in generated_commands:
        try:
            emb.upsert([command])
        except Exception as e:
            print(f"Error during upsert: {e}")

    # Esegui una ricerca
    # results = emb.search("select score,text,campo,tabella from txtai where similar() limit 2")

    # Interactive loop
    while True:
        # User input
        user_query = input("Enter your query (type 'exit' to quit): ")

        # Check for exit condition
        if user_query.lower() == 'exit':
            break

        # Perform a search based on user input
        results = emb.search(f"select score,text,campo,tabella,references from txtai where similar('{user_query}') limit 2")

        # Print the results
        print(results)

    '''
    # Stampa i risultati
    print(results)

    # Esempio di utilizzo del metodo transform
    transformed_text = emb.transform((None, "ragione sociale", None))
    print(transformed_text)
    '''

if __name__ == "__main__":
    dir_path = os.path.dirname(os.path.realpath(__file__))
    json_file_path = os.path.join(dir_path, "..", "JSON")
    jsonFileName = os.path.join(json_file_path, "movies.json") # va cambiata ogni volta che vuoi cambiare file
    emb(jsonFileName)