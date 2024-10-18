# Invitation Generator & Uploader

## Project Overview
This project automates the process of creating, uploading, and updating personalized invitations for contacts from Mautic CRM. The system fetches the list of registered contacts, generates personalized invitation images based on each contact's information (name, profile picture, lucky number), and uploads these images to Google Drive. Finally, the Google Drive link of the invitation is updated into the custom field of each contact in Mautic.

### Key Components:
1. **Invitation Generator**: Generates invitations from a template and adds personalized information (name, profile picture, lucky number).
2. **Uploader**: Uploads the generated invitation image to Google Drive and retrieves the shareable link.
3. **Mautic API**: Fetches contact lists from Mautic and updates the invitation link in a custom field.
4. **Face Extractor**: Detects and crops faces from the profile picture and inserts them into the invitation.

## Project Structure

```
Invitation_WS#8/
│
├── app/
│   ├── __pycache__/                  # Python cache files
│   ├── templates/                    # Directory for storing invitation templates (not included in repo)
│   │  
│   ├── __init__.py                   # Initialization for app package
│   ├── email_sender.py               # Updates the Google Drive link in Mautic
│   ├── face_extractor.py             # Detects and crops faces from the profile picture
│   ├── invitation_creator.py         # Generates invitations from a template and personalizes them
│   ├── invitation_uploader.py        # Uploads invitations to Google Drive and retrieves the link
│   ├── mautic_api.py                 # Functions for working with Mautic API
│   ├── utils.py                      # Utility functions for saving/loading processed emails
│   └── routes.py                     # Handles the logic for fetching contacts and updating invitation links
│
├── generated_invitations/            # Directory where generated invitations are saved (not included in repo)
│
├── .env                              # Environment variables file for API credentials (not included in repo)
├── app.py                            # Main entry point for the project, handles task scheduling and RabbitMQ. Script that runs both Flask App and RabbitMQ Worker
├── auth.py                           # Handles authentication logic for Google Drive
├── client_secrets.json               # Client secrets for Google Drive API authentication (not included in repo)
├── config.py                         # Common configurations (API paths, directories, etc.)
├── credentials.json                  # Authentication credentials for Google Drive API
├── readme.md                         # General project overview 
├── requirements.txt                  # Required libraries for the project
├── token_info.json                   # Stores token information for Mautic API (not included in repo)
├── processed_emails.json             # Contains emails that have been included in RabbitMQ
├── telegram_bot.py                   # Sends status updates via Telegram
├── get_chat_id.py                    # This file is used to get chat id to send notifications from the system via Telegram bot.
└── worker.py                         # RabbitMQ worker to handle invitation generation tasks from queue
```

## Installation Guide

### 1. Setup the Environment
First, make sure you have `Python 3.x` installed. Then, install the required libraries using `pip`:

```bash
pip install -r requirements.txt
```

The required dependencies are:

```text
Flask
python-dotenv
pydrive
pillow
requests
opencv-python
numpy
```
These libraries are responsible for various aspects of the project, such as image processing, HTTP requests, and Google Drive interaction.


### 2. Configuration

1. **Google Drive API**:
   - You need to authenticate your Google Drive access. To do this, create a project in [Google Developers Console](https://console.developers.google.com/), enable Google Drive API, and download the `credentials.json` file.
   - Place the `credentials.json` file into the `config/` folder.
   - The program will handle authentication when you run the script for the first time.

2. **Mautic API**:
   - Configure your Mautic API in `config.py`:
   
   ```python
   MAUTIC_API_URL = "https://example.com"  # Your Mautic base URL
   MAUTIC_AUTH = ("username", "password")  # Mautic username and password
   OUTPUT_DIR = "path/to/your/folder"  # Path to save generated invitations
   INVITATION_TEMPLATE = "path/to/your/folder"  # Path to the invitation template
   ```

3. **Directory Setup**:
   Ensure the `generated_invitations` and `templates` directories exist as they will store the generated invitations and the invitation template respectively.

4. **Environment Variables**: 
   - Create a .env file in the root directory and configure the following variables:

    ```
    TELEGRAM_BOT_TOKEN=<Your Telegram Bot Token>
    TELEGRAM_CHAT_ID=<Your Telegram Chat ID>
    RABBITMQ_HOST=<Your RabbitMQ Host>
    RABBITMQ_PORT=<Your RabbitMQ Port>
    RABBITMQ_USER=<Your RabbitMQ Username>
    RABBITMQ_PASSWORD=<Your RabbitMQ Password>
    ```

### 3. Running the Project
To start the program, simply run `app.py`:

```bash
python app.py
```

This command will:
   - Start the Flask app.
   - Begin fetching contacts from Mautic.
   - Publish new contacts to RabbitMQ.
   - Start the RabbitMQ worker to process each contact by generating an invitation, uploading it to Google Drive, and updating Mautic with the invitation link.
   - Send real-time updates to your Telegram bot for each step of the process.

### 4. Telegram Bot Integration
- The system integrates with a Telegram bot to send real-time updates on contact processing, such as:

    - **Contact Detected**: "New contact detected: <email>"
    - **Processing**: "Processing contact: <name>, Email: <email>"
    - **Invitation Created**: "Invitation created for: <name>"
    - **Link Uploaded**: "Invitation link uploaded to Google Drive: <link>"
    - **Success**: "Successfully updated contact in Mautic: <email>"

### 5. Error Handling
- **Authentication Issues**: If there is an issue with Google Drive authentication, the script will guide you through the OAuth2 authentication process in your browser.
- **Image Processing**: If the face is not detected in the profile picture, a default avatar will be used.
- **API Rate Limits**: If Mautic or Google Drive rate limits are hit, the script handles retries automatically with exponential backoff.

## Core Functionality

### 1. Fetching Contacts from Mautic
The system fetches contact information from the Mautic form via API calls. These contacts are processed to generate personalized invitations:

```python
def get_all_contacts_from_form(form_id):
    # Retrieves all contacts from a given form in Mautic
```

### 2. Generating Personalized Invitations
Based on a pre-existing template, an invitation is created with:
- The contact’s name.
- Their profile picture (detected and cropped).
- A unique lucky number.

```python
def create_personalized_invitation(name, contact_id):
    # Creates a personalized invitation using the template and the contact's information
```

### 3. Uploading Invitations to Google Drive
Once the invitation is generated, it is uploaded to Google Drive. A shareable link is created and returned:

```python
def upload_invitation_to_server(invitation_file, name):
    # Uploads the invitation to Google Drive and returns a shareable link
```

### 4. Updating the Google Drive Link in Mautic
After the invitation link is generated, it is updated into the custom field `invitation_link` in the contact’s Mautic profile:

```python
def update_invitation_link_in_mautic_by_email(email, invitation_url):
    # Updates the custom field in Mautic with the invitation link based on email
```

### 5. Sending Status Updates via Telegram
The system sends updates about each step of the invitation process (detection, creation, upload, and success) to a Telegram bot:

```python
def send_message_sync(message):
    # Sends a synchronous message to the Telegram bot
```

## Customization Options

### Face Detection & Cropping
The face detection uses OpenCV's Haar Cascade classifier to locate and crop faces from the profile picture. The cropped face is resized and placed into the invitation:

```python
def detect_and_crop_face(image):
    # Detects and crops the face using OpenCV's Haar Cascade
```

You can adjust the detection sensitivity and size by modifying the `scaleFactor` and `minNeighbors` parameters.

### RabbitMQ Integration
### RabbitMQ for Task Queuing
RabbitMQ is used to queue the task of creating invitations to prevent the system from getting overwhelmed when processing many contacts simultaneously. The tasks are queued up, and a separate worker (defined in worker.py) processes each contact.

1. Publish Contacts to Queue
In app.py, contacts are fetched and published to the RabbitMQ queue:

```python
def publish_to_rabbitmq(contact):
    # Sends the contact details to RabbitMQ for processing
```

2. Worker to Process Queue
The worker.py file listens to the queue and processes each contact. The worker creates the invitations and uploads them to Google Drive:

```python
def start_worker():
    # Start RabbitMQ worker to process invitations
```

## Additional Features
- **Crash Recovery**: If the script crashes, it will not regenerate invitations that have already been created. Instead, it resumes where it left off.
- **Skipping Existing Links**: If a contact already has an invitation link, the script skips processing that contact, saving time and resources.

