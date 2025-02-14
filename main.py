
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
from bedrock_example import initialize_bedrock_client, invoke_bedrock_model

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str
    json_data: dict


@app.post("/process-prompt")
async def process_prompt(request: PromptRequest):
    try:
        # Initialize Bedrock client
        bedrock_client = initialize_bedrock_client()

        # Combine prompt with JSON data and output sample
        context = (
            f"{request.prompt}\n\n"
            f"Datos: {json.dumps(request.data, indent=2, ensure_ascii=False)}\n\n"
            f"Formato de salida esperado: {json.dumps(request.output_sample, indent=2, ensure_ascii=False)}\n\n"
        )

        # Get response from Bedrock
        response = invoke_bedrock_model(bedrock_client, context)

        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

