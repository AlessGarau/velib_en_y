FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY ./apps/microservices/favorite/ /app/favorite
COPY ./database_access_layer/ /app/database_access_layer

EXPOSE 8002

WORKDIR /app/favorite

CMD ["python3", "-m", "flask", "run", "--reload"]
