from fastapi import FastAPI

app = FastAPI(
    title="PhotoShare API"
)

@app.get("/")
def root():

    return {
        "message": "PhotoShare working"
    }