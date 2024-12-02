FROM python:3.10-slim-buster
WORKDIR /app 
COPY . /app 

RUN apt update -y && apt install awscli -y 
RUN apt-get update && pip install -r requirements.txt && pip install --upgrade pymongo
CMD ["python", "app.py"]
