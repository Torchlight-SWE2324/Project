import os

content = (0, {"table": "watches", "field": "id", "type": "integer", "references": "None", "description": "Unique identifier for the watch"})

os.system('clear')

print("\033[1mPLAYGROUND 🛝\033[0m")
# extract data from content and print it
print(content[0])
print(content[1]["field"])
print(content[1]["type"])

# add message before content
print("Field name: " + str(content[1]["field"]))
print("Filed table: " + str(content[1]["table"]))
print("Filed type: " + str(content[1]["type"]))
print("References from other tables: " + str(content[1]["references"]))
print("Field description: " + str(content[1]["description"]))