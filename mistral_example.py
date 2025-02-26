import boto3
import json


def initialize_bedrock_client():
    """
    Initialize and return a Bedrock client
    """
    bedrock_client = boto3.client(
        service_name='bedrock-runtime',
        region_name='us-east-1'  # replace with your preferred region
    )
    return bedrock_client


def invoke_mistral_model(client, prompt, model_id="mistral.mistral-large-2402-v1:0"):
    """
    Invoke the Mistral model with a prompt
    """
    body = json.dumps({
        "prompt": prompt["text"],
        "max_tokens": 4096,
        "temperature": 0.1,
        "top_p": 0.9,
        "stop": []
    })

    response = client.invoke_model(
        modelId=model_id,
        body=body,
        contentType='application/json',
        accept='application/json'
    )

    # Parse and return the response
    response_body = json.loads(response.get('body').read())
    return response_body['outputs'][0]['text']


def main():
    # Initialize the Bedrock client
    client = initialize_bedrock_client()

    # Read and load the JSON data
    with open('jsons/data.json', 'r') as json_file:
        json_data = json.load(json_file)
    
    # Create the prompt
    prompt = {"text": """Contexto: Se realiza una programación semanal de una maquina corrugadora de

Reglas de negocio:
- Refile (desperdicio) 2cm-4cm por lado (izq y der) de toda la lamina después de combinar.
- Laminas de 160cm, 134cm y 1120cm.
- Solo se permiten máximo 2 combinaciones por lámina.
- Los pedidos deben agruparse según compatibilidad de ECT, liner y tratamiento antihumedad.
- Priorizar pedidos con fecha de entrega más cercana.

Horario:
- Lunes 8:20am - 6:00pm
- Martes-jueves 8:20am - 10:30pm
- Viernes 8:20am - 5:30pm
- Tiempo: 45min por corrida

Datos del sistema:
{}

Instrucciones: Analiza los datos proporcionados y optimiza los pedidos para aprovechar al máximo el """.format(
        json.dumps(json_data, indent=2, ensure_ascii=False))}

    try:
        # Invoke the model
        response = invoke_mistral_model(client, prompt)
        print("AI Response:", response)
    except Exception as e:
        print(f"Error occurred: {str(e)}")


if __name__ == "__main__":
    main()