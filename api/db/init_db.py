from sqlalchemy import create_engine
from dotenv import load_dotenv
from db.models import Base
import os


# Load environment variables
load_dotenv()

# Connection URL for the database
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
