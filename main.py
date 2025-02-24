
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
        Boxes data: {json.dumps(request.data_cajas, indent=2, ensure_ascii=False)}\n\n
        Sheets data: {json.dumps(request.data_laminas, indent=2, ensure_ascii=False)}\n\n
        Purchase orders data: {json.dumps(request.data_pedidos, indent=2, ensure_ascii=False)}\n\n
        Expected output, Respond with a JSON structured as follows, with no extra text: {json.dumps(request.output_sample, indent=2, ensure_ascii=False)}\n\n
        """}

        # Get response from Bedrock
        response = invoke_bedrock_model(bedrock_client, context)
        json_response = extract_json_from_response(response)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


texto = "You are an expert in production planning for corrugated cardboard machines. Your task is to create an optimized schedule that maximizes resource usage, minimizes waste (refile), and meets delivery deadlines. Follow the business rules strictly.\n\n### Context\nThe machine can process between one and two types of boxes per run. The objective is to maximize sheet usage and ensure all orders are completed before their delivery date. Prioritize orders based on delivery date and quantity.\n\n### Rules\n\n1. **Corrugator Run:**\n   - Process up to two box types per run.\n   - The allowed refile is between 4 cm and 8 cm.\n   - If the sheet has associated boxes (caja.id), it cannot be combined with another box.\n   - If a sheet has no associated boxes, it can combine up to two compatible boxes.\n\n2. **Box Compatibility:**\n   - Two boxes are compatible if they share the same ECT, liner, and anti-humidity treatment.\n   - Incompatible boxes cannot be combined on the same sheet.\n\n3. **Refile Calculation:**\n   - Calculate refile as: sheet_width - (sum of box widths * quantity per sheet).\n   - Ensure the refile is within 4 cm to 8 cm.\n   - If the refile exceeds limits and no adjustment is possible, schedule the box alone and mark it with \"tira_autorizada\": true.\n\n4. **Production Calculations:**\n   - **Salen:** Number of times a box fits into the sheet width. Example: if the box width is 50 cm and the sheet is 105 cm wide, salen = 2, leaving a 5 cm refile.\n   - **Metros lineales:** ((cantidad * largo) / 100) / salen\n   - **Production time:** metros_lineales / 65 (round the result to the nearest minute)\n   - **Total weight:** metros_lineales * lamina.grms / 1000\n\n5. **Scheduling:**\n   - Respect working hours:\n     - Monday: 08:20–18:00\n     - Tuesday to Thursday: 08:20–22:30\n     - Friday: 08:20–17:30\n   - Fill the available time before moving to the next day.\n   - Runs must be continuous without dead time.\n   - If a run exceeds the day's available time, continue on the next working day without interruption.\n   - If all days are full, continue scheduling into the next week.\n\n6. **Prioritization of Orders:**\n   - Select the order with the highest quantity as the priority.\n   - To calculate the complementary pieces:  \n     complemento_piezas = ((cantidad_prioridad * largo_prioridad / salen_prioridad)) / (largo_complemento * salen_complemento)\n\n7. **Validation Rules:**\n   - Ensure the sum of box widths plus refile does not exceed the sheet width.\n   - The refile must strictly remain between 4 cm and 8 cm.\n   - Start and end times should reflect the exact production time and align with working hours.\n   - Verify that all calculations match the results in the output.\n\n### Final Instructions\n- Return only the JSON.\n- Validate all calculations before providing the final output.\n- Ensure there are no discrepancies between calculated values and the ones shown in the JSON.\n- Maintain consistency in the refile, production time, and scheduling."