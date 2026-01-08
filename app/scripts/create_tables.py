from app.database.session import engine, Base
from app.database import models

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("Tables created")
