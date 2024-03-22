FROM python:3.11.8-alpine3.19

RUN apk update && \
    apk add --no-cache git

EXPOSE 5000

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY wsgi.py config.py application/ ./

CMD ["python", "wsgi.py"]