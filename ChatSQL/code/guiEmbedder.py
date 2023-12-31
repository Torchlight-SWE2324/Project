import json
#!!!!!!!!!! DA AGGIUSTARE FILE SCHEMA.JSON PER CAMPO REFERENCES


def generatePromptAdmin(emb, user_query):  # !!!!! DA REFACTORING + FARE VERSIONE USER ED ADMIN
    if emb == None:
        return "Error: there is no model connected"

    embedder_search_result = emb.search(f"select score, text, table_name, table_description, field_name, field_type, field_references, "
                         f" from txtai where similar('{user_query}') limit 30") #da definire il limite

    prompt=""
    for result in embedder_search_result:
        prompt = prompt+"\n"+str(result)+"\n"

    return prompt


def generatePromptUser(emb, user_query):
    if emb == None:
        return "Error: there is no model connected"

    embedder_search_result = emb.search(f"select score, text, table_name, table_description, field_name, field_type, field_references, "
                         f" from txtai where similar('{user_query}') limit 30") #!!! DA SOSTITUIRE "LIMIT 30"

    selected_fields_list = {}
    relationship_list = []

    for result in embedder_search_result:
        table_name = result['table_name']
        field_name = result['field_name']

        if table_name in selected_fields_list:
            selected_fields_list[table_name].append(field_name)
        else:
            selected_fields_list[table_name] = [field_name]

        if table_name == result['table_name'] and field_name == result['field_name'] and result['field_references']:
            references = json.loads(result['field_references'])
            relationship_list.append(f"'{table_name}.{field_name}' references '{references['table_name']}."
                            f"{references['field_name']}';\n")

    #!!! DA VEDERE QUANDO NON TROVA NESSUNA TABELLA
    prompt = f"\n\nThe database contains the following tables:\n\n" # SCEGLERE SE METTERE "s" QUANDO MULTIPLO

    for table, fields in selected_fields_list.items():
        field_str = ', '.join([f"'{field}'" for field in fields])
        prompt += f"'{table}' with fields {field_str};\n\n" #!!! ULTIMA ITERAZIONE SI METTE PUNTO # SCEGLERE SE METTERE "s" QUANDO MULTIPLO


    if relationship_list:
        prompt += "\nand the database contains the following relationships:\n" # SCEGLERE SE METTERE "s" QUANDO MULTIPLO

        for relation in relationship_list:
            prompt += "\n"+relation
        prompt += f"\nGenerate the SQL query equivalent to: {user_query}"

    return prompt