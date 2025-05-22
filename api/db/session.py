from sqlalchemy.orm import sessionmaker
from db.init_db import engine

# Create a session factory
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency to get the session
def get_db():
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()