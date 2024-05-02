from unittest.mock import patch, Mock
from src.route.webhook import get_profile_description, send_notification

class TestProfileFunctions:

    @patch('src.route.webhook.requests.get')
    @patch('src.route.webhook.json.loads')
    @patch('src.route.webhook.Env')
    def test_get_profile_description_successful(self, mocked_api, mock_json_loads, mock_requests_get):
        profile_url = "/exampleuser"
        api_response = Mock()
        api_response.status_code = 200
        api_response.json.return_value = {'data': 'Profile Description'}
        mock_requests_get.return_value = api_response
        mock_json_loads.return_value = api_response
        mock_env = Mock()
        mock_env.LINKEDIN_API_URL = Mock()
        mocked_api.return_value = mock_env

        result = get_profile_description(profile_url)

        assert result == {'data': 'Profile Description'}

    @patch('src.route.webhook.requests.exceptions')
    @patch('src.route.webhook.Env')
    def test_get_profile_description_failure(self, mock_requests_exceptions, mock_env):

        mock_env_response = Mock()
        mock_env_response.WEBHOOK_URL = Mock()
        mock_env.return_value = mock_env_response
        mock_requests_exceptions.RequestError = Mock()

        result = get_profile_description("/invaliduser")

        assert result is None

    @patch('src.route.webhook.sleep')
    @patch('requests.post')
    @patch('src.route.webhook.Env')
    def test_send_notification_success(self, mock_sleep, mock_requests_post, mock_env):
        profile_name = "exampleuser"
        mock_sleep.return_value = None
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_requests_post.return_value = mock_response

        mock_env_response = Mock()
        mock_env_response.WEBHOOK_URL = Mock()
        mock_env.return_value = mock_env_response

        result = send_notification(profile_name)

        assert result is True
        mock_requests_post.assert_called_once()

    @patch('src.route.webhook.requests.post')
    @patch('src.route.webhook.sleep', return_value=None)
    def test_send_notification_failure(self, mock_sleep, mock_requests_post):
        profile_name = "exampleuser"
        mock_response = Mock()
        mock_response.status_code = 500
        mock_requests_post.return_value = mock_response

        result = send_notification(profile_name)

        assert result is False
        