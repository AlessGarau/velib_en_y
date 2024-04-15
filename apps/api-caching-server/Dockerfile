FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY ./apps/api-caching-server/ /app

EXPOSE 8004

CMD ["python3", "-m", "flask", "run", "--reload"]
