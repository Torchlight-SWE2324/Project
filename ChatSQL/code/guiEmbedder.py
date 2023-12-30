import json

def generatePromptAdmin(emb, user_query):  # !!!!! DA REFACTORING + FARE VERSIONE USER ED ADMIN
    if emb == None:
        return "Error: there is no model connected"

    results = emb.search(f"select score, text, table_name, table_description, field_name, field_type, field_references, "
                         f" from txtai where similar('{user_query}') limit 30") #da definire il limite

    prompt=""
    for result in results:
        prompt = prompt+"\n"+str(result)+"\n"

    return prompt


def generatePromptUser(emb, user_query):
    if emb == None:
        return "Error: there is no model connected"

    results = emb.search(f"select score, text, table_name, table_description, field_name, field_type, field_references, "
                         f" from txtai where similar('{user_query}') limit 30") #!!! DA SOSTITUIRE "LIMIT 30"

    table_fields = {}
    messages = []
    for result in results:
        table_name = result['table_name']
        field_name = result['field_name']

        if table_name in table_fields:
            table_fields[table_name].append(field_name)
        else:
            table_fields[table_name] = [field_name]

        if table_name == result['table_name'] and field_name == result['field_name'] and result['field_references']:
            fieldsReferences = json.loads(result['field_references'])
            xxx = fieldsReferences['table_name'] #?? SERVE
            yyy = fieldsReferences['field_name'] #?? SERVE
            messages.append(f"'{table_name}.{field_name}' references '{xxx}."
                            f"{yyy}';\n")


    prompt = f"\n\nThe database contains the following tables:\n\n" # SCEGLERE SE METTERE "s" QUANDO MULTIPLO
    for table, fields in table_fields.items():
        field_str = ', '.join([f"'{field}'" for field in fields])
        prompt += f"'{table}' with fields {field_str};\n\n" #!!! ULTIMA ITERAZIONE SI METTE PUNTO # SCEGLERE SE METTERE "s" QUANDO MULTIPLO

    if messages:
        prompt += "\nand the database contains the following relationships:\n" # SCEGLERE SE METTERE "s" QUANDO MULTIPLO
    # Print messages if show_message is True
    for message in messages:
        prompt += "\n"+message
    prompt += f"\nGenerate the SQL query equivalent to: {user_query}"

    return prompt