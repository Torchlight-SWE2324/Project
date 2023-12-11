from txtai import Embeddings

# Inizializza il modulo Embeddings con il modello specificato
emb = Embeddings({"path": "efederici/sentence-BERTino", "content": True})

# Aggiungi alcuni dati di esempio
emb.upsert([(0, {"text": "campo che contiene la citta", "campo": "CITTA", "tabella": "CLIENTI"})])
emb.upsert([(1, {"text": "informazioni metodo di pagamento", "campo": "METPAGCLI", "tabella": "CLIENTI"})])
emb.upsert([(2, {"text": "codice cliente", "campo": "CODCLI", "tabella": "CLIENTI"})])
emb.upsert([(3, {"text": "ragione sociale", "campo": "RAGSOCCLI", "tabella": "CLIENTI"})])
emb.upsert([(4, {"text": "nome della azienda", "campo": "RAGSOCCLI", "tabella": "CLIENTI"})])

# Esegui una ricerca
results = emb.search("select score,text,campo,tabella from txtai where similar('cliente') limit 2")

# Stampa i risultati
print(results)
# Esempio di utilizzo del metodo transform
transformed_text = emb.transform((None, "ragione sociale", None))
print(transformed_text)