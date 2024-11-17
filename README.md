# Notion Team Members Automation 
 
## Project Overview
This project provides a Python script to fetch user details from a Notion workspace using the Notion API. It requires a valid Notion session token (notion_session.json) to authenticate and interact with the Notion platform.

## Setting Up the Project
### Clone the Repository

```
git clone https://github.com/soham2312/NotionAutomation.git
cd NotionAutomation
```

### Install Required Dependencies using pip:

```
pip install -r requirements.txt
```

### Create a .env file in the project directory with your Notion API token:

```
NOTION_API_KEY=your_integration_token
```
### Getting the Storage State for Notion Login
To automate tasks on Notion, you need to retrieve the storage state (including session tokens). This will allow you to stay logged in without re-entering credentials each time. Follow the steps below to obtain the storage state:

### Install Prerequisites
Ensure you have Python and Playwright installed:
```
pip install playwright
playwright install
```
### Save the Storage State
Run the Python script to save the storage state after logging in
``` 
python session.py
```
- A browser window will open, and you will be directed to the Notion login page.
- Log in manually using your credentials or single sign-on (SSO).
- Once logged in, the script will save the session information in a file named `notion_storage_state.json`.

### Running the Script
Fetch Notion Users Run the script app.py to fetch all user details in your Notion workspace:

```
python app.py
```
### Running the Script to get all memebers of the workspace
```
python fetch.py
```
- check users.json and notion_storage_session.json files are present in directory
- Final ouput would be stored in *team_members_paginated.json* file

## Troubleshooting

### Session Expiration:
 If the session expires, repeat the process to fetch storage state of login and update notion_storage_state.json.

### Invalid API Key: 
Verify that the API key in .env matches your integration key in the Notion dashboard.

