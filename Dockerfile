# Dockerfile
FROM python:3.9-slim

WORKDIR /project

COPY requirements.txt .

RUN apt-get update && apt-get install -y gcc libffi-dev musl-dev python3-dev

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
