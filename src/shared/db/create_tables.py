from shared.db.session import Base, engine
from shared.models.tables import User
from shared.models.TaskTable import Task
from shared.models.MediaTable import Media


def create_all_tables():
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully.")


if __name__ == "__main__":
    create_all_tables()
