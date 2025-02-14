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


def invoke_bedrock_model(client, prompt, model_id="amazon.nova-micro-v1:0"):
    """
    Invoke the Bedrock model with a prompt
    """
    body = json.dumps({
        "messages": [
            {"role": "user", "content": [prompt]}
        ],
    })

    response = client.invoke_model(
        modelId=model_id,
        body=body,
    )

    # Parse and return the response
    response_body = json.loads(response.get('body').read())
    return response_body['output']['message']['content'][0]['text']


def main():
    # Initialize the Bedrock client
    client = initialize_bedrock_client()

    # Read and load the JSON data
    with open('data.json', 'r') as json_file:
        json_data = json.load(json_file)
    # Create the prompt
    prompt = {"text": """Contexto: Se realiza una programación semanal de una maquina corrugadora de carton para cumplir con fechas de entrega y con eficiencia en el uso de recursos. Se realizan corridas que son bloques de producción que cortan al menos 1 caja, máximo 2, y las corridas son ordenadas para su producción durante el día, según el tiempo que toma producirlas y la fecha de entrega del pedido dejando máximo 2 dias de anticipación para la produccion de un pedido. Se cuida el no sobrecargar un solo día de trabajo.

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

Instrucciones: Analiza los datos proporcionados y optimiza los pedidos para aprovechar al máximo el material, cumplir con fechas de entrega y respetar las reglas de negocio impuestas. La respuesta debe ser un JSON estructurado con la información de las corridas, incluyendo qué día y hora se ejecuta cada corrida, qué pedidos incluye, su refile.""".format(
        json.dumps(json_data, indent=2, ensure_ascii=False))}

    try:
        # Invoke the model
        response = invoke_bedrock_model(client, prompt)
        print("AI Response:", response)
    except Exception as e:
        print(f"Error occurred: {str(e)}")


if __name__ == "__main__":
    main()
