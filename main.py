
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
from bedrock_example import initialize_bedrock_client, invoke_bedrock_model
from extract_json_from_response import extract_json_from_response

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str
    data_cajas: list
    data_laminas: list
    data_pedidos: list
    output_sample: list

@app.post("/process-prompt")
async def process_prompt(request: PromptRequest):
    try:
        # Initialize Bedrock client
        bedrock_client = initialize_bedrock_client()

        # Combine prompt with structured JSON data
        context = {"text":f"""
        {request.prompt}\n\n
        Datos Cajas: {json.dumps(request.data_cajas, indent=2, ensure_ascii=False)}\n\n
        Datos Láminas: {json.dumps(request.data_laminas, indent=2, ensure_ascii=False)}\n\n
        Datos Pedidos: {json.dumps(request.data_pedidos, indent=2, ensure_ascii=False)}\n\n
        Formato de Salida Esperado: {json.dumps(request.output_sample, indent=2, ensure_ascii=False)}\n\n
        """}

        # Get response from Bedrock
        response = invoke_bedrock_model(bedrock_client, context)
        json_response = extract_json_from_response(response)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

