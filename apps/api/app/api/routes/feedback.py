from fastapi import APIRouter, Depends, Header, HTTPException, Query, Request

from app.api.deps import get_admin_user, get_db
from app.schemas.feedback import FeedbackCreate, FeedbackListResponse, FeedbackResponse, FeedbackUpdate
from app.services.admin_audit_service import AdminAuditService
from app.services.auth_service import get_current_identity
from app.services.feedback_service import FeedbackService
from app.services.user_service import UserService

router = APIRouter(tags=["feedback"])
admin_router = APIRouter(prefix="/admin", tags=["admin"])


def _row_to_response(row) -> FeedbackResponse:
    return FeedbackResponse(
        id=row.id,
        user_id=row.user_id,
        page_path=row.page_path,
        feedback_type=row.feedback_type,
        rating=row.rating,
        message=row.message,
        email=row.email,
        metadata=row.metadata_json,
        status=row.status,
        created_at=row.created_at.isoformat(),
        updated_at=row.updated_at.isoformat(),
    )


def _optional_user_id(authorization: str | None, db) -> str | None:
    if not authorization:
        return None
    try:
        identity = get_current_identity(authorization=authorization)
        return UserService(db).get_or_create_user(identity).id
    except HTTPException:
        return None


@router.post("/feedback", response_model=FeedbackResponse)
def submit_feedback(
    payload: FeedbackCreate,
    request: Request,
    authorization: str | None = Header(default=None),
    db=Depends(get_db),
):
    metadata = payload.metadata or {}
    metadata.setdefault("userAgent", request.headers.get("user-agent", ""))
    row = FeedbackService(db).create(
        user_id=_optional_user_id(authorization, db),
        page_path=payload.page_path,
        feedback_type=payload.feedback_type,
        rating=payload.rating,
        message=payload.message,
        email=str(payload.email) if payload.email else None,
        metadata=metadata,
    )
    return _row_to_response(row)


@admin_router.get("/feedback", response_model=FeedbackListResponse)
def list_feedback(
    status: str | None = Query(default=None),
    feedback_type: str | None = Query(default=None),
    limit: int = 100,
    _admin=Depends(get_admin_user),
    db=Depends(get_db),
):
    return FeedbackListResponse(items=[_row_to_response(row) for row in FeedbackService(db).list(status=status, feedback_type=feedback_type, limit=limit)])


@admin_router.put("/feedback/{feedback_id}", response_model=FeedbackResponse)
def update_feedback(
    feedback_id: str,
    payload: FeedbackUpdate,
    admin_user=Depends(get_admin_user),
    db=Depends(get_db),
):
    try:
        row = FeedbackService(db).update_status(feedback_id, payload.status)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if row is None:
        raise HTTPException(status_code=404, detail="Feedback not found.")
    AdminAuditService(db).log(
        user_id=admin_user.id,
        action="admin.feedback.update",
        entity_type="beta_feedback",
        entity_id=feedback_id,
        details={"status": payload.status},
    )
    return _row_to_response(row)
