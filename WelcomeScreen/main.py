from fastapi import FastAPI

app = FastAPI(title="API Token & Usage Tracker")

@app.get("/")
def home():
    return {"message": "API Token Tracker is live!"}
