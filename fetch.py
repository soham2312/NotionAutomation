import asyncio
import json
from playwright.async_api import async_playwright


async def login_and_fetch_team_members():
    # Load users data
    with open("users.json", "r") as users_file:
        users_data = json.load(users_file)
    user_lookup = {user["id"]: {"email": user["email"], "name": user["name"]} for user in users_data}

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(storage_state="notion_storage_state.json")
        page = await context.new_page()

        print("Navigating to Notion login page...")
        await page.goto("https://www.notion.so/login")
        await page.wait_for_timeout(15000)  # Allow manual login if needed
        print("Logged in or session restored.")

        # Set up data handling
        api_endpoint = "https://www.notion.so/api/v3/syncRecordValuesSpace"
        paginated_team_members = {}
        seen_user_ids = set()
        page_number = 1

        async def handle_request(route, request):
            if request.url.startswith(api_endpoint) and request.method == "POST":
                response = await route.fetch()
                response_json = await response.json()

                new_team_members = []
                if response_json.get("recordMap", {}).get("space_user", {}):
                    print(f"Fetched data for page {page_number}.")
                    users = response_json["recordMap"]["space_user"]
                    for user_id, user_data in users.items():
                        user_value = user_data.get("value", {})
                        user_id_value = user_value.get("value", {}).get("user_id", "")

                        if user_id_value and user_id_value not in seen_user_ids:
                            matched_user = user_lookup.get(user_id_value, {"email": "", "name": ""})
                            new_team_members.append({
                                "ID": user_id_value,
                                "Role": user_value.get("value", {}).get("membership_type", ""),
                                "Email": matched_user["email"],
                                "Name": matched_user["name"]
                            })
                            seen_user_ids.add(user_id_value)

                if new_team_members:
                    paginated_team_members[f"Page_{page_number}"] = new_team_members
                    with open("team_members_paginated.json", "w") as file:
                        json.dump(paginated_team_members, file, indent=4)
                    print(f"Saved page {page_number} data.")
                await route.continue_()

        await page.route(api_endpoint, handle_request)

        print("Navigating to team members page...")
        await page.wait_for_selector('[dir="ltr"]', timeout=30000)
        await page.click('[dir="ltr"]')
        print("Navigated.")

        await page.wait_for_selector('.settings', timeout=30000)
        await page.click('.settings')
        print("Accessing settings.")

        await page.wait_for_selector('div:text("People")', timeout=30000)
        await page.click('div:text("People")')
        print("Opened 'People' section.")
        await page.wait_for_timeout(5000)

        # Trigger data fetch
        await page.evaluate("""
            async () => {
                await fetch('https://www.notion.so/api/v3/syncRecordValuesSpace', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        requests: [{
                            pointer: {
                                table: "space"
                            },
                            version: -1
                        }]
                    })
                });
            }
        """)
        await page.wait_for_timeout(3000)

        # Load additional data
        while True:
            try:
                load_more_button = await page.wait_for_selector(".arrowDown", timeout=5000)
                await load_more_button.click()
                print(f"Loaded more data for page {page_number}.")
                page_number += 1
                await page.wait_for_timeout(3000)
            except Exception:
                print("No more 'Load More' button found.")
                break

        await browser.close()


asyncio.run(login_and_fetch_team_members())
