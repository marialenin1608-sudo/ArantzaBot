FROM python:3.10-slim

WORKDIR /code

# Actualización de certificados para evitar el error NameResolutionError
RUN apt-get update && apt-get install -y ca-certificates && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app.py"]
