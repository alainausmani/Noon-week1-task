from src.shared.db.session import Base, engine
from src.shared.models.tables import User
from src.shared.models.TaskTable import Task
from src.shared.models.MediaTable import Media

def create_all_tables():
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully.")

if __name__ == "__main__":
    create_all_tables()
