FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY initial_data_quotes.csv .

EXPOSE 5002

CMD ["python", "app.py"]