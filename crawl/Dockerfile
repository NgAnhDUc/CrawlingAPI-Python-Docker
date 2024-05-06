FROM python:3.9.16-slim
WORKDIR /app
COPY . .
RUN pip install requests mysql-connector-python
CMD [ "python","crawl.py"]