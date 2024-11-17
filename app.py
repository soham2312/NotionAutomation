import os
import json
from dotenv import load_dotenv
from notion_client import Client

# Load environment variables from a .env file
load_dotenv()

# Fetch the Notion API key from environment variables
NOTION_API_KEY = os.getenv("NOTION_API_KEY")

if not NOTION_API_KEY:
    raise ValueError("API key is missing! Set NOTION_API_KEY in the .env file or as an environment variable.")

# Initialize the Notion client
notion = Client(auth=NOTION_API_KEY)


def fetch_all_users():
    """
    Fetch all users from the Notion workspace and return their details.
    """
    try:
        # Initialize pagination variables
        has_more = True
        next_cursor = None
        all_users = []

        # Fetch users with pagination
        while has_more:
            response = notion.users.list(start_cursor=next_cursor)

            # Collect users from the current page
            all_users.extend(response.get("results", []))

            # Update pagination variables
            has_more = response.get("has_more", False)
            next_cursor = response.get("next_cursor")

        # Extract and format user details
        user_data = []
        for user in all_users:
            user_info = {
                "id": user.get("id"),
                "name": user.get("name"),
                "email": user.get("person", {}).get("email") if user.get("type") == "person" else None,
                "type": user.get("type"),
            }
            user_data.append(user_info)
            print(user_info)  # Optional: Log user details to the console

        return user_data
    except Exception as e:
        print(f"Error fetching users: {str(e)}")
        return []


def save_to_json(data, filename="users.json"):
    """
    Save the user data to a JSON file.
    """
    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        print(f"User data saved to {filename}")
    except Exception as e:
        print(f"Error saving data to JSON: {str(e)}")


if __name__ == "__main__":
    print("Fetching users from the Notion workspace...")
    user_data = fetch_all_users()

    if user_data:
        save_to_json(user_data)
