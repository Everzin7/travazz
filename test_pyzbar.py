from pyzbar.pyzbar import decode
from PIL import Image
import sys

try:
    # Try to load the image
    img = Image.open("debug_qr.png")
    print(f"Image loaded: {img.size}")
    
    # Decode
    decoded_objects = decode(img)
    
    if decoded_objects:
        print(f"Success! Found {len(decoded_objects)} codes.")
        for obj in decoded_objects:
            print(f"Data: {obj.data.decode('utf-8')}")
    else:
        print("No QR code found by pyzbar.")
        
except Exception as e:
    print(f"Error: {e}")
    print("Likely missing libzbar shared library.")
