from sqlalchemy.orm import Session

from src.models.linkedin_profile_model import Profile
from src.schemas.linkedin_profile import ProfileSchema


class ProfileRepository:

    def __init__(self, session: Session) -> None:
        self.session = session

    def get_all_profile(self, limit: int = 0):
        all_profiles: list
        if limit:
            all_profiles = self.session.query(Profile).limit(limit).all()
        else:
           all_profiles = self.session.query(Profile).all()

        return all_profiles
    
    def get_filtered_by_id(self, id_: int):
        return self.session.query(Profile).filter_by(id=id_).first()
    
    def get_filtered_by_url(self, url: str):
        return self.session.query(Profile).filter_by(url=url).first()
    
    def create_profile(self, profile: ProfileSchema):
        profile_model: Profile = Profile(**profile.dict())
        self.session.add(profile_model)
        return profile_model

    def create_profile_from_model(self, profile: Profile):
        self.session.add(profile)

    def __del__(self):
        if self.session is not None:
            self.session.close()

    def delete_profile(self, profile_to_delete: Profile):
        self.session.delete(profile_to_delete)

