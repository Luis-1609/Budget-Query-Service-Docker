from functions_sheets import *
from functions_webscraping import *
from datetime import datetime
import logging

SHEET_DATA = "Datos"
SHEET_RECORDS = "Registros Base"

logger = logging.getLogger("Scraper.functions")

def update_query_state(sheets, state_message):
    update_sheet_values(sheets, f"{SHEET_DATA}!B14", [[state_message]])

def validate_sheets_data(sheets, lookup_fields):
    partida = lookup_fields[3][0]
    unidad = lookup_fields[8][0]

    if not partida or not unidad:
        logger.error("Error at getting key values.\n")
        update_query_state(sheets, "Error: Sin acceso a valores de Sheets")
        raise RuntimeError("Sheets error, ending current run.")

    if partida == "%" or unidad == "%":
        logger.error("Requested entry values were not provided.\n")
        update_query_state(sheets, "Error: Datos de entrada incompletos")
        raise RuntimeError("Logic error, ending current run.")

def save_query_record(sheets, lookup_fields, available_budget, i, client_name):
    # Get current date and time and format it as a string
    now = datetime.now()    
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    chartfield = lookup_fields[8][0] + "." + lookup_fields[10][0] + "." + lookup_fields[9][0] + "." + lookup_fields[11][0]
    solicitud = "" if lookup_fields[0][0] == "%" else lookup_fields[0][0]

    record = [[timestamp, client_name, solicitud, lookup_fields[1][0], lookup_fields[2][0], lookup_fields[3+i][0],
               chartfield, lookup_fields[8][0], lookup_fields[9][0], lookup_fields[10][0], lookup_fields[11][0],
               available_budget[0][0], available_budget[0][1], available_budget[0][2], available_budget[0][3], available_budget[0][4]]]
    
    safe_insert_at_bottom(sheets, SHEET_RECORDS, record)

def process_budget_item(driver, sheets, lookup_fields, i, client_name):
    if lookup_fields[3+i][0] != "%":
        budget_data = get_available_budget(driver, lookup_fields, i)

        if budget_data:
            save_query_record(sheets, lookup_fields, budget_data[0], i, client_name)
            if len(budget_data) > 1:
                # Save the search results in Sheets
                update_sheet_values(sheets, f"'Tabla {i+1}'!A2", budget_data[1])
        else:
            logger.error("The search request could not be completed.\n")
            update_query_state(sheets, "Error: Extracción de datos fallida")
            raise RuntimeError("Scraper error, ending current run.")

def search_available_budget():
    sheets = get_sheets_api(get_valid_creds())
    
    # Get base values of the Query (Estado, Nombre Usuario)
    base_values = get_sheet_values(sheets,  f"{SHEET_DATA}!F1:F2")
    
    if base_values[0][0] == "NO":
        return
        
    logger.info(f"Query: {base_values}")    
    logger.info("Starting budget query...")

    client_name = base_values[1][0]
    update_sheet_values(sheets, f"{SHEET_DATA}!F1", [["NO"]])

    # Get lookup fields (Año, Cuenta, Unidad, Actividad, Sede, Ref Ppto)
    lookup_fields = get_sheet_values(sheets,  f"{SHEET_DATA}!B1:B12")
    logger.info(f"Entry values:\n{lookup_fields}")

    # Clean the cells with raw data in Sheets
    clear_sheet_values(sheets, f"{SHEET_DATA}!C1:C12")
    clear_sheet_values(sheets, f"{SHEET_DATA}!B14")
    clear_sheet_values(sheets, f"'Tabla 1'!A2:N200")
    clear_sheet_values(sheets, f"'Tabla 2'!A2:N200")
    clear_sheet_values(sheets, f"'Tabla 3'!A2:N200")
    clear_sheet_values(sheets, f"'Tabla 4'!A2:N200")
    clear_sheet_values(sheets, f"'Tabla 5'!A2:N200")
    
    # Validate the Sheets data and save the lookup fields
    validate_sheets_data(sheets, lookup_fields)
    update_sheet_values(sheets, f"{SHEET_DATA}!C1:C12", lookup_fields)
    update_query_state(sheets, "Consultando...")
    
    driver = get_chrome_driver()

    # Search in the webpage (Centuria)
    log_in(driver)
    go_to_general_budget(driver)

    for i in range(5):
        process_budget_item(driver, sheets, lookup_fields, i, client_name)

    update_query_state(sheets, "Consulta Finalizada")
    logger.info("Budget query completed.")

    driver.close()