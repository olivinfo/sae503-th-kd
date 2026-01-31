
FROM python:3.9-alpine

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY initial_data_users.csv .

RUN adduser -D appuser
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 CMD wget --no-verbose --tries=1 --spider http://localhost:5001/ || exit 1
USER appuser

EXPOSE 5001

CMD ["python", "app.py"]