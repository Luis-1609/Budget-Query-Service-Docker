from functions_selenium import *
import config

# URL de la página donde se realizará el Webscrapping
WEBSCRAPPING_URL = config.WEBSCRAPPING_URL

# El usuario y contraseña siguientes para las pruebas:
TEST_USERNAME = config.TEST_USERNAME
TEST_PASSWORD = config.TEST_PASSWORD

MAX_TRIES = 2

logger = logging.getLogger("Scraper.functions")

def log_in(driver, user=TEST_USERNAME, password=TEST_PASSWORD):
    driver.get(WEBSCRAPPING_URL)

    for i in range(MAX_TRIES):
        # Select the purchasing module
        find_and_click(driver, By.CSS_SELECTOR, ".selected")
        find_and_click(driver, By.CSS_SELECTOR, ".circle")

        # Enter credentials
        find_and_send(driver, By.ID, "userid", user)
        find_and_send(driver, By.ID, "pwd", password + Keys.ENTER)

        # Verify successful login
        try:
            wait_until_present(driver, By.ID, "pthnavbca_PORTAL_ROOT_OBJECT")
            logger.debug("Successful login.")
            return
        except:
            pass

    # Handle the error case
    logger.error("Error at logging in.")
    raise RuntimeError("Login error, ending current run.")

def go_to_general_budget(driver): 
    driver.switch_to.default_content()
    find_and_click(driver, By.ID, "pthnavbca_PORTAL_ROOT_OBJECT") # "Menu Principal"
    find_and_click(driver, By.ID, "EPCO_COMMITMENT_CONTROL") # "Control de Compromisos"
    find_and_click(driver, By.ID, "EPKK_ANALYZE_CONTROL_BUDGETS2") # "Revision Actividades de Ppto"
    find_and_click(driver, By.ID, "crefli_EP_KK_INQ_LEDGER_GBL") # "Descr General de Presupuestos"

    driver.switch_to.frame(0)
    find_and_click(driver, By.ID, "#ICSearch") # "Buscar"

def get_available_budget(driver, lookup_fields, i):
    anho_ini = lookup_fields[1][0]
    anho_fin = lookup_fields[2][0]
    cuenta = lookup_fields[3+i][0]
    unidad = lookup_fields[8][0]
    sede = lookup_fields[9][0]
    actividad = lookup_fields[10][0]
    ref_ppto = lookup_fields[11][0]

    driver.switch_to.default_content()
    driver.switch_to.frame(0)
    find_clear_and_send(driver, By.ID, "KK_INQ_LD_CRIT_BUSINESS_UNIT", "GL001") # "Unidad Negocio"
    find_clear_and_send(driver, By.ID, "KK_INQ_LDTS_TMP_BP_FROM$0", anho_ini) # "Periodo Inicio"
    find_clear_and_send(driver, By.ID, "KK_INQ_LDTS_TMP_BP_TO$0", anho_fin) # "Periodo Fin"

    find_clear_and_send(driver, By.ID, "KK_INQ_LD_CF_CHARTFIELD_VALUE$0", cuenta)
    find_clear_and_send(driver, By.ID, "KK_INQ_LD_CF_CHARTFIELD_VALUE$1", unidad)
    find_clear_and_send(driver, By.ID, "KK_INQ_LD_CF_CHARTFIELD_VALUE$2", sede)
    find_clear_and_send(driver, By.ID, "KK_INQ_LD_CF_CHARTFIELD_VALUE$3", actividad)
    find_clear_and_send(driver, By.ID, "KK_INQ_LD_CF_CHARTFIELD_VALUE$4", ref_ppto)
    
    find_and_click(driver, By.ID, "KK_INQ_WRK_PB_FETCH") # "Buscar"

    # Check if data was found
    founded = False

    driver.switch_to.default_content()
    if is_element_present(driver, By.ID, "#ICOK", 2):
        find_and_click(driver, By.ID, "#ICOK")
        logger.info(f"The search results were empty for item {cuenta}.")
    else:            
        driver.switch_to.frame(0)
        if is_element_present(driver, By.ID, "KK_INQ_WRK_AMT7", 2):
            logger.info(f"Found valid results for item {cuenta}.")
            founded = True
    
    if not founded:
        not_found_matrix = [[["", "", "", "", ""]]]
        return not_found_matrix

    # Get budget data and extract the table with search results
    available_budget = find_and_return_text(driver, By.ID, "KK_INQ_WRK_AMT7")
    budget = find_and_return_text(driver, By.ID, "KK_INQ_WRK_AMT1")
    expenses = find_and_return_text(driver, By.ID, "KK_INQ_WRK_AMT2")
    assessment = find_and_return_text(driver, By.ID, "KK_INQ_WRK_AMT3")
    preassessment = find_and_return_text(driver, By.ID, "KK_INQ_WRK_AMT4")
    
    found_matrix = [[[available_budget, budget, expenses, assessment, preassessment]]]

    # The JavaScript code is stored in a multi-line string
    js_code = """
        // Find the table by its ID (escaping the $ sign)
        var table = document.getElementById('tdgbrKK_INQ_LD_WS$0');
        if (!table) return [];

        var rows = Array.from(table.querySelectorAll('tbody tr'));
        
        return rows.map(row => {
            var cells = Array.from(row.querySelectorAll('td'));
            return cells.map(cell => cell.innerText.trim());
        });
    """
    # Run the script and get the list of lists back directly
    table_data = driver.execute_script(js_code)
    found_matrix.append(table_data)
    
    find_and_click(driver, By.ID, "KK_INQ_WRK_PB_RETURN") # "Regresar"

    return found_matrix