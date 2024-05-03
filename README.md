# LinkedInAPI

## Introduction
This API is built using FastAPI and SQLAlchemy. It's designed to manage LinkedIn profile URLs, track updates in profile descriptions, and notify a specific URL via a POST request when any changes are detected in the descriptions of tracked profiles.

## Features
- **Save LinkedIn Profile URL**: Store LinkedIn profile URLs for monitoring.
- **Monitor Profile Descriptions**: Check saved profiles regularly (each 2 min) for any updates in the description.
- **Notification on Changes**: Automatically send a notification (POST request) to the defined direction when a profile description is updated with the profile url that changed.


## Installation without docker
1. **Clone this repository**:
   ```
   git clone https://your-repository-url.git
   cd your-repository-directory
   ```

2. **Install the required packages**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the env and the database**:
   Update the database connection details in the .env and all the others required fields that you will find in the .env_example.

4. **Run the application**:
   ```bash
   uvicorn main:app
   ```

   You can also run the main.py
   This command will start the FastAPI server on the defined host and port in the .env

## Installation with docker


## Usage
1. **Clone this repository**:
   ```
   git clone https://your-repository-url.git
   cd your-repository-directory
  ```
2. **Set up the env and the database**:
   Update the database connection details in the .env and all the others required fields that you will find in the .env_example.

3. **Build the docker image from the Dockerfile**: 
   ```bash
   docker build -t fastapi-image .
   ```

4. **Run a container from the image**:
The docker file launch configuration will overwrite the .env host, port and reload. The default dockerfile will start the FastAPI server on http://0.0.0.0:8000 with reload as False.
  ```bash
    docker run -d --name mycontainer -p 8000:8000 fastapi-image
```
### Endpoints

#### 1. Add LinkedIn Profile
- **URL**: `/profile/`
- **Method**: `POST`
- **Body**:
  ```json
  {
    "url": "https://www.linkedin.com/in/example"
  }
  ```

#### 2. Check for Updates
- **URL**: `/check-updates`
- **Method**: `GET`
- The system automatically checks for updates every 2 minutes

### Environment Variables
- **DATABASE_HOST**: Hostname for the database connection
- **DATABASE_PASSWORD**: Password for the database connection
- **WEBHOOK_URL**: URL to which notifications are sent when a LinkedIn profile description is updated
- **LINKEDIN_API_URL**: Base URL for making LinkedIn API requests

- **HOST**: The host address to bind the server to. To allow external connections, use `0.0.0.0`.
- **PORT**: The port on which the application will be served, e.g., `8000`.
- **RELOAD**: Set this to `True` during development to enable live reloading, or `False` for production settings.

## Scheduled Tasks
The API includes a background task setup to run at specified intervals to check for profile description updates.

## Potential Enhancements
- OAuth integration for LinkedIn API for more precise and authorized data access.
- Refining the notification system to include more details or integrate with other services like email.
- Enhancing security features to protect the stored profile data.


Due to time constraints, compromises had to be made. A security system including OAuth and token authentication should have been implemented, for different users if needed. For testing purposes, a SQLite database has been incorporated. We're utilizing uvicorn as our server, the standard ASGI server for fastAPI development. While suitable for production in certain cases, depending on usage, alternative software may be necessary. Tests have been added to validate the main functions of the API.

Unfortunately, the LinkedIn API is not openly accessible. To utilize it, you must request access, a process that takes considerably longer than the timeframe of this project. Scraping LinkedIn was considered, but the platform prohibits scraping its website. To maintain the proyect business friendliness, a mock solution was implemented. To fully integrate the API functionalities, all necessary LinkedIn API implementations must be developed.