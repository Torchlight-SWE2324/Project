class ResponseTechnician():
    def __init__(self) -> None:
        pass

    def generateResponse(emb, user_query):
        embedder_search_result = emb.search(f"SELECT score, text, table_name, field_name, field_description FROM txtai WHERE similar('{user_query}') AND score > 0.01 GROUP BY table_name, field_name", limit=50)

        # Gestione dizionari e loro percorsi ancora da implementare, dipende da che parametri passeremo alla funzione/cosa arriva dal controller
        # Con l'implentazione attuale, per il debug basta avere l'emb con dentro caricato l'index corrente
        # dictionary_path = os.path.join(getDictionariesFolderPath(), dictionary_name)

        tables_with_fields = {}

        for result in embedder_search_result:
            table_name = result['table_name']
            field_name = result['field_name']
            field_description = result['field_description']
            score = result['score']

            if table_name not in tables_with_fields:
                tables_with_fields[table_name] = []

            tables_with_fields[table_name].append((field_name, field_description, score))

        prompt = "Similarity score with the user interrogation of each field in the database:\n\n"

        for table_name, fields in tables_with_fields.items():
            prompt += f"TABLE '{table_name}':\n"
            for field, description, score in fields:
                prompt += f"- FIELD: {field} {' '*(max(len(field), 12) - len(field))} | SCORE: {score:.5f} | DESCRIPTION: {description}\n"

        return prompt