import json
import re


# Función para extraer y convertir el JSON del response
def extract_json_from_response(response_content):
    # Usar una expresión regular para extraer el contenido JSON
    json_pattern = r'\{.*\}'
    json_match = re.search(json_pattern, response_content, re.DOTALL)

    if json_match:
        json_str = json_match.group(0)  # Extraer el JSON como cadena
        try:
            # Convertir la cadena JSON a un objeto Python
            json_object = json.loads(json_str)

            # Guardar el JSON en un archivo
            with open('jsons/response.json', 'w') as json_file:
                json.dump(json_object, json_file, indent=2)
                print("JSON file created successfully.")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
    else:
        print("No JSON content found in the response.")
