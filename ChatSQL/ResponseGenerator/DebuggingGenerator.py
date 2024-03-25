import os
import json

from txtai import Embeddings
#---Se si crea una interfaccia in comune tra DebuggingGenerator e PromptGenerator----
# from ResponseGeneratorInterface import *         
# class DebuggingGenerator(ResponseGeneratorInterface):
#------------------------------------------------------------------------------------    
class DebuggingGenerator:
    def __init__(self) -> None:
        pass


#Output della funzione implementata
"""
TABLE 'item':
- FIELD 'id' | DESCRIPTION 'Unique identifier assigned to each auction item' | SCORE;
- FIELD 'name' | DESCRIPTION 'Name of the auction item' | SCORE;
- FIELD 'description' | DESCRIPTION 'Description of the auction item' | SCORE;
- FIELD 'starting_bid' | DESCRIPTION 'Starting bid amount for the auction item' | SCORE;


class Response(ABC):

    @abstractmethod
    def generateResponse(query, dictionary_path):
        pass

class ResponseUser:
    implementa utente
    def generateResponse(query, dictionary_path):
        
    tutti tranne score

class ResponseTechnician:
    implementa tecnico
    tutto con score
    
    

class ResponseModel:
    + string: Response

    def cmdGenerateResponse()

    responseGenerator = ResponseGenerator()   interfaccia

    if //controlla se accesso fatto o meno
        responseGenerator = DebuggingGenerator()  sottoclasse1
    else:
        responseGenerator = PromptGenerator() sottoclasse2

    Response.generateResponse()

"""
def generateResponse(emb, user_query, dictionary_path):


    embedder_search_result = emb.search(f"SELECT score, text, table_name, field_name, field_description FROM txtai WHERE similar('{user_query}') AND score > 0.01 GROUP BY table_name, field_name", limit=50)

    # Gestione dizionari e loro percorsi ancora da implementare, dipende da che paramtri passeremo alla funzione/cosa arriva dal controller
    # Con l'implentazione attuale, per il debug basta avere l'emb con dentro caricato l'index corrente 
    # dictionary_path = os.path.join(getDictionariesFolderPath(), dictionary_name)

    tables_with_fields = {}

    for result in embedder_search_result:
        table_name = result['table_name']
        field_name = result['field_name']
        field_description = result['field_description']
        score = result['score']

        if table_name not in tables_with_fields:
            tables_with_fields[table_name] = []

        tables_with_fields[table_name].append((field_name, field_description, score ))

    prompt = "Similarity score with the user interrogation of each field in the database:\n\n"

    for table_name, fields in tables_with_fields.items():
        prompt += f"TABLE '{table_name}':\n"
        for field, description, score in fields:
            prompt += f"- FIELD: {field} {' '*(max(len(field), 12) - len(field))} | SCORE: {score:.5f} | DESCRIPTION: {description}\n"

    return prompt