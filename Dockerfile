FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend backend

# Porta usada pelo Cloud Run
ENV PORT=8080

CMD ["gunicorn", "-b", "0.0.0.0:8080", "backend.dashboard.app:server"]
