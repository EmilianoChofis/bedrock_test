import pandas as pd

# Ruta del archivo
file_path = "./CONTROL DE PEDIDOS ARAPACK 2025.xlsx"

# Cargar el archivo y listar las hojas
xls = pd.ExcelFile(file_path)
sheet_name = "SEM 03"

# Verificar si la hoja existe en el archivo
if sheet_name in xls.sheet_names:
    # Cargar los datos de la hoja especificada
    df = pd.read_excel(xls, sheet_name=sheet_name, skiprows=1)  # Saltar la primera fila (índice 0)

    # Convertir el DataFrame a formato JSON
    json_data = df.to_json(orient="records", date_format="iso")
else:
    json_data = f"Error: La hoja '{sheet_name}' no existe en el archivo."

# Guardar el JSON en un archivo
with open("data_pedidos.json", "w") as json_file:
    json_file.write(json_data)
