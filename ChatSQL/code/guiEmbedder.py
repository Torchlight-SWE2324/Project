#versione per GUI di embedder.py
import re

def generatePrompt(generated_commands, emb, user_query):
    if emb == None:
        return "Error: emb is None"
    results = emb.search(f"select score,text,table,table-description,field,type,references,description from txtai where similar('{user_query}') limit 3")
    table_fields = {}

    ret = "SCORE FOR DEBUGGING ONLY\n\n"
    for result in results:
        ret += f"Score: {result['score']}\n"

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
    ret += "\nThe database contains the following tables:\n"
    for table, fields in table_fields.items():
        field_str = ', '.join([f"'{field}'" for field in fields])
        ret += f"'{table}' with fields {field_str};\n"

    messages = []

    for command_result in results:
        command_id = int(re.search(r"\((\d+),", command_result['text']).group(1))
        references_value = generated_commands[command_id][1]["references"]

        if references_value:
            table_name = generated_commands[command_id][1]["table"]
            field_name = generated_commands[command_id][1]["field"]
            messages.append(f"'{table_name}.{field_name}' references '{references_value}';\n")

    # Check if there are messages to show
    if messages:
        ret += "\nThe database contains the following relationships:\n"
    # Print messages if show_message is True
    for message in messages:
        ret += "\n"+message
    ret += f"\nGenerate the SQL query equivalent to: {user_query}"
    return ret