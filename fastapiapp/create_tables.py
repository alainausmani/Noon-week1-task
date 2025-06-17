from test.context import Base, engine
from test.auth.models.tables import User  # ✅ ensures model is registered

def create_all_tables():
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully.")

if __name__ == "__main__":
    create_all_tables()
