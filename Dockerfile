# Usamos imagen base oficial Python 3.11 slim
FROM python:3.11-slim

# Instalamos dependencias de sistema + Chromium
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    gnupg \
    ca-certificates \
    fonts-liberation \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxrandr2 \
    libasound2 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libgbm-dev \
    xdg-utils \
    chromium \
    chromium-driver \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Instalamos Python packages
RUN pip install --no-cache-dir selenium webdriver-manager fastapi uvicorn

# Copiamos tu código
WORKDIR /app
COPY . /app

# Ejecutamos la app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
