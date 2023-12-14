from txtai import Embeddings
import os
import sys

# Your existing code
content = (0, {"table": "watches", "field": "id", "type": "integer", "references": "None", "description": "Unique identifier for the watch"})

# Extract relevant information
text = content[1]["description"]
field_name = content[1]["field"]
table_name = content[1]["table"]

# Initialize the Embeddings module with the specified model
emb = Embeddings({"path": "efederici/sentence-BERTino", "content": True})

# Upsert the data into the txtai Embeddings
emb.upsert([(0, {"text": text, "campo": field_name, "tabella": table_name})])

# Execute a search using the txtai library
results = emb.search("select score,text,campo,tabella from txtai where similar('unique identifier') limit 2")

# Print the results
print(results)
for result in results:
    print(f"\nScore: {result['score']}")
    print(f"Text: {result['text']}")
    print(f"Field name: {result['campo']}")
    print(f"Table name: {result['tabella']}\n")

