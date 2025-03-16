FROM python:3.11-slim

WORKDIR /init_db

COPY . /init_db

RUN pip install python-dotenv psycopg2-binary

CMD ["python3", "/init_db/create_db.py"]