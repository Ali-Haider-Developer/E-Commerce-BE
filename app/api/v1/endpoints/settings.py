from typing import List, Optional, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.api import deps

router = APIRouter()

@router.get("/admin", response_model=List[schemas.SettingsResponse])
def read_settings(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: schemas.User = Depends(deps.get_current_active_superuser),
):
    """
    Retrieve settings (admin only).
    """
    settings = crud.settings.get_multi(db, skip=skip, limit=limit)
    return settings

@router.post("/admin", response_model=schemas.SettingsResponse)
def create_setting(
    *,
    db: Session = Depends(deps.get_db),
    setting_in: schemas.SettingsCreate,
    current_user: schemas.User = Depends(deps.get_current_active_superuser),
):
    """
    Create new setting (admin only).
    """
    setting = crud.settings.create(db=db, obj_in=setting_in)
    return setting

@router.put("/admin/{setting_id}", response_model=schemas.SettingsResponse)
def update_setting(
    *,
    db: Session = Depends(deps.get_db),
    setting_id: int,
    setting_in: schemas.SettingsUpdate,
    current_user: schemas.User = Depends(deps.get_current_active_superuser),
):
    """
    Update a setting (admin only).
    """
    setting = crud.settings.get(db=db, id=setting_id)
    if not setting:
        raise HTTPException(status_code=404, detail="Setting not found")
    setting = crud.settings.update(db=db, db_obj=setting, obj_in=setting_in)
    return setting

@router.delete("/admin/{setting_id}")
def delete_setting(
    *,
    db: Session = Depends(deps.get_db),
    setting_id: int,
    current_user: schemas.User = Depends(deps.get_current_active_superuser),
):
    """
    Delete a setting (admin only).
    """
    setting = crud.settings.get(db=db, id=setting_id)
    if not setting:
        raise HTTPException(status_code=404, detail="Setting not found")
    setting = crud.settings.remove(db=db, id=setting_id)
    return {"ok": True}

@router.get("/", response_model=List[schemas.SettingsResponse])
def read_public_settings(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: schemas.User = Depends(deps.get_current_user),
):
    """
    Retrieve public settings.
    """
    settings = crud.settings.get_multi(db, skip=skip, limit=limit)
    return settings

@router.get("/{key}", response_model=Any)
def read_setting_by_key(
    *,
    db: Session = Depends(deps.get_db),
    key: str,
    current_user: schemas.User = Depends(deps.get_current_user),
):
    """
    Get setting value by key.
    """
    setting = crud.settings.get_by_key(db=db, key=key)
    if not setting:
        raise HTTPException(status_code=404, detail="Setting not found")
    return setting.value 