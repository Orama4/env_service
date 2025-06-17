from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse
from fastapi import Depends
from app.services.prediction import handle_prediction
from app.models.loader import loaded_models
from sqlalchemy.orm import Session
from app.core.db import SessionLocal
from app.schemas.environement import EnvironmentCreate, EnvironmentResponse, EnvironmentOut
from app.services.environement import create_environment, save_uploaded_file
from app.core.db import get_db   
from app.services.environement import get_environment_by_id
from app.schemas.environement import EnvironmentUpdate
from app.services.environement import update_environment
from app.schemas.environement import UserResponse
from typing import List
from app.services.environement import get_all_environments
from app.services.environement import delete_environment,get_users_with_normal_role,assign_user_to_environment
import json
from typing import Optional




router = APIRouter()

@router.get("/")
def root():
    available_models = [k for k, v in loaded_models.items() if v is not None]
    return {
        "message": "Multi-Model Detection API is running!",
        "available_models": available_models,
    }

@router.post("/predict/{model_id}/")
async def predict(model_id: str, file: UploadFile = File(...)):
    try:
        return await handle_prediction(model_id, file)
    except HTTPException as e:
        raise e


@router.post("/env/", response_model=EnvironmentOut)
async def create_environment_route(
    env_data: str = Form(...),
    envID: Optional[int] = Form(None),
    db: Session = Depends(get_db)
):
    try:
        # debug log
        print("Debug env_data:", env_data)

        # parse JSON payload
        env_dict = json.loads(env_data)
        env = EnvironmentCreate(**env_dict)  # validate input

        # decide between create or update
        if envID:
            return update_environment(db, envID, env)
        return create_environment(db=db, env=env)

    except json.JSONDecodeError as je:
        raise HTTPException(status_code=400, detail="Invalid JSON in env_data")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving environment: {e}")
    
    
@router.get("/env/{env_id}", response_model=EnvironmentOut)
def read_environment(env_id: int, db: Session = Depends(get_db)):
    return get_environment_by_id(db, env_id)

@router.put("/env/{env_id}", response_model=EnvironmentOut)
def update_environment_route(env_id: int, update_data: EnvironmentUpdate, db: Session = Depends(get_db)):
    return update_environment(db, env_id, update_data)


@router.get("/env/{env_id}/assign-user/{user_id}")
def assign_user_route(
    env_id: int,
    user_id: int,
    assign: bool = True,
    db: Session = Depends(get_db)
):
    return assign_user_to_environment(db, user_id, env_id, assign)


@router.delete("/env/{env_id}")
def delete_environment_route(env_id: int, db: Session = Depends(get_db)):
    return delete_environment(db, env_id)



@router.get("/env/", response_model=List[EnvironmentResponse])
def get_all_environments_route(db: Session = Depends(get_db)):
    return get_all_environments(db)

@router.get("/users/normal", response_model=List[UserResponse])
def fetch_users_with_normal_role(db: Session = Depends(get_db)):
    return get_users_with_normal_role(db)