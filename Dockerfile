# Usamos imagen base oficial Python 3.11 slim
FROM python:3.11-slim

# Instalamos dependencias para Chrome + Selenium
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
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Instalamos Google Chrome DEB de forma robusta - esta linea se esta probando para el CI de Jenkins
RUN curl -sSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# Instalamos Chromium versión 120 - esta linea funciona bien como imagen directamente con docker
#RUN curl -sSL https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o google-chrome.deb && \
#    apt-get update && apt-get install -y ./google-chrome.deb && \
#    rm google-chrome.deb

# Instalamos Python packages
RUN pip install --no-cache-dir selenium webdriver-manager fastapi uvicorn

# Copiamos tu código
WORKDIR /app
COPY . /app

# Comando por defecto para tu app
#CMD ["python", "main.py"]
#CMD ["sh", "-c", "python main.py; tail -f /dev/null"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]