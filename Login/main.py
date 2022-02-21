import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from models import dbmodels
from models.dbconfig import engine
from models.dbconfig import get_db
from routes import users, records, auth, ranking, notification
from routes.auth import oauth2_scheme

dbmodels.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def validate_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return await auth.get_current_user(token, db)


app.include_router(
    auth.router,
    prefix="/v1/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)
app.include_router(
    users.router,
    prefix="/v1/users",
    tags=["users"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

app.include_router(
    records.router,
    prefix="/v1/records",
    tags=["records"],
    dependencies=[Depends(validate_user)],
    responses={404: {"description": "Not found"}},
)

app.include_router(
    ranking.router,
    prefix="/v1/ranking",
    tags=["ranking"],
    dependencies=[Depends(validate_user)],
    responses={404: {"description": "Not found"}},
)
app.include_router(
    notification.router,
    prefix="/v1/notification",
    tags=["notification"],
    dependencies=[Depends(validate_user)],
    responses={404: {"description": "Not found"}},
)


@app.get("/")
async def home():
    return {"message": "Hi!"}


if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8000)
