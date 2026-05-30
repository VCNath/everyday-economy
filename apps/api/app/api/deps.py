from app.services.dashboard_service import DashboardService, dashboard_service
from app.database import get_db_session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from fastapi import Depends
from fastapi import HTTPException

from app.services.auth_service import AuthIdentity, get_current_identity
from app.services.user_service import UserService


def get_dashboard_service():
    db_generator = get_db_session()
    db = next(db_generator)
    try:
        try:
            db.execute(text("SELECT 1"))
        except SQLAlchemyError:
            db.close()
            yield dashboard_service
            return
        yield DashboardService(db)
    finally:
        try:
            next(db_generator)
        except StopIteration:
            pass


def get_db():
    db_generator = get_db_session()
    db = next(db_generator)
    try:
        yield db
    finally:
        try:
            next(db_generator)
        except StopIteration:
            pass


def get_current_user(identity: AuthIdentity = Depends(get_current_identity), db=Depends(get_db)):
    service = UserService(db)
    return service.get_or_create_user(identity)


def get_admin_user(current_user=Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required.")
    return current_user
