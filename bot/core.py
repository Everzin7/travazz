from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError
from bot.utils import logger
import time
from rich.progress import track

OPTIONS = [
    "CRASH INVISIVEL IPHONE",
    "ATRASO INFINITO IOS",
    "CRASH IPHONE",
    "TELA PRETA INVI"
]

TARGET_NUMBER = "+55 34 99163-7054"
GROUP_NAME = "Travazap | bot de travas"

def navigate_to_group(page: Page):
    logger.info(f"Searching for group '{GROUP_NAME}'...")
    try:
        # Search input
        search_input = page.locator("input[placeholder='Search']")
        search_input.wait_for(state="visible", timeout=10000)
        search_input.click()
        search_input.fill(GROUP_NAME)
        
        # Wait for results
        time.sleep(2)
        
        # Click the chat
        # Using a broad selector to catch the chat item
        chat_selector = f".row-title:has-text('{GROUP_NAME}')"
        page.locator(chat_selector).first.click()
        
        logger.info("Entered group.")
        
        # Wait for the chat to load (look for the header)
        page.wait_for_selector(f".chat-info .title:has-text('{GROUP_NAME}')", timeout=10000)
        
    except Exception as e:
        logger.error(f"Error navigating to group: {e}")
        raise

def run_cycle(page: Page):
    option_idx = 0
    
    logger.info("Starting automation cycle...")
    
    while True:
        try:
            current_option = OPTIONS[option_idx % len(OPTIONS)]
            logger.info(f"--- Cycle Start: {current_option} ---")
            
            # 1. Click "BUG IPHONE"
            # We look for the button in the message history. 
            # We assume the menu is visible or close to the bottom.
            logger.info("Looking for 'BUG IPHONE' button...")
            
            # Check if we need to go back from submenu first
            back_menu_btn = page.locator("button, .reply-markup-button").filter(has_text="VOLTAR AO MENU").last
            if back_menu_btn.is_visible():
                logger.info("Found 'VOLTAR AO MENU', clicking it to return to main menu...")
                back_menu_btn.click()
                time.sleep(1.5)

            bug_btn = page.locator("button, .reply-markup-button").filter(has_text="BUG IPHONE").last
            bug_btn.wait_for(state="visible", timeout=5000)
            bug_btn.click()
            
            # 2. Select the Option (Submenu)
            logger.info(f"Waiting for option '{current_option}'...")
            option_btn = page.locator("button, .reply-markup-button").filter(has_text=current_option).last
            option_btn.wait_for(state="visible", timeout=10000)
            option_btn.click()
            
            # 3. Enter Number
            logger.info("Waiting for input field...")
            # Wait a moment for the bot to ask
            time.sleep(1.5)
            
            input_box = page.locator(".input-message-input")
            input_box.click()
            input_box.fill(TARGET_NUMBER)
            page.keyboard.press("Enter")
            logger.info(f"Sent number: {TARGET_NUMBER}")
            
            # 4. Wait for Success and 'VOLTAR'
            logger.info("Waiting for confirmation...")
            
            # Wait for the success text to appear. This guarantees the new message has arrived.
            try:
                page.wait_for_selector("text=CRASH ENVIADO COM SUCESSO", timeout=40000)
                logger.info("✅ Success confirmed!")
            except PlaywrightTimeoutError:
                logger.warning("Success text not found, but trying to find VOLTAR anyway...")

            # NOW find the VOLTAR button. Since the message just arrived, it's the last one.
            voltar_btn = page.locator("button, .reply-markup-button").filter(has_text="VOLTAR").last
            voltar_btn.click()
            logger.info("Clicked 'VOLTAR'")
            
            # 5. Cycle Management
            option_idx += 1
            
            # 6. Countdown
            logger.info("Waiting 30 seconds before next cycle...")
            for i in range(30, 0, -1):
                print(f"⏳ Next cycle in {i:02d}s...", end="\r")
                time.sleep(1)
            print(" " * 30, end="\r") # Clear line
            
        except PlaywrightTimeoutError:
            logger.error("Timeout occurred. Element not found. Retrying cycle...")
            # If we time out, we might be in a weird state. 
            # Ideally we should try to find "BUG IPHONE" again in the next loop.
            time.sleep(2)
        except KeyboardInterrupt:
            logger.info("Stopping...")
            break
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            time.sleep(5)
