from sqlalchemy import create_engine
from SocialScores.Models.Account import Base as AccountBase
from SocialScores.Models.Post import Base as PostBase

database_engine = 'postgres'
connection_string = 'postgresql://postgres:admin@database:5432/socialscores'  # Use full connection URL

def start():
    """
    Initialize the database by creating required tables using SQLAlchemy's Base.metadata.create_all()
    """
    print("Connecting to the database...")
    engine = create_engine(connection_string)

    try:
        print("Creating tables...")
        # Create all tables defined in the ORM models
        AccountBase.metadata.create_all(engine)
        PostBase.metadata.create_all(engine)
        print("Tables created successfully.")
    except Exception as e:
        print(f"Error creating tables: {e}")
    finally:
        print("Database initialization complete.")
