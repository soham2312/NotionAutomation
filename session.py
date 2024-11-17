import asyncio
from playwright.async_api import async_playwright

async def save_storage_state():
    async with async_playwright() as p:
        # Launch the browser
        browser = await p.chromium.launch(headless=False)  # Set headless=True for invisible browser
        context = await browser.new_context()

        # Open a new page
        page = await context.new_page()

        # Navigate to the login page
        print("Navigating to the login page...")
        await page.goto("https://www.notion.so/login")

        # Wait for manual login (or automate if credentials are known)
        print("Please log in manually...")
        input()
        await page.wait_for_timeout(15000)  # Adjust timeout as needed

        # Save the storage state after login
        storage_state_file = "notion_storage_state.json"
        await context.storage_state(path=storage_state_file)
        print(f"Storage state saved to {storage_state_file}")

        # Close the browser
        await browser.close()

asyncio.run(save_storage_state())
