# Proyecto Procesamiento Segundo Plano

## Descripción
Este proyecto combina dos funcionalidades principales:
1. **Procesamiento de archivos Excel**: Un script que permite programar la lectura y procesamiento de archivos Excel en intervalos específicos dentro de un rango horario definido.
2. **API de Web Scraping**: Una API basada en FastAPI que proporciona endpoints para realizar web scraping utilizando Selenium, capturar pantallas de sitios web y listar las capturas realizadas.

## Tecnologías Utilizadas
- **Python 3.11**: Lenguaje de programación principal
- **Pandas**: Para el procesamiento de archivos Excel
- **FastAPI**: Framework para crear la API REST
- **Uvicorn**: Servidor ASGI para ejecutar la aplicación FastAPI
- **Selenium 4.18.0**: Para automatización de navegadores y web scraping
- **Webdriver-Manager 4.0.2**: Para gestionar la instalación de webdrivers
- **Docker**: Para la contenerización de la aplicación

## Requisitos
- Python 3.11 o superior
- Docker (opcional, para ejecutar en contenedor)
- Navegador Chromium (para la funcionalidad de web scraping)

## Instalación

### Opción 1: Instalación Local
1. Clonar el repositorio:
   ```bash
   git clone https://github.com/francostuart/PythonDocker.git
   cd PythonDocker
   ```

2. Crear un entorno virtual (opcional pero recomendado):
   ```bash
   python -m venv mi_entorno
   source mi_entorno/bin/activate  # En Windows: mi_entorno\Scripts\activate
   ```

3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   pip install pandas  # Asegúrate de instalar pandas que no está en requirements.txt
   ```

### Opción 2: Usando Docker
1. Construir la imagen Docker:
   ```bash
   docker build -t python-docker .
   ```

2. Ejecutar el contenedor:
   ```bash
   docker run -p 8000:8000 python-docker
   ```

### Opción 3: Usando el script de configuración
1. Dar permisos de ejecución al script:
   ```bash
   chmod +x setup.sh
   ```

2. Ejecutar el script:
   ```bash
   ./setup.sh
   ```

## Uso

### Procesamiento de Archivos Excel
El script `ProcessExcel.py` permite programar la lectura de archivos Excel en intervalos específicos dentro de un rango horario:

```bash
python ProcessExcel.py input.xlsx 9:30 18:30 300
```

Donde:
- `input.xlsx`: Ruta al archivo Excel a procesar
- `9:30`: Hora de inicio (formato HH:MM)
- `18:30`: Hora de fin (formato HH:MM)
- `300`: Intervalo en segundos (en este ejemplo, 5 minutos)

### API de Web Scraping
La API proporciona los siguientes endpoints:

1. **Página principal**:
   ```
   GET /
   ```
   Devuelve un mensaje de bienvenida.

2. **Realizar web scraping**:
   ```
   GET /scrap
   ```
   Realiza web scraping en una página específica y guarda una captura de pantalla.

3. **Listar capturas**:
   ```
   GET /list
   ```
   Lista todas las capturas de pantalla realizadas.

Para iniciar la API:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Estructura del Proyecto
- `ProcessExcel.py`: Script para procesamiento programado de archivos Excel
- `main.py`: Aplicación FastAPI para web scraping
- `Dockerfile`: Configuración para contenerización con Docker
- `requirements.txt`: Dependencias del proyecto
- `setup.sh`: Script de configuración automatizada
- `capturas/`: Directorio donde se guardan las capturas de pantalla

## Notas Adicionales
- El script de procesamiento Excel se ejecutará solo dentro del rango horario especificado
- La API de web scraping está configurada para trabajar con Chromium en modo headless
- Para entornos de producción, considere configurar adecuadamente los parámetros de seguridad

<!-- Este es un comentario en Markdown 
#sudo    find / -name "mi_entorno"
#source mi_entorno/bin/activate
#python3 ./ProcessExcel.py input.xlsx 9:30 6:30 300
-->