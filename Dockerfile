FROM python:3.13.3
WORKDIR /app
COPY . /app

RUN apt update -y && apt install awscli -y
RUN apt- get update && pip install -r requirement.txt
CMD ["python", "app.py"]
