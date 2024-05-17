FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# ENV BOT_TOKEN=<your-bot-token> (uncomment and use for static token setting)

CMD ["python", "main.py"]