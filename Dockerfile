FROM python:3.10-alpine

WORKDIR /root/dev

COPY requirements.txt src/* ./
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "main.py"]