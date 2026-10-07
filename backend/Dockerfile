FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

# uvicorn (ASGI) con varios workers. Render asigna el puerto en PORT.
# --proxy-headers: detras del proxy de Render la IP real del cliente llega
# en X-Forwarded-For (la usa el limite de peticiones)
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-5000} --workers ${WEB_CONCURRENCY:-2} --proxy-headers --forwarded-allow-ips='*'"]
