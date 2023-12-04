import json
import sys

def decode_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data

def print_table_info(table):
    print(f"Table Name: {table['name']}")
    print("Columns:")
    for column in table['columns']:
        print(f"  - Name: {column['name']}")
        print(f"    Type: {column['type']}")
        print(f"    Description: {column['description']}")
        if 'references' in column:
            print(f"    References: {column['references']}")
        print()

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    decoded_data = decode_json_file(file_path)

    # Accessing the decoded data
    tables = decoded_data['tables']
    for table in tables:
        print_table_info(table)

if __name__ == "__main__":
    main()