from app.models.economic import UserModel, utc_now
from app.services.auth_service import AuthIdentity


class UserService:
    def __init__(self, session):
        self.session = session

    def get_or_create_user(self, identity: AuthIdentity) -> UserModel:
        user = self.session.get(UserModel, identity.user_id)
        if user is None:
            user = UserModel(
                id=identity.user_id,
                email=identity.email,
                display_name=identity.display_name,
                role=identity.role,
            )
            self.session.add(user)
            self.session.commit()
            self.session.refresh(user)
            return user

        changed = False
        if user.email != identity.email:
            user.email = identity.email
            changed = True
        if identity.display_name and user.display_name != identity.display_name:
            user.display_name = identity.display_name
            changed = True
        if changed:
            user.updated_at = utc_now()
            self.session.commit()
            self.session.refresh(user)
        return user

    def update_profile(self, user_id: str, display_name: str | None, avatar_url: str | None) -> UserModel | None:
        user = self.session.get(UserModel, user_id)
        if user is None:
            return None
        if display_name is not None:
            user.display_name = display_name
        if avatar_url is not None:
            user.avatar_url = avatar_url
        user.updated_at = utc_now()
        self.session.commit()
        self.session.refresh(user)
        return user
