import json
# IMPORTANT: jsonschema is not a python library
# You need to install it with pip using the command:
# pip install jsonschema
from jsonschema import validate, ValidationError

def jsonValidator(json_data, json_schema):
    try:
        validate(instance=json_data, schema=json_schema)
        return True
    except ValidationError as e:
        return False

"""# Use absolute paths for schema and data files
schema_file_path = "ChatSQL/res/schema.json"
data_file_path = "ChatSQL/res/movies.json"

# Load JSON Schema from file
with open(schema_file_path, "r") as schema_file:
    json_schema = json.load(schema_file)

# Load JSON data from file
with open(data_file_path, "r") as data_file:
    json_data = json.load(data_file)

# Check compliance
is_compliant, error_message = jsonValidator(json_data, json_schema)

if is_compliant:
    print("The JSON is compliant with the schema.")
else:
    print(f"The JSON is not compliant. Error: {error_message}")"""