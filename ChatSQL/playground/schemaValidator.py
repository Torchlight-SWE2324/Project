import json
# IMPORTANT: jsonschema is not a python library
# You need to install it with pip using the command:
# pip install jsonschema
from jsonschema import validate, ValidationError

def is_json_compliant(json_data, json_schema):
    try:
        validate(instance=json_data, schema=json_schema)
        return True, None
    except ValidationError as e:
        return False, str(e)

# Load JSON Schema from file
with open("/Users/giovannifilippini/Desktop/UNI/swe/progetto/1_repos/ChatSQL/ChatSQL/res/anpr.json", "r") as schema_file:
    json_schema = json.load(schema_file)

# Load JSON data from file
with open("/Users/giovannifilippini/Desktop/UNI/swe/progetto/1_repos/ChatSQL/ChatSQL/res/schema.json", "r") as data_file:
    json_data = json.load(data_file)

# Check compliance
is_compliant, error_message = is_json_compliant(json_data, json_schema)

if is_compliant:
    print("The JSON is compliant with the schema.")
else:
    print(f"The JSON is not compliant. Error: {error_message}")

