from fastapi import FastAPI,  HTTPException, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from src.routes import contacts
from src.database.db import get_db

app = FastAPI()

app.include_router(contacts.router, prefix='/api')

@app.get('/')
def index():
    return {'message': 'Contacts'}

@app.get("/api/healthchecker")
def healthchecker(db: Session = Depends(get_db)):
    try:
        # Make request
        result = db.execute(text("SELECT 1")).fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail="Database is not configured correctly")
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")