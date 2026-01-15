from playwright.sync_api import Page
from bot.utils import logger, decode_qr_from_bytes, print_qr_to_terminal
import time

def login(page: Page):
    logger.info("Accessing Telegram Web K...")
    page.goto("https://web.telegram.org/k/")
    
    # Check if already logged in
    try:
        # Look for the chat list or the search bar
        page.wait_for_selector(".chat-list, input[placeholder='Search']", timeout=5000)
        logger.info("Already logged in!")
        return
    except:
        pass
    
    logger.info("Waiting for QR Code...")
    # The canvas usually holds the QR code in version K
    try:
        # Wait for canvas to be visible
        qr_canvas = page.wait_for_selector("canvas", timeout=30000)
    except:
        logger.error("Could not find QR code canvas. Please check if Telegram Web is loading correctly.")
        raise
    
    # Wait a bit for the animation to finish/render
    time.sleep(5)
    
    logger.info("Capturing QR Code...")
    
    qr_data = None
    for attempt in range(5):
        try:
            # Take screenshot of the entire page to ensure we capture the QR
            png_bytes = page.screenshot()
            
            # Try to decode
            qr_data = decode_qr_from_bytes(png_bytes)
            
            if qr_data:
                break
            
            logger.warning(f"Attempt {attempt+1}/5: QR Code not detected. Retrying...")
            time.sleep(2)
        except Exception as e:
            logger.error(f"Error during capture: {e}")
            time.sleep(2)
    
    if qr_data:
        logger.info("QR Code decoded. Please scan this with your Telegram app:")
        print_qr_to_terminal(qr_data)
    else:
        # Save debug image
        with open("debug_qr.png", "wb") as f:
            f.write(png_bytes)
        logger.warning("Could not decode QR code automatically. Debug image saved to 'debug_qr.png'.")
    
    logger.info("Waiting for authentication...")
    try:
        # Wait for the chat list to appear (indicating login success)
        page.wait_for_selector(".chat-list, .sidebar-header", timeout=300000) # 5 minutes
        logger.info("Login successful!")
    except:
        logger.error("Login timed out.")
        raise Exception("Login failed or timed out.")
