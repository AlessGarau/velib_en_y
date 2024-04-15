FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY ./apps/microservices/favorite/ /app

EXPOSE 8002

CMD ["python3", "-m", "flask", "run", "--reload"]
