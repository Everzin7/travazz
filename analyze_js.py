import cv2
import numpy as np

def analyze_js_image():
    try:
        img = cv2.imread("debug_js_qr.png")
        if img is None:
            print("Image not found or empty")
            return

        print(f"Dimensions: {img.shape}")
        
        # Check if it has content
        if np.mean(img) < 10 or np.mean(img) > 250:
            print("Image is blank/solid color")
        else:
            print(f"Image has content. Mean: {np.mean(img)}")
            
        # Try to detect on this raw image
        detector = cv2.QRCodeDetector()
        data, _, _ = detector.detectAndDecode(img)
        print(f"Raw detection: {data}")
        
        # Try with border
        img_border = cv2.copyMakeBorder(img, 50, 50, 50, 50, cv2.BORDER_CONSTANT, value=[255, 255, 255])
        data, _, _ = detector.detectAndDecode(img_border)
        print(f"Border detection: {data}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    analyze_js_image()
