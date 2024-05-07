FROM python:3.9.16-slim
WORKDIR /app

RUN pip install requests mysql-connector-python schedule fastapi

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7000"]
