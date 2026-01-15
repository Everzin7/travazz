import sys
import os
from playwright.sync_api import sync_playwright
from bot.utils import logger
from bot.auth import login
from bot.core import navigate_to_group, run_cycle

SESSION_FILE = "session.json"

def main():
    logger.info("Starting Travazap Bot...")
    
    with sync_playwright() as p:
        # Determine if we are running on a server (headless) or desktop
        # If we are on Mac (local), we can run headful to scan easily
        is_headless = True
        if sys.platform == "darwin": # Mac OS
            is_headless = False # Open browser window on Mac
            logger.info("Running in Desktop mode (Window visible)")
        else:
            logger.info("Running in Server mode (Headless)")

        browser = p.chromium.launch(headless=is_headless, args=["--window-size=1280,720"])
        
        # Load session if exists
        context_args = {
            "user_agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "viewport": {"width": 1280, "height": 720}
        }
        
        if os.path.exists(SESSION_FILE):
            logger.info(f"Loading session from {SESSION_FILE}...")
            context_args["storage_state"] = SESSION_FILE
            
        context = browser.new_context(**context_args)
        page = context.new_page()
        
        try:
            # 1. Authentication
            # Pass the context so we can save the session after login
            login(page, context, SESSION_FILE)
            
            # 2. Navigation
            navigate_to_group(page)
            
            # 3. Execution
            run_cycle(page)
            
        except KeyboardInterrupt:
            logger.info("\nBot stopped by user.")
        except Exception as e:
            logger.exception(f"Fatal error: {e}")
        finally:
            logger.info("Closing browser...")
            browser.close()

if __name__ == "__main__":
    main()
