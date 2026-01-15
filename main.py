import sys
from playwright.sync_api import sync_playwright
from bot.utils import logger
from bot.auth import login
from bot.core import navigate_to_group, run_cycle

def main():
    logger.info("Starting Travazap Bot for Ubuntu...")
    
    with sync_playwright() as p:
        # Launch browser
        # headless=True is essential for terminal-only operation
        # We use a custom user agent to look like a standard Linux desktop
        browser = p.chromium.launch(headless=True, args=["--window-size=1280,720"])
        context = browser.new_context(
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720}
        )
        page = context.new_page()
        
        try:
            # 1. Authentication
            login(page)
            
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
