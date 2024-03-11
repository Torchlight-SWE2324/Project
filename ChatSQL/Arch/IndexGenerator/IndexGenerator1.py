import IndexGenerator

class IndexGenerator1(IndexGenerator):
    def __init__(self):
        super().__init__()

    def generate_index(self, model, commands):
        model.getEmbeddings().index([{"table_name": command["table_name"], "table_description": command["table_description"], "field_name": command["field_name"], "field_type": command["field_type"], "field_references": command["field_references"], "text": command["table_description"]} for command in commands])