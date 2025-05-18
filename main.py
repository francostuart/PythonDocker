import time
import os
import json
from pathlib import Path
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
app = FastAPI()

CAPTURAS_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), "capturas")

# Si no existe, la creamos
os.makedirs(CAPTURAS_DIR, exist_ok=True)

# Montamos ya con la certeza de que existe
app.mount("/capturas", StaticFiles(directory=CAPTURAS_DIR), name="capturas")


@app.get("/")
def root():
    return {"message": "Scraping API con Selenium"}


@app.get("/scrap")
def interactuar_con_web():

    options = Options()
    opts.binary_location = "/usr/bin/chromium"
    # options.binary_location = "/usr/bin/chromium"
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')

    # Configuración de Selenium (navegador Chrome)
    # options = webdriver.ChromeOptions()
    # options.add_argument('--headless')  # Para que no se abra la ventana del navegador
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    # service = Service("/usr/local/bin/chromedriver")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        # service=service,
        options=options
    )

    try:
        # Acceder a una página web de ejemplo
        url = 'https://arenarpa.com/crazy-form'
        driver.get(url)
        print(url)

        driver.maximize_window()

        # Esperar que la página cargue completamente
        time.sleep(3)

        # Obtener el título de la página
        titulo = driver.title
        print(f"El título de la página es: {titulo}")

        # Obtener el texto de algún elemento
        # Ejemplo: Suponiendo que hay un <h1> en la página
        encabezado = driver.find_element(By.XPATH, '/html/body/app-root/app-crazy-form/div/div[1]/h2').text
        print(f"Encabezado de la página: {encabezado}")

        time.sleep(3)

        # 1. Define la carpeta donde guardarás las capturas
        output_dir = Path("capturas")
        # 2. Asegúrate de que exista (mkdir –p)
        output_dir.mkdir(parents=True, exist_ok=True)

        fecha_actual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # captura de pantallla
        screenshot_path = output_dir / f"captura_arena_{fecha_actual}.png"
        driver.save_screenshot(screenshot_path)
        return {"message": "Scraping finalizado correctamente"}

    finally:
        driver.quit()  # Cerramos el navegador


@app.get("/list")
async def listar_capturas_json(carpeta="capturas"):
    """
    Lista todos los archivos de la carpeta especificada
    y devuelve un JSON con la lista de nombres.
    """
    # 1) Asegurarse de que la carpeta existe
    if not os.path.isdir(carpeta):
        return json.dumps({"error": f"La carpeta '{carpeta}' no existe."})

    # 2) Recorrer la carpeta y quedarnos solo con archivos
    archivos = [
        nombre for nombre in os.listdir(carpeta)
        if os.path.isfile(os.path.join(carpeta, nombre))
    ]

    # 3) Crear el JSON de salida
    resultado = {
        "timestamp": datetime.now().isoformat(),
        "carpeta": carpeta,
        "capturas": archivos
    }
    return resultado
