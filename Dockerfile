FROM python:3.12-slim

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "uvicorn", "--factory", "main:create_app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--reload-exclude", "*", "--reload-include", "main.py" ]
