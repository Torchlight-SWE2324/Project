import json

def json_decoder(json_data):
    code = []
    for table in json_data["tables"]:
        table_name = table["name"]
        for column in table["columns"]:
            column_name = column["name"]
            description = column.get("description", "")
            if "references" in column:
                referenced_table = column["references"]
                code.append(f"emb.upsert((len(code), {{'text': '{description}', 'campo': '{column_name}', 'tabella': '{table_name}'}}")
                code.append(f"emb.upsert((len(code), {{'text': '{description} (foreign key referencing {referenced_table})', 'campo': '{column_name}', 'tabella': '{table_name}'}}")
            else:
                code.append(f"emb.upsert((len(code), {{'text': '{description}', 'campo': '{column_name}', 'tabella': '{table_name}'}}")

    return code

if __name__ == "__main__":
    with open("ChatSQL/res/data.json") as f:
        json_data = json.load(f)

    code = json_decoder(json_data)
    print(code)
