FROM python:3.12-slim

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "uvicorn", "--factory", "main:create_app", "--port", "8000", "--host", "0.0.0.0" ]
