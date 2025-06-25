from src.libauth.context import Base, engine
from src.libauth.models.tables import User 
from src.libauth.models.TaskTable import Task
from src.libauth.models.MediaTable import Media

def create_all_tables():
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully.")

if __name__ == "__main__":
    create_all_tables()
