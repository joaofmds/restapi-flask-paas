FROM python:3.11.8-alpine3.19

RUN apk update && \
    apk add --no-cache git

EXPOSE 5000

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY application application
COPY wsgi.py config.py ./
 
CMD [ "python", "wsgi.py" ]