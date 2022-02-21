import os

from models import dbmodels, crud, schemas
from models.dbconfig import SessionLocal
from models.dbconfig import engine

if __name__ == "__main__":
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    if os.path.isfile(cur_dir + '/sql_app.db'):
        os.remove(cur_dir + '/sql_app.db')

    dbmodels.Base.metadata.create_all(bind=engine)

    session = SessionLocal()
    user = schemas.UserCreate(username="admin",
                              nick_name="admin",
                              password="admin",
                              date_of_birth="1993-08-10",
                              avatar="default.jpg"
                              )
    crud.create_user(session, user)
