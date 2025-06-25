import time
from datetime import datetime, time as dt_time
import pandas as pd
import argparse
import os
import glob
import logging
from typing import List

# Configuración de directorios desde variables de entorno
INPUT_DIR = os.getenv('EXCEL_INPUT_DIR', '/data/client1/upload')
PROCESSED_DIR = os.getenv('PROCESSED_DIR', '/data/client1/processed')
LOG_FILE = os.getenv('LOG_FILE', '/var/log/excel_processor.log')


def setup_logging():
    """Configura el logging para registrar todas las operaciones"""
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    # Añadir logger a consola
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    return logging.getLogger()


logger = setup_logging()


def parse_time(time_str: str) -> dt_time:
    """Convierte string HH:MM a objeto time con validación estricta"""
    try:
        hours, minutes = map(int, time_str.split(':'))
        if 0 <= hours <= 23 and 0 <= minutes <= 59:
            return dt_time(hours, minutes)
        raise ValueError
    except (ValueError, AttributeError):
        logger.error(f"Formato horario inválido: '{time_str}'. Use HH:MM en formato 24h (00:00 a 23:59)")
        exit(1)


def encontrar_archivos_excel() -> List[str]:
    """Encuentra todos los archivos Excel en el directorio de entrada"""
    patrones = ('*.xlsx', '*.xls', '*.XLSX', '*.XLS')
    archivos = []
    for patron in patrones:
        archivos.extend(glob.glob(os.path.join(INPUT_DIR, patron)))
    return sorted(archivos)  # Orden alfabético para consistencia


def procesar_archivo(ruta_archivo: str) -> bool:
    """Procesa un archivo Excel individual"""
    nombre_archivo = os.path.basename(ruta_archivo)
    try:
        logger.info(f"Procesando archivo: {nombre_archivo}")

        # Leer el archivo Excel
        df = pd.read_excel(ruta_archivo)
        logger.info(f"Archivo {nombre_archivo} leído correctamente (Filas: {len(df)})")

        # =============================================
        # AQUÍ VA TU LÓGICA PRINCIPAL DE PROCESAMIENTO
        # =============================================

        # Ejemplo: mostrar primeras filas
        print(f"\nContenido de {nombre_archivo}:")
        print(df.head())

        return True

    except Exception as e:
        logger.error(f"Error procesando {nombre_archivo}: {str(e)}")
        return False


def mover_archivo_procesado(ruta_original: str):
    """Mueve el archivo procesado al directorio correspondiente"""
    nombre_archivo = os.path.basename(ruta_original)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    nombre_procesado = f"{timestamp}_{nombre_archivo}"
    ruta_destino = os.path.join(PROCESSED_DIR, nombre_procesado)

    os.makedirs(PROCESSED_DIR, exist_ok=True)
    os.rename(ruta_original, ruta_destino)
    logger.info(f"Archivo movido a: {ruta_destino}")


def ejecutar_ciclo_procesamiento():
    """Ejecuta un ciclo completo de procesamiento de todos los archivos"""
    archivos = encontrar_archivos_excel()
    if not archivos:
        logger.warning("No se encontraron archivos para procesar")
        return

    for archivo in archivos:
        if procesar_archivo(archivo):
            mover_archivo_procesado(archivo)


def ejecutar_en_horario(hora_inicio_str: str, hora_fin_str: str, intervalo: int):
    """Controla el procesamiento en el horario especificado"""
    hora_inicio = parse_time(hora_inicio_str)
    hora_fin = parse_time(hora_fin_str)

    logger.info(f"\n{'=' * 40}")
    logger.info(f"Iniciando procesamiento programado")
    logger.info(f"Horario: {hora_inicio.strftime('%H:%M')} a {hora_fin.strftime('%H:%M')}")
    logger.info(f"Intervalo: {intervalo} segundos")
    logger.info(f"Directorio de entrada: {INPUT_DIR}")
    logger.info(f"Directorio de procesados: {PROCESSED_DIR}")
    logger.info(f"{'=' * 40}\n")

    try:
        while True:
            ahora = datetime.now().time()

            # Manejo especial para rangos que cruzan medianoche
            if hora_inicio < hora_fin:
                en_horario = hora_inicio <= ahora <= hora_fin
            else:
                en_horario = ahora >= hora_inicio or ahora <= hora_fin

            if en_horario:
                logger.info(f"Ciclo iniciado a las {ahora.strftime('%H:%M:%S')}")
                ejecutar_ciclo_procesamiento()

                logger.info(f"Esperando {intervalo} segundos...")
                time.sleep(intervalo)
            else:
                logger.info(f"Fuera del horario programado. Hora actual: {ahora.strftime('%H:%M:%S')}")
                time.sleep(60)  # Espera 1 minuto antes de volver a verificar

    except KeyboardInterrupt:
        logger.info("Procesamiento detenido por el usuario")
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}", exc_info=True)
        raise


def main():
    """Función principal"""
    parser = argparse.ArgumentParser(
        description="Procesador batch de archivos Excel con programación horaria",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        "start",
        help="Hora de inicio en formato HH:MM (24 horas)\nEjemplo: 06:00, 22:30"
    )
    parser.add_argument(
        "end",
        help="Hora de fin en formato HH:MM (24 horas)\nEjemplo: 18:00, 04:00"
    )
    parser.add_argument(
        "interval",
        type=int,
        help="Intervalo entre ejecuciones en segundos\nEjemplo: 3600 (1 hora), 1800 (30 min)"
    )

    args = parser.parse_args()

    # Validación adicional del intervalo
    if args.interval <= 0:
        logger.error("El intervalo debe ser un número positivo de segundos")
        exit(1)

    ejecutar_en_horario(args.start, args.end, args.interval)


if __name__ == "__main__":
    main()