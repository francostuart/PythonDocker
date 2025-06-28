#!/bin/bash

# Configuración básica
PROJECT_DIR="site"
VENV_NAME="excel_venv"
PYTHON_SCRIPT="ProcessExcel.py"
REQUIREMENTS="pandas openpyxl"
REPO_URL="https://github.com/francostuart/PythonDocker/archive/refs/heads/vps.zip"

# Configuración de directorios (pueden sobrescribirse con variables de entorno)
export EXCEL_INPUT_DIR="${EXCEL_INPUT_DIR:-/Users/ricardobuenobalbis/Desktop/sh/input}"
export PROCESSED_DIR="${PROCESSED_DIR:-/Users/ricardobuenobalbis/Desktop/sh/output}"
export LOG_FILE="${LOG_FILE:-/Users/ricardobuenobalbis/Desktop/sh/log/excel_processor.log}"

# Función para registro de logs
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "=== Inicio de configuración del entorno ==="

# Crear directorios necesarios
mkdir -p "$EXCEL_INPUT_DIR" "$PROCESSED_DIR"
log "Directorios de entrada y procesados verificados"

# Descargar y actualizar el código fuente
log "Descargando código fuente desde GitHub..."
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR" || exit

if wget -q --show-progress "$REPO_URL" -O repo.zip; then
    if unzip -q -o repo.zip; then
        mv -f PythonDocker-vps/"$PYTHON_SCRIPT" .
        log "Código fuente actualizado correctamente"
        rm -f repo.zip
        rm -rf PythonDocker-vps
    else
        log "❌ Error al descomprimir el repositorio"
        exit 1
    fi
else
    log "❌ Error al descargar el repositorio"
    exit 1
fi

cd ..

# Configurar entorno virtual
if [ ! -d "$VENV_NAME" ]; then
    log "Creando entorno virtual..."
    if python3 -m venv "$VENV_NAME"; then
        source "$VENV_NAME"/bin/activate
        log "Instalando dependencias..."
        pip install --upgrade pip && pip install $REQUIREMENTS || {
            log "❌ Error al instalar dependencias";
            exit 1;
        }
    else
        log "❌ Error al crear el entorno virtual"
        exit 1
    fi
else
    source "$VENV_NAME"/bin/activate
    log "Entorno virtual existente activado"
fi

# Verificar parámetros
if [ "$#" -ne 3 ]; then
    log "Uso: $0 <hora_inicio> <hora_fin> <intervalo_minutos>"
    log "Ejemplo: $0 08:00 17:00 30"
    exit 1
fi

# Ejecutar el script Python principal
log "Iniciando procesamiento con parámetros: $1 $2 $3"
python3 "$PROJECT_DIR/$PYTHON_SCRIPT" "$1" "$2" "$3"

log "=== Proceso completado ==="