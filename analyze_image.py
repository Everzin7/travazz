import cv2
import numpy as np

def analyze_debug_image():
    try:
        img = cv2.imread("debug_qr.png")
        if img is None:
            print("Image not found or empty")
            return

        print(f"Dimensions: {img.shape}")
        
        # Calculate average brightness
        avg_color_per_row = np.average(img, axis=0)
        avg_color = np.average(avg_color_per_row, axis=0)
        print(f"Average Color (BGR): {avg_color}")
        
        # Check if it's mostly black
        if np.mean(img) < 10:
            print("Image is mostly black/dark.")
        elif np.mean(img) > 240:
            print("Image is mostly white.")
        else:
            print("Image has content.")
            
        # Check for Canvas-like structure (Telegram Web K usually centers the QR)
        # Let's crop the center and see statistics there
        h, w, _ = img.shape
        center_crop = img[int(h/3):int(2*h/3), int(w/3):int(2*w/3)]
        print(f"Center Crop Mean: {np.mean(center_crop)}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    analyze_debug_image()
