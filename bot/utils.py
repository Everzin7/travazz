import cv2
import numpy as np
import qrcode
from rich.console import Console
from rich.logging import RichHandler
import logging

console = Console()

def setup_logger():
    logging.basicConfig(
        level="INFO",
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)]
    )
    return logging.getLogger("rich")

logger = setup_logger()

def decode_qr_from_bytes(image_bytes):
    """
    Decodes a QR code from image bytes using OpenCV.
    Tries multiple preprocessing methods (original, inverted, threshold).
    """
    try:
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            return None
        
        detector = cv2.QRCodeDetector()
        
        # Try 1: Original
        data, bbox, _ = detector.detectAndDecode(img)
        if data: return data
        
        # Try 2: Inverted (often needed for dark mode)
        img_inv = cv2.bitwise_not(img)
        data, bbox, _ = detector.detectAndDecode(img_inv)
        if data: return data
        
        # Try 3: Grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        data, bbox, _ = detector.detectAndDecode(gray)
        if data: return data

        # Try 4: Binary Threshold
        _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)
        data, bbox, _ = detector.detectAndDecode(thresh)
        if data: return data
        
        # Try 5: Inverted Binary Threshold
        thresh_inv = cv2.bitwise_not(thresh)
        data, bbox, _ = detector.detectAndDecode(thresh_inv)
        if data: return data

        return None
    except Exception as e:
        logger.error(f"Error decoding QR: {e}")
        return None

def print_qr_to_terminal(data):
    """
    Prints the QR code to the terminal using qrcode library.
    """
    qr = qrcode.QRCode(border=1)
    qr.add_data(data)
    f = io.StringIO()
    qr.print_ascii(out=f, invert=True)
    f.seek(0)
    print(f.read())

import io
