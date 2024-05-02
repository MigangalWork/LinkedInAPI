from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.route.profile_route import create_profile, read_profile, read_profiles, update_profile, delete_profile
from src.repository.linkedin_profile_crud import ProfileRepository
from src.schemas.linkedin_profile import ProfileSchema, ProfileSchemaModel
from src.models.linkedin_profile_model import Profile

from unittest.mock import patch


class TestProfileroute:
    
    @patch('src.route.profile_route.ProfileRepository')
    def test_create_profile(self, mock_profile_repo):
        fake_profile = ProfileSchema(url='https://www.linkedin.com/test_url', last_description='test_description', is_active=True)
        mock_profile_instance = mock_profile_repo.return_value
        mock_profile_instance.create_profile.return_value = Profile(id=1, url='test_url', last_description='test_description', is_active=True)

        session = Session()
        
        result = create_profile(fake_profile, session)
        
        assert result == 1
        mock_profile_instance.create_profile.assert_called_once()
    
    @patch('src.route.profile_route.ProfileRepository')
    def test_read_profile(self, mock_profile_repo):
        fake_profile_id = 1
        mock_profile_instance = mock_profile_repo.return_value
        mock_profile_instance.get_filtered_by_id.return_value = Profile(id=fake_profile_id)

        session = Session()

        result = read_profile(fake_profile_id, session)
        
        assert result.id == fake_profile_id
        mock_profile_instance.get_filtered_by_id.assert_called_once()
    
    @patch('src.route.profile_route.ProfileRepository')
    def test_read_profiles(self, mock_profile_repo):
        fake_profiles = [Profile(id=1), Profile(id=2)]
        mock_profile_instance = mock_profile_repo.return_value
        mock_profile_instance.get_all_profile.return_value = fake_profiles

        session = Session()

        result = read_profiles(2, session)
        
        assert len(result) == 2
        mock_profile_instance.get_all_profile.assert_called_once_with(2)
    
    @patch('src.route.profile_route.ProfileRepository')
    def test_update_profile(self, mock_profile_repo):
        fake_profile_id = 1
        fake_updated_profile = ProfileSchema(url='https://www.linkedin.com/updated_url', last_description='updated_description', is_active=False)
        
        mock_profile_instance = mock_profile_repo.return_value
        mock_profile_instance.get_filtered_by_id.return_value = Profile(id=fake_profile_id, url='https://www.linkedin.com/old_url', last_description='old_description', is_active=True)

        session = Session()

        result = update_profile(fake_profile_id, fake_updated_profile, session)
        
        assert result.url == 'https://www.linkedin.com/updated_url'
        assert result.last_description == 'updated_description'
        assert result.is_active == False
        mock_profile_instance.get_filtered_by_id.assert_called_once()
    
    @patch('src.route.profile_route.ProfileRepository')
    def test_delete_profile(self, mock_profile_repo):
        fake_profile_id = 1
        mock_profile_instance = mock_profile_repo.return_value
        mock_profile_instance.get_filtered_by_id.return_value = Profile(id=fake_profile_id)

        session = Session()

        result = delete_profile(fake_profile_id, session)
        
        assert result == fake_profile_id
        mock_profile_instance.get_filtered_by_id.assert_called_once()