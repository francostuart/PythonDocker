# interactuar_web.py
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def interactuar_con_web():
    # Configuración de Selenium (navegador Chrome)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Para que no se abra la ventana del navegador
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

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

        fecha_actual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        #captura de pantallla
        screenshot_path = f"captura_arena_{fecha_actual}.png"
        driver.save_screenshot(screenshot_path)

    finally:
        driver.quit()  # Cerramos el navegador



interactuar_con_web()