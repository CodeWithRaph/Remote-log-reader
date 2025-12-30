FROM python:3.14-alpine

WORKDIR /app_logs

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "run.py"]