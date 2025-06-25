import time
from datetime import datetime, time as dt_time
import pandas as pd
import argparse
import os
import glob
from typing import List

# Configuración de directorios desde variables de entorno
INPUT_DIR = os.getenv('EXCEL_INPUT_DIR', './excel_input')
PROCESSED_DIR = os.getenv('PROCESSED_DIR', './processed')
LOG_FILE = os.getenv('LOG_FILE', './excel_processor.log')


def setup_logging():
    """Configura el logging para registrar todas las operaciones"""
    import logging
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger()


logger = setup_logging()


def encontrar_archivos_excel() -> List[str]:
    """Encuentra todos los archivos Excel en el directorio de entrada"""
    patrones = ('*.xlsx', '*.xls', '*.XLSX', '*.XLS')
    archivos = []
    for patron in patrones:
        archivos.extend(glob.glob(os.path.join(INPUT_DIR, patron)))
    return archivos


def procesar_archivo(ruta_archivo: str) -> bool:
    """Procesa un archivo Excel individual"""
    try:
        logger.info(f"Iniciando procesamiento de: {os.path.basename(ruta_archivo)}")

        # Leer el archivo Excel
        df = pd.read_excel(ruta_archivo)
        logger.info(f"Archivo {os.path.basename(ruta_archivo)} leído correctamente")

        # =============================================
        # AQUÍ VA TU LÓGICA PRINCIPAL DE PROCESAMIENTO
        # =============================================

        # Ejemplo: procesamiento básico
        print(f"\nContenido de {os.path.basename(ruta_archivo)}:")
        print(df.head())

        # Mover archivo procesado
        mover_archivo_procesado(ruta_archivo)
        return True

    except Exception as e:
        logger.error(f"Error al procesar {os.path.basename(ruta_archivo)}: {str(e)}")
        return False


def mover_archivo_procesado(ruta_original: str):
    """Mueve el archivo procesado al directorio correspondiente"""
    nombre_archivo = os.path.basename(ruta_original)
    nombre_procesado = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{nombre_archivo}"
    ruta_destino = os.path.join(PROCESSED_DIR, nombre_procesado)

    os.makedirs(PROCESSED_DIR, exist_ok=True)
    os.rename(ruta_original, ruta_destino)
    logger.info(f"Archivo movido a: {ruta_destino}")


def ejecutar_procesamiento(hora_inicio: dt_time, hora_fin: dt_time, intervalo: int):
    """Controla el procesamiento en el horario especificado"""
    while True:
        ahora = datetime.now().time()

        if hora_inicio <= ahora <= hora_fin:
            logger.info(f"Ciclo de procesamiento iniciado a las {ahora}")

            # Procesar todos los archivos encontrados
            archivos = encontrar_archivos_excel()
            if not archivos:
                logger.warning("No se encontraron archivos para procesar")
            else:
                for archivo in archivos:
                    procesar_archivo(archivo)

            logger.info(f"Esperando {intervalo} segundos para el próximo ciclo")
            time.sleep(intervalo)
        else:
            logger.info(f"Fuera del horario programado. Hora actual: {ahora}")
            time.sleep(60)  # Espera 1 minuto antes de volver a verificar


def main():
    """Función principal"""
    parser = argparse.ArgumentParser(description="Procesador batch de archivos Excel")

    parser.add_argument("start", help="Hora de inicio (formato HH:MM)")
    parser.add_argument("end", help="Hora de fin (formato HH:MM)")
    parser.add_argument("interval", type=int, help="Intervalo en segundos")

    args = parser.parse_args()

    # Convertir argumentos
    hora_inicio = dt_time(*map(int, args.start.split(':')))
    hora_fin = dt_time(*map(int, args.end.split(':')))

    logger.info("=== Iniciando procesamiento batch ===")
    logger.info(f"Horario: {args.start} a {args.end}")
    logger.info(f"Intervalo: {args.interval} segundos")
    logger.info(f"Directorio de entrada: {INPUT_DIR}")
    logger.info(f"Directorio de procesados: {PROCESSED_DIR}")

    try:
        ejecutar_procesamiento(hora_inicio, hora_fin, args.interval)
    except KeyboardInterrupt:
        logger.info("Procesamiento detenido por el usuario")
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}")
        raise


if __name__ == "__main__":
    main()