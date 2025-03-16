from fastapi import FastAPI
import psycopg2

app = FastAPI()
@app.get("/test")
def test():
    return "ok"