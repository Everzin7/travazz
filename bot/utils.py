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
            
        # Add a white border (Quiet Zone) - Crucial for CV2
        # 240x240 -> 280x280
        img = cv2.copyMakeBorder(img, 20, 20, 20, 20, cv2.BORDER_CONSTANT, value=[255, 255, 255])
        
        detector = cv2.QRCodeDetector()
        
        # Try 1: Original with border
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
        
        # Try 3.1: Zoomed/Cropped (Center) - New Strategy
        # Sometimes there's too much whitespace
        h, w = gray.shape
        center_crop = gray[int(h*0.1):int(h*0.9), int(w*0.1):int(w*0.9)]
        data, bbox, _ = detector.detectAndDecode(center_crop)
        if data: return data

        # Try 4: Binary Threshold
        _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)
        data, bbox, _ = detector.detectAndDecode(thresh)
        if data: return data
        
        # Try 4.1: Adaptive Threshold (Better for uneven lighting/rendering)
        thresh_adapt = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        data, bbox, _ = detector.detectAndDecode(thresh_adapt)
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
