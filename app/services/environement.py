from fastapi import UploadFile  # Add this import
from fastapi import HTTPException
import os
import json
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.core.models import Environment, User,EnvUser,Profile
from app.schemas.environement import EnvironmentCreate
from app.schemas.environement import EnvironmentUpdate


def create_environment(db: Session, env: EnvironmentCreate):
    # Debug: print incoming environment data
    print(
        f"Creating environment with "
        f"name={env.name!r}, address={env.address!r}, cords={env.cords!r}, "
        f"pathCartographie={env.pathCartographie!r}, scale={env.scale!r}")
    # Parse cords field if it's a JSON string (handle nested encoding)
    cords = env.cords
    if isinstance(cords, str):
        try:
            attempts = 0
            while isinstance(cords, str) and attempts < 3:  # Prevent infinite loops
                cords = json.loads(cords)
                attempts += 1
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid cords format")

    # Final check
    if not isinstance(cords, dict):
        raise HTTPException(status_code=400, detail="Cords must be a GeoJSON object")

    new_env = Environment(
    name=env.name,
    address=env.address,
    cords=cords,
    pathCartographie=env.pathCartographie,
    scale=env.scale,
    createdAt=datetime.now(timezone.utc)  # set timezone-aware UTC datetime
    )
    db.add(new_env)
    db.commit()
    db.refresh(new_env)
    # Debug: print created Environment object
    print(f"Created Environment: id={new_env.id}, name={new_env.name!r}, address={new_env.address!r}, "
          f"cords={new_env.cords!r}, pathCartographie={new_env.pathCartographie!r}, scale={new_env.scale!r}")
    return new_env

import json

def get_environment_by_id(db: Session, env_id: int):
    env = db.query(Environment).filter(Environment.id == env_id).first()
    if not env:
        raise HTTPException(status_code=404, detail="Environment not found")

    # Deserialize cords field if it's a string
    cords = env.cords
    if isinstance(cords, str):
        try:
            cords = json.loads(cords)
        except json.JSONDecodeError:
            print(f"❌ Error decoding cords for env id={env.id}")
            cords = {}

    return {
        "id": env.id,
        "name": env.name,
        "address": env.address,
        "cords": cords,  # Ensure cords is included and is a dictionary
        "pathCartographie": env.pathCartographie,
        "scale": env.scale,
        "createdAt": env.createdAt.isoformat(),  # Convert datetime to ISO 8601 string
    }

def update_environment(db: Session, env_id: int, update_data: EnvironmentUpdate):
    env = db.query(Environment).filter(Environment.id == env_id).first()
    if not env:
        raise HTTPException(status_code=404, detail="Environment not found")
    
    for field, value in update_data.dict(exclude_unset=True).items():
        setattr(env, field, value)
    
    db.commit()
    db.refresh(env)
    return env

async def save_uploaded_file(file: UploadFile) -> str:
    """Save an uploaded file and return the file path"""
    # Create uploads directory if it doesn't exist
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    
    # Create a unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{file.filename}"
    file_path = os.path.join(upload_dir, filename)
    
    # Save the file
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    
    return file_path

def delete_environment(db: Session, env_id: int):
    env = db.query(Environment).filter(Environment.id == env_id).first()
    if not env:
        raise HTTPException(status_code=404, detail="Environment not found")
    
    db.delete(env)
    db.commit()
    return {"message": f"Environment with id {env_id} has been deleted"}

import json

import json

def get_all_environments(db: Session):
    print("🔍 Fetching all environments from DB")
    try:
        # Fetch all environments
        environments = db.query(Environment).all()
        print(f"✅ Retrieved {len(environments)} environments")
    except Exception as e:
        print(f"❌ Error fetching environments: {e}")
        raise HTTPException(status_code=500, detail="Error fetching environments")

    result = []
    for env in environments:
        print(f"📦 Processing Environment id={env.id}, name={env.name!r}")
        try:
            # Fetch users associated with the environment
            users = (
                db.query(User)
                .join(EnvUser, EnvUser.userId == User.id)
                .filter(EnvUser.envId == env.id)
                .all()
            )
            print(f"   👥 Found {len(users)} users for env id={env.id}")
        except Exception as e:
            print(f"   ❌ Error fetching users for env id={env.id}: {e}")
            users = []
        # Append environment and user data to the result
        result.append({
            "id": env.id,
            "name": env.name,
            "address": env.address,
            "pathCartographie": env.pathCartographie,
            "scale": env.scale,
            "createdAt": env.createdAt.isoformat(),  # Convert datetime to ISO 8601 string
            "users": [
                {
                    "id": user.id,
                    "role": user.role,
                    "email": user.email,
                    "createdAt": user.createdAt.isoformat(),  # Convert datetime to ISO 8601 string
                    "lastLogin": user.lastLogin.isoformat() if user.lastLogin else None  # Handle nullable field
                }
                for user in users
            ]
        })

    print("🏁 Completed get_all_environments, returning result")
    return result

# filepath: environement.py
from sqlalchemy.orm import joinedload

def get_users_with_normal_role(db: Session):
    users = (
        db.query(User)
        .options(joinedload(User.profile))
        .filter(User.role == "normal")
        .all()
    )
    return [
        {
            "id": u.id,
            "email": u.email,
            "role": u.role,
            "firstname": u.profile.firstname if u.profile else None,
            "lastname": u.profile.lastname if u.profile else None,
            "createdAt": u.createdAt.isoformat(),
            "lastLogin": u.lastLogin.isoformat() if u.lastLogin else None
        }
        for u in users
    ]

def assign_user_to_environment(db: Session, user_id: int, env_id: int, assign: bool = True):
    # Check if the user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if the environment exists
    environment = db.query(Environment).filter(Environment.id == env_id).first()
    if not environment:
        raise HTTPException(status_code=404, detail="Environment not found")

    existing = (
        db.query(EnvUser)
        .filter(EnvUser.userId == user_id, EnvUser.envId == env_id)
        .first()
    )

    # Debug print
    print("assign:", assign, existing)

    if assign:
        if existing:
            raise HTTPException(status_code=400, detail="User already assigned")
        assignment = EnvUser(userId=user_id, envId=env_id)
        db.add(assignment)
        db.commit()
        return {"message": f"User {user_id} assigned to environment {env_id}"}
    else:
        if not existing:
            raise HTTPException(status_code=400, detail="Assignment not found")
        db.delete(existing)
        db.commit()
        return {"message": f"User {user_id} removed from environment {env_id}"}