import os
from modules.utils import init_db, save_fingerprint, get_all_fingerprints
from modules.immune_system import process_suspected_video

def test_system():
    print("Initializing Database...")
    init_db()
    
    # Mock some data if needed, but the modules should handle empty state
    fps = get_all_fingerprints()
    print(f"Current fingerprints in DB: {len(fps)}")
    
    print("System check complete. Run 'streamlit run app.py' to test the full UI.")

if __name__ == "__main__":
    test_system()
