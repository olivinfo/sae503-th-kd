FROM python:3.9-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY initial_data_quotes.csv .

RUN adduser -D appuser
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 CMD wget --no-verbose --tries=1 --spider http://localhost:5002/ || exit 1
USER appuser

EXPOSE 5002

CMD ["python", "app.py"]