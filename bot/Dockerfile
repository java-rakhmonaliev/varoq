FROM python:3.12-slim

WORKDIR /app

RUN pip install aiogram asyncpg

COPY main.py .

CMD ["python", "main.py"]
