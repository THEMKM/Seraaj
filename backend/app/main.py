from fastapi import FastAPI

app = FastAPI(title="Seraaj API")

@app.get("/")
def read_root():
    return {"message": "Seraaj API"}
