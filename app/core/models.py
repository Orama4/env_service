from sqlalchemy import Column, Integer, String, JSON, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.db import Base

class Environment(Base):
    __tablename__ = "Environment"  # Match the exact table name in the database
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    cords = Column(JSON, nullable=False)  # JSONB in PostgreSQL
    pathCartographie = Column(String(255), nullable=False)
    scale = Column(Integer, nullable=False)
    createdAt = Column(DateTime, nullable=False)
    env_users = relationship(
        "EnvUser",
        back_populates="environment",
        primaryjoin="Environment.id == EnvUser.envId"  # Explicit join condition
    )

class EnvUser(Base):
    __tablename__ = "EnvUser"  # Match the exact table name in the database
    id = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer, ForeignKey("User.id"), nullable=False)  # Foreign key to User
    envId = Column(Integer, ForeignKey("Environment.id"), nullable=False)  # Foreign key to Environment
    environment = relationship("Environment", back_populates="env_users")
    user = relationship("User", back_populates="env_users")

class User(Base):
    __tablename__ = "User"  # Match the exact table name in the database
    id = Column(Integer, primary_key=True, index=True)
    role = Column(String, nullable=False)
    createdAt = Column(DateTime, nullable=False)
    lastLogin = Column(DateTime, nullable=True)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    env_users = relationship("EnvUser", back_populates="user")
    profile = relationship("Profile", back_populates="user", uselist=False)  # One-to-One relationship


class Profile(Base):
    __tablename__ = "Profile"  # Match the exact table name in the database
    userId = Column(Integer, ForeignKey("User.id"), primary_key=True, nullable=False)  # Use userId as primary key
    firstname = Column(String, nullable=True)
    lastname = Column(String, nullable=True)
    phonenumber = Column(String, nullable=True)
    address = Column(String(255), nullable=True)  # Match the database column type
    user = relationship("User", back_populates="profile")  # Back reference to User