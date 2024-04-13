FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY ./apps/microservices/user/ /app

EXPOSE 8003

CMD ["python3", "-m", "flask", "run"]