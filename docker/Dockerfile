FROM python:3.5.2-alpine

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY src/ /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD [ "python", "./main.py" ]
