import os
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from app.core.models import Base, Environment, EnvUser, User

# Load environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# Create database engine
engine = create_engine(DATABASE_URL)

# Seed data
def seed_database():
    with Session(engine) as session:
        # Seed Users
        user1 = User(id=1, status="active", createdAt="2025-06-16")
        user2 = User(id=2, status="inactive", createdAt="2025-06-16")
        session.add_all([user1, user2])

        # Seed Environments
        env1 = Environment(
            id=1,
            name="Environment 1",
            address="123 Main St",
            cords={"lat": 40.7128, "lng": -74.0060},
            pathCartographie="/path/to/cartography1",
            scale=1,
            createdAt="2025-06-16",
        )
        env2 = Environment(
            id=2,
            name="Environment 2",
            address="456 Elm St",
            cords={"lat": 34.0522, "lng": -118.2437},
            pathCartographie="/path/to/cartography2",
            scale=2,
            createdAt="2025-06-16",
        )
        session.add_all([env1, env2])

        # Seed EnvUser
        env_user1 = EnvUser(userId=1, envId=1)
        env_user2 = EnvUser(userId=2, envId=2)
        session.add_all([env_user1, env_user2])

        # Commit changes
        session.commit()
        print("✅ Database seeded successfully!")

if __name__ == "__main__":
    seed_database()