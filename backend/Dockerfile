#Stage-1

FROM python:3.9-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --user --no-cache-dir -r requirements.txt

COPY . .

#Stage-2

FROM python:3.9-slim

WORKDIR /app

COPY --from=builder /root/.local /root/.local

COPY --from=builder /app .

EXPOSE 5000

CMD ["python","app.py"] 
