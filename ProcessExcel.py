import time
from datetime import datetime, time as dt_time
import pandas as pd


def tu_script_principal(ruta=""):
    """Aquí va el código de tu script que quieres ejecutar"""
    print("Ejecutando tarea programada...")
    # Tu código principal aquí
    df = pd.read_excel(ruta)
    print(df)


def ejecutar_en_horario(hora_inicio, hora_fin, intervalo=3600):
    """
    Ejecuta un script dentro de un rango horario específico

    Args:
        hora_inicio (tuple): (horas, minutos) de inicio
        hora_fin (tuple): (horas, minutos) de fin
        intervalo (int): segundos entre verificaciones (default 1 hora)
    """
    hora_inicio = dt_time(*hora_inicio)
    hora_fin = dt_time(*hora_fin)

    while True:
        ahora = datetime.now().time()
        print(f"Verificando a las: {ahora.strftime('%H:%M:%S')}")  # Agregamos esta línea para ver la hora actual en cada ciclo

        # Verificar si estamos dentro del horario deseado
        if hora_inicio <= ahora <= hora_fin:
            print(f"Ejecutando script a las {ahora}")
            tu_script_principal(ruta=r"C:\Users\Franco Stuart\OneDrive\Desktop\python-docker\PythonDocker\input.xlsx")
        else:
            print(f"Fuera del horario programado. Hora actual: {ahora}")

        # Esperar el intervalo especificado
        time.sleep(intervalo)


# Ejemplo: ejecutar entre las 9:30 y las 18:15, verificando cada 5 minutos
if __name__ == "__main__":
    ejecutar_en_horario(
        hora_inicio=(9, 30),  # 9:30 AM
        hora_fin=(23, 50),  # 6:15 PM
        intervalo=100  # 5 minutos (300 segundos)
    )