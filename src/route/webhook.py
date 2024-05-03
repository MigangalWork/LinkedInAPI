from random import randint
import requests
import json
from fastapi import APIRouter, FastAPI, BackgroundTasks
from time import sleep
from sqlalchemy.orm import Session
from typing import List
from configparser import ConfigParser

from src.repository.linkedin_profile_crud import ProfileRepository
from src.db_connection.database import DatabaseConnection
from src.models.linkedin_profile_model import Profile
from src.helpers import get_config
from src.settings import Env


webhook_router = APIRouter(prefix='/webhook')


def get_profile_description(profile_url: str) -> str:
    """
    Function to fetch profile description from LinkedIn API.

    Parameters:
    - profile_url: URL of the LinkedIn profile to fetch the description.

    Returns:
    Dictionary of the LinkedIn profile data.
    """
    api_url = Env.LINKEDIN_API_URL + profile_url
    try:
        response = requests.get(api_url)
    except Exception as e:
        print(f'An error ocurred while getting profile data: {str(e)}')
        return None
    
    if response.status_code != 200:
         return None
    
    return response.json()

def get_profile_description_mock(profile_url: str) -> str:
    """
    This mocks the function to fetch profile description from LinkedIn API.

    Parameters:
    - profile_url: URL of the LinkedIn profile to fetch the description.

    Returns:
    Dictionary of the LinkedIn profile data.
    """
    response = None
    if randint(0,1):
        response = str(randint(0, 1000))
    
    return response


def send_notification(profile_name: str, mock: bool = False) -> bool:
    """
    Function to send a notification with the updated profile name.

    Parameters:
    - profile_name: Name of the profile to send the notification for.

    Returns:
    True if the notification is successfully sent, False otherwise.
    """
    if mock:
        return True
    
    profile_data: dict = {
        'profile updated': profile_name
        }
    
    status_code = False
    try_count = 0
    while try_count < 3:
        try:
            response = requests.post(Env.WEBHOOK_URL, json=json.dumps(profile_data))
            status_code = response.status_code
        except Exception as e:
            print(f'An error ocurred while sending a notification: {str(e)}')
            try_count = try_count + 1
            sleep(0.5)

        break

    return status_code == 200

async def profile_update_check(loop: bool = True):
    """
    Background task to periodically check for profile updates. This function runs indefinitely.

    Retrieves all profiles from the database, fetches their current description from LinkedIn,
    compares it with the last description, and sends a notification if there are updates.

    Configuration Options:
    - 'refresh_profiles_time': Time interval to wait between profile updates.
    """
    
    config: ConfigParser = get_config()
    sleep_interval_seconds = config.getint('time', 'refesh_profiles_time')
    one_execution = True

    while True and (loop or one_execution):
        one_execution = False
        session: Session = DatabaseConnection.create_session()
        profile_repo: ProfileRepository = ProfileRepository(session=session)
        profile_list: List[Profile] = profile_repo.get_all_profile()

        for profile in profile_list:
            actual_description: str = get_profile_description_mock(profile.url)

            if actual_description is None or actual_description == profile.last_description:
                continue

            if send_notification(profile.url, mock=True):
                profile.last_description = actual_description
                profile_repo.create_profile_from_model(profile)
        
        session.commit()
        session.close()
        sleep(sleep_interval_seconds)

@webhook_router.on_event("startup")
async def start_backgroud_task():
    """
    Event handler to start the background task on FastAPI startup.
    # Adds the profile_update_check task to the BackgroundTasks to run on startup.
    """
    bg_tasks.add_task(profile_update_check)


@webhook_router.get("/check", response_model=int)
async def check_profiles():
    await profile_update_check(loop=False)
    return 200

bg_tasks = BackgroundTasks()

