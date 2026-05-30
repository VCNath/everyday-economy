from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import get_current_user, get_db
from app.models.economic import LocationModel, UserModel
from app.schemas.user import (
    SavedRegion,
    SavedRegionRequest,
    UpdateUserPreferencesRequest,
    UpdateUserProfileRequest,
    UserPreferences,
    UserProfile,
    WatchlistRegion,
)
from app.services.preferences_service import PreferencesService
from app.services.saved_regions_service import SavedRegionsService
from app.services.user_service import UserService
from app.services.watchlist_service import WatchlistService

router = APIRouter(prefix="/me", tags=["me"])


@router.get("", response_model=UserProfile)
def get_me(current_user: UserModel = Depends(get_current_user)):
    return UserProfile(
        id=current_user.id,
        email=current_user.email,
        display_name=current_user.display_name,
        avatar_url=current_user.avatar_url,
        role=current_user.role,
        created_at=current_user.created_at.isoformat() if current_user.created_at else None,
    )


@router.get("/profile", response_model=UserProfile)
def get_profile(current_user: UserModel = Depends(get_current_user)):
    return get_me(current_user)


@router.put("/profile", response_model=UserProfile)
def update_profile(
    payload: UpdateUserProfileRequest,
    current_user: UserModel = Depends(get_current_user),
    db=Depends(get_db),
):
    updated = UserService(db).update_profile(current_user.id, payload.display_name, payload.avatar_url)
    if updated is None:
        raise HTTPException(status_code=404, detail="User not found.")
    return UserProfile(
        id=updated.id,
        email=updated.email,
        display_name=updated.display_name,
        avatar_url=updated.avatar_url,
        role=updated.role,
        created_at=updated.created_at.isoformat() if updated.created_at else None,
    )


@router.get("/preferences", response_model=UserPreferences)
def get_preferences(current_user: UserModel = Depends(get_current_user), db=Depends(get_db)):
    pref = PreferencesService(db).get_or_create(current_user.id)
    return UserPreferences(
        default_location_id=pref.default_location_id,
        default_metric=pref.default_metric,
        default_period=pref.default_period,
        default_basket_id=pref.default_basket_id,
        household_size=pref.household_size,
        theme=pref.theme,
        data_density=pref.data_density,
    )


@router.put("/preferences", response_model=UserPreferences)
def update_preferences(
    payload: UpdateUserPreferencesRequest,
    current_user: UserModel = Depends(get_current_user),
    db=Depends(get_db),
):
    pref = PreferencesService(db).update(current_user.id, payload.model_dump(exclude_unset=True))
    return UserPreferences(
        default_location_id=pref.default_location_id,
        default_metric=pref.default_metric,
        default_period=pref.default_period,
        default_basket_id=pref.default_basket_id,
        household_size=pref.household_size,
        theme=pref.theme,
        data_density=pref.data_density,
    )


@router.get("/saved-regions", response_model=list[SavedRegion])
def list_saved_regions(current_user: UserModel = Depends(get_current_user), db=Depends(get_db)):
    service = SavedRegionsService(db)
    rows = service.list(current_user.id)
    result: list[SavedRegion] = []
    for row in rows:
        location = db.get(LocationModel, row.location_id)
        result.append(
            SavedRegion(
                location_id=row.location_id,
                name=location.name if location else row.location_id,
                label=row.label,
                saved_at=row.created_at.isoformat(),
            )
        )
    return result


@router.post("/saved-regions", response_model=SavedRegion)
def save_region(
    payload: SavedRegionRequest,
    current_user: UserModel = Depends(get_current_user),
    db=Depends(get_db),
):
    row = SavedRegionsService(db).save(current_user.id, payload.location_id, payload.label)
    location = db.get(LocationModel, row.location_id)
    return SavedRegion(
        location_id=row.location_id,
        name=location.name if location else row.location_id,
        label=row.label,
        saved_at=row.created_at.isoformat(),
    )


@router.delete("/saved-regions/{location_id}")
def remove_region(location_id: str, current_user: UserModel = Depends(get_current_user), db=Depends(get_db)):
    removed = SavedRegionsService(db).remove(current_user.id, location_id)
    if not removed:
        raise HTTPException(status_code=404, detail="Saved region not found.")
    return {"status": "ok"}


@router.get("/watchlist", response_model=list[WatchlistRegion])
def get_watchlist(current_user: UserModel = Depends(get_current_user), db=Depends(get_db)):
    return WatchlistService(db).list_watchlist(current_user.id)
