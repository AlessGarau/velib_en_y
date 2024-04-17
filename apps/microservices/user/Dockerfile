FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY ./apps/microservices/user/ /app/user
COPY ./database_access_layer/ /app/database_access_layer

EXPOSE 8003

WORKDIR /app/user

CMD ["python3", "-m", "flask", "run", "--reload"]
