from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from app.models.settings import Settings
from app.schemas.settings import SettingsCreate, SettingsUpdate
from app.crud.base import CRUDBase

class CRUDSettings(CRUDBase[Settings, SettingsCreate, SettingsUpdate]):
    def get_by_key(self, db: Session, *, key: str) -> Optional[Settings]:
        return db.query(Settings).filter(Settings.key == key).first()

    def get_value(self, db: Session, *, key: str) -> Optional[Dict[str, Any]]:
        settings = self.get_by_key(db, key=key)
        return settings.value if settings else None

    def set_value(self, db: Session, *, key: str, value: Dict[str, Any]) -> Settings:
        settings = self.get_by_key(db, key=key)
        if settings:
            settings.value = value
        else:
            settings = Settings(key=key, value=value)
            db.add(settings)
        db.commit()
        db.refresh(settings)
        return settings

    def delete_by_key(self, db: Session, *, key: str) -> bool:
        settings = self.get_by_key(db, key=key)
        if not settings:
            return False
        db.delete(settings)
        db.commit()
        return True

settings = CRUDSettings(Settings) 