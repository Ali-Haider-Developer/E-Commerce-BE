from typing import Dict, Any, Optional
from pydantic import BaseModel
from datetime import datetime

class SettingsBase(BaseModel):
    key: str
    value: Any
    description: Optional[str] = None

class SettingsCreate(SettingsBase):
    pass

class SettingsUpdate(SettingsBase):
    key: Optional[str] = None
    value: Optional[Any] = None
    description: Optional[str] = None

class SettingsInDBBase(SettingsBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Settings(SettingsInDBBase):
    pass

class SettingsResponse(SettingsInDBBase):
    pass 