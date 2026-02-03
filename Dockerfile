FROM python:3.11-slim

WORKDIR /app

# Instala sqlite3 (opcional, Python já tem sqlite3 embutido)
RUN apt-get update && apt-get install -y sqlite3 && rm -rf /var/lib/apt/lists/*

# Copia e instala dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código
COPY ./app /app

CMD ["python", "main.py"]
