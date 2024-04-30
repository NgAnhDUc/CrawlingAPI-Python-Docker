FROM python:3.9.16-slim
COPY . ./api
RUN pip install fastapi uvicorn
WORKDIR /api
CMD [ "uvicorn","db_api:app","--host","0.0.0.0","--port","8000" ]
