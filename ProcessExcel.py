import time
from datetime import datetime, time as dt_time
import pandas as pd
import argparse


def tu_script_principal(ruta=""):
    """Aquí va el código de tu script que quieres ejecutar"""
    print("Ejecutando tarea programada...")
    # Tu código principal aquí
    df = pd.read_excel(ruta)
    print(df)


def ejecutar_en_horario(input, hora_inicio, hora_fin, intervalo=3600):
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
            tu_script_principal(ruta=input)
        else:
            print(f"Fuera del horario programado. Hora actual: {ahora}")

        # Esperar el intervalo especificado
        time.sleep(intervalo)


# Ejemplo: ejecutar entre las 9:30 y las 18:15, verificando cada 5 minutos
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script para procesar datos con Pandas.")

    # Definir argumentos
    parser.add_argument("input", help="Ruta al archivo de entrada (ej. input.xlsx)")
    parser.add_argument("start", help="hora de inicio de ejecucion del script - 9:30 AM")
    parser.add_argument("end", help="hora de fin de ejecucion del script - 6:30 PM")
    parser.add_argument("interval", help="intervalo de ejecucion del script - 5 minutos (300 segundos)")

    # Parsear los argumentos de la línea de comandos
    args = parser.parse_args()

    # Convertir los argumentos a los formatos adecuados
    hora_inicio = tuple(map(int, args.start.split(':')))  # Convierte "9:30" a (9, 30)
    hora_fin = tuple(map(int, args.end.split(':')))  # Convierte "18:30" a (18, 30)
    intervalo = int(args.interval)  # Convierte el intervalo a entero

    # Llamar a la función principal con los argumentos obtenidos
    # print(args.input, args.start, args.end, args.interval)
    ejecutar_en_horario(input=args.input, hora_inicio=hora_inicio, hora_fin=hora_fin, intervalo=intervalo)
    # ejecutar_en_horario(
    #     hora_inicio=(5, 30),  # 9:30 AM
    #     hora_fin=(23, 50),  # 6:15 PM
    #     intervalo=100  # 5 minutos (300 segundos)
    # )
