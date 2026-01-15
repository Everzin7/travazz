import cv2
import numpy as np

def analyze_debug_image():
    try:
        img = cv2.imread("debug_qr.png")
        if img is None:
            print("Image not found or empty")
            return

        print(f"Dimensions: {img.shape}")
        print(f"Mean Color: {np.mean(img)}")
        
        # Save a crop to see if it's the QR
        h, w, _ = img.shape
        center_crop = img[int(h*0.1):int(h*0.9), int(w*0.1):int(w*0.9)]
        cv2.imwrite("debug_crop.png", center_crop)
        print("Saved debug_crop.png")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    analyze_debug_image()
