from copy import copy
from typing import List
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from src.db_connection.database import DatabaseConnection
from src.repository.linkedin_profile_crud import ProfileRepository
from src.schemas.linkedin_profile import ProfileSchema, ProfileSchemaCreate, ProfileSchemaModel
from src.models.linkedin_profile_model import Profile


profile_router = APIRouter(prefix='/profile')

@profile_router.post("/create", response_model=int)
def create_profile(profile: ProfileSchemaCreate, session: Session = Depends(DatabaseConnection.create_session)):
    """
    Create a new LinkedIn profile in the database.

    Parameters:
    - profile: ProfileSchema model containing the details of the profile to be created.
    - session: Database session for performing database operations.

    Returns:
    The ID of the created profile.
    """
    profile_repo = ProfileRepository(session=session)

    profile_model: Profile = profile_repo.create_profile(profile)
    profile_repo.session.commit()
    profile_repo.session.close()
    return 200

@profile_router.get("/profiles/{profile_id}", response_model=ProfileSchemaModel)
def read_profile(profile_id: int, session: Session = Depends(DatabaseConnection.create_session)):
    """
    Retrieve a specific LinkedIn profile by ID.

    Parameters:
    - profile_id: The unique identifier of the profile to retrieve.
    - session: Database session for performing database operations.

    Returns:
    Details of the retrieved profile.
    Raises:
    HTTPException: If the profile is not found in the database.
    """
    profile_repo: ProfileRepository = ProfileRepository(session=session)
    
    profile: Profile = profile_repo.get_filtered_by_id(id_=profile_id)
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    profile_repo.session.close()
    return profile

@profile_router.get("/profiles/", response_model=List[ProfileSchemaModel])
def read_profiles(limit: int = 100, session: Session = Depends(DatabaseConnection.create_session)):
    """
    Retrieve a list of LinkedIn profiles from the database, limited by the specified limit.

    Parameters:
    - limit: Maximum number of profiles to retrieve.
    - session: Database session for performing database operations.

    Returns:
    A list of profile details.
    """
    profile_repo: ProfileRepository = ProfileRepository(session=session)
    profiles: List[Profile] = profile_repo.get_all_profile(limit)

    profile_repo.session.close()
    return profiles

@profile_router.put("/profiles/{profile_id}", response_model=int)
def update_profile(profile_id: int, 
                   updated_profile: ProfileSchema, 
                   session: Session = Depends(DatabaseConnection.create_session)
                ):
    """
    Update an existing LinkedIn profile with the provided details.

    Parameters:
    - profile_id: The unique identifier of the profile to update.
    - updated_profile: ProfileSchema model containing the updated details of the profile.
    - session: Database session for performing database operations.

    Returns:
    The updated profile details after committing changes to the database.
    """
    profile_repo: ProfileRepository = ProfileRepository(session=session)
    profile: Profile = profile_repo.get_filtered_by_id(id_=profile_id)
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    if updated_profile.last_description == '':
        updated_profile.last_description = profile.last_description

    profile.url = updated_profile.url
    profile.last_description = updated_profile.last_description
    profile.is_active = updated_profile.is_active
    
    profile_repo.create_profile_from_model(profile)

    profile_repo.session.commit()
    profile_repo.session.close()
    return 200

@profile_router.delete("/profiles/{profile_id}", response_model=int)
def delete_profile(profile_id: int, session: Session = Depends(DatabaseConnection.create_session)):
    """
    Delete a LinkedIn profile from the database based on the profile ID.

    Parameters:
    - profile_id: The unique identifier of the profile to delete.
    - session: Database session for performing database operations.

    Returns:
    The ID of the deleted profile after committing the deletion.
    """
    profile_repo: ProfileRepository = ProfileRepository(session=session)
    profile: Profile = profile_repo.get_filtered_by_id(id_=profile_id)
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    profile_repo.delete_profile(profile_to_delete=profile)
    profile_repo.session.commit()
    return profile_id