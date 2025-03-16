FROM python:3.9-slim

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt
RUN pip install prometheus_client pyrate-limiter tenacity pytest python-telegram-bot

# Configurar PYTHONPATH para incluir o diretório raiz
ENV PYTHONPATH="${PYTHONPATH}:/app"

EXPOSE 8000
CMD ["python", "main.py"] 