import os
import json
import streamlit as st

from guiUtils import generateUpsertCommands, upsert
from txtai import Embeddings

def loadIndex(dictionary_file_name):
    if st.session_state.emb == None:
        st.session_state.emb = Embeddings({"path": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2", "content": True})
    st.session_state.emb.load(f"indexes/{os.path.splitext(dictionary_file_name)[0]}")

def createIndex(dictionary_path):
    st.session_state.upsert_commands = generateUpsertCommands(dictionary_path)
    st.session_state.emb = upsert(st.session_state.upsert_commands)
    file_name = os.path.basename(dictionary_path)
    st.session_state.emb.save(f"indexes/{os.path.splitext(file_name)[0]}")
    st.session_state.emb.close()

def deleteIndex(dirPath, filename_to_delete_without_extension):
    indexes_folder_path = os.path.join(dirPath, "indexes")
    index_folder_to_delete_path = os.path.join(indexes_folder_path, filename_to_delete_without_extension)

    for file_to_delete in os.listdir(index_folder_to_delete_path):
        file_to_delete_path = os.path.join(index_folder_to_delete_path, file_to_delete)
        os.remove(file_to_delete_path)
    os.rmdir(index_folder_to_delete_path)

def generatePromptAdmin(emb, user_query):
    if emb == None:
        return "Error: there is no model connected"

    embedder_search_result = emb.search(f"select score, text, table_name, table_description, field_name, field_type, field_references from txtai where similar('{user_query}') limit 30") #da definire il limite

    prompt = ""
    for result in embedder_search_result:
        prompt = prompt+"\n"+str(result)+"\n"

    return prompt

def generatePromptUser(emb, user_query):
    if emb == None:
        return "Error: there is no model connected"

    #embedder_search_result = emb.search(f"select score, text, table_name, table_description, field_name, field_type, field_references, from txtai where similar('{user_query}') limit 30") #!!! DA SOSTITUIRE "LIMIT 30"

    prompt =''

    if st.session_state.logged_in == True:
        '''
        for result in embedder_search_result:
            prompt = prompt+"\n"+str(result)+"\n"
        return prompt
        '''
        embedder_search_result = emb.search(f"select score, text, table_name, table_description, field_name, field_type, field_references, from txtai where similar('{user_query}') limit 30") #!!! DA SOSTITUIRE "LIMIT 30"

        for result in embedder_search_result:
            prompt += f"'{result['table_name']}.{result['field_name']}' have score: {result['score']};\n"

        return prompt

    else:
        embedder_search_result = emb.search(f"select score, text, table_name, table_description, field_name, field_type, "
                                            f"field_references, from txtai where similar('{user_query}') and score >= 0.4")

        selected_fields_list = {}
        relationship_list = []

        ret = ""
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


        prompt = ''
        prompt_fields_list = ''

        for table, fields in selected_fields_list.items():
            field_str = ', '.join([f"'{field}'" for field in fields])
            prompt_fields_list += f"'{table}' with fields {field_str};\n"

        if prompt_fields_list:
            prompt += f"{ret}\nThe database contains the following tables:\n"
            prompt += prompt_fields_list

            if relationship_list:
                prompt_relationship_list = "\nand the database contains the following relationships:\n"
                for relation in relationship_list:
                    prompt_relationship_list += relation

                prompt += prompt_relationship_list

            prompt += f"\nGenerate the SQL query equivalent to: {user_query}"

        else:
            prompt += "No relevant information was found in relation to the request"

        return prompt