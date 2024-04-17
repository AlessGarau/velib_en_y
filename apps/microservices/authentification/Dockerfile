FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY ./apps/microservices/authentification/ /app/authentification
COPY ./database_access_layer/ /app/database_access_layer

EXPOSE 8001

WORKDIR /app/authentification

CMD ["python3", "-m", "flask", "run", "--reload"]
