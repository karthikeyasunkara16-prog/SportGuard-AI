from .utils import log_piracy_alert, get_all_fingerprints
from .surveillance import scan_video_for_piracy

SIMILARITY_THRESHOLD = 85.0

def process_suspected_video(video_path, source_url):
    """
    Main entry point for checking a video and taking action.
    """
    official_fps = get_all_fingerprints()
    if not official_fps:
        return "No official content registered.", 0
        
    similarity = scan_video_for_piracy(video_path, official_fps)
    
    if similarity >= SIMILARITY_THRESHOLD:
        log_piracy_alert(source_url, similarity)
        return "PIRACY DETECTED", similarity
    else:
        return "CONTENT CLEAR", similarity

def get_redirection_mock():
    """
    Simulates the response mechanism (e.g., overlaying a legal stream link).
    """
    return {
        "message": "This stream is unauthorized.",
        "action": "Redirecting to official broadcaster...",
        "official_url": "https://official-sports-stream.com/live"
    }
