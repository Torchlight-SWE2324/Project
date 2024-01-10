import json
from utils import jsonValidator

if __name__ == "__main__":
    # Use absolute paths for schema and data files
    schema_file_path = "ChatSQL/code/schema.json"
    data_file_path = "ChatSQL/JSON_old_versions/movies.json"

    # Load JSON_old_versions Schema from file
    with open(schema_file_path, "r") as schema_file:
        json_schema = json.load(schema_file)

    # Load JSON_old_versions data from file
    with open(data_file_path, "r") as data_file:
        json_data = json.load(data_file)

    # Check compliance
    is_compliant, error_message = jsonValidator(json_data, json_schema)

    if is_compliant:
        print("The JSON_old_versions is compliant with the schema.")
    else:
        print(f"The JSON_old_versions is not compliant. Error: {error_message}")