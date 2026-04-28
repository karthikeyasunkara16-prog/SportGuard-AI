import cv2
import imagehash
from PIL import Image
import numpy as np

def generate_video_fingerprint(video_path):
    """
    Generates a consolidated fingerprint for a video by hashing frames.
    For simplicity, we hash every 30th frame and join them.
    """
    cap = cv2.VideoCapture(video_path)
    hashes = []
    count = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        if count % 30 == 0:
            # Convert OpenCV BGR to RGB for PIL
            img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            h = str(imagehash.phash(img))
            hashes.append(h)
        
        count += 1
    
    cap.release()
    return ",".join(hashes)

def compare_fingerprints(fp1, fp2):
    """
    Compares two comma-separated hash strings and returns similarity percentage.
    """
    hashes1 = fp1.split(",")
    hashes2 = fp2.split(",")
    
    matches = 0
    total = max(len(hashes1), len(hashes2))
    
    if total == 0: return 0
    
    # Simple set-based matching for demonstration
    set1 = set(hashes1)
    set2 = set(hashes2)
    
    common = set1.intersection(set2)
    return (len(common) / total) * 100
