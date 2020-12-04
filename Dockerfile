FROM python:3.8

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src ./src

WORKDIR /app/src
EXPOSE 8000
ENTRYPOINT ["uvicorn", "webserver:api", "--port", "8000", "--host", "0.0.0.0"]