import json


# Extraer el JSON del response
def extract_json_from_response(response_content):

    # Extraer los bloques de JSON del contenido
    import re

    # Expresión regular para encontrar bloques JSON
    json_pattern = re.compile(r'```json\n(.*?)\n```', re.DOTALL)

    # Encontrar todos los bloques JSON
    json_blocks = json_pattern.findall(response_content)

    # Convertir cada bloque JSON a un objeto Python
    json_objects = [json.loads(block) for block in json_blocks]

    # crear un archivo JSON con los bloques JSON
    with open('jsons/response.json', 'w') as json_file:
        json.dump(json_objects, json_file, indent=2)
        print("JSON file created successfully.")