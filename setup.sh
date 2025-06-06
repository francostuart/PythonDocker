#!/bin/bash

echo "🧱 Preparando entorno..."
mkdir -p site && cd site
wget https://github.com/francostuart/PythonDocker/archive/refs/heads/vps.zip
unzip vps.zip
mv PythonDocker-vps/ProcessExcel.py .
cd ..

echo "🏃 Ejecutando Script Python..."
python3 ProcessExcel.py

echo ""
echo "✅ Ejecucion Satisfactoria"
echo ""
