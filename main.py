import secrets
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import models, database, schemas

# Automatically create the tracker.db database and tables on startup
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="API Token & Usage Tracker")


@app.post("/tokens", response_model=schemas.TokenResponse)
def create_token(token_data: schemas.TokenCreate, db: Session = Depends(database.get_db)):
    # Generate a secure random token key (e.g. "tk_a1b2c3d4...")
    generated_key = f"tk_{secrets.token_hex(16)}"

    db_token = models.APIToken(
        token_key=generated_key,
        owner_name=token_data.owner_name
    )
    db.add(db_token)
    db.commit()
    db.refresh(db_token)

    return db_token


@app.get("/tokens", response_model=list[schemas.TokenResponse])
def get_all_tokens(db: Session = Depends(database.get_db)):
    return db.query(models.APIToken).all()
