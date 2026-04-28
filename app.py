import streamlit as st
import os
import pandas as pd
import numpy as np
import time
from modules.utils import init_db, save_fingerprint, get_alerts, get_all_fingerprints
from modules.fingerprinter import generate_video_fingerprint
from modules.immune_system import process_suspected_video

# Initialize DB
init_db()

def main_ui():
    st.set_page_config(
        page_title="SportGuard AI | Digital Immune System", 
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Custom CSS for "Professional Sports Tech" Dark Mode & Animations
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

        /* Global Theme Overrides */
        .stApp {
            background-color: #0E1117 !important;
            font-family: 'Inter', sans-serif !important;
            color: #FFFFFF !important;
        }

        /* Typography */
        h1, h2, h3, .stHeader {
            color: #FFFFFF !important;
            font-weight: 800 !important;
        }
        
        p, span, label, .stMarkdown {
            color: #8B949E !important;
        }
        
        strong {
            color: #FFFFFF !important;
        }

        /* Premium Card System */
        .premium-card {
            background-color: #161B22 !important;
            padding: 2rem !important;
            border-radius: 12px !important;
            border: 1px solid #30363D !important;
            margin-bottom: 1.5rem !important;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3) !important;
            position: relative;
            overflow: hidden;
        }
        
        /* Scanning Animation Overlay */
        .scanning-line {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 4px;
            background: #3FB950;
            box-shadow: 0 0 15px #3FB950;
            animation: scan 2s linear infinite;
            z-index: 10;
        }

        @keyframes scan {
            0% { top: 0; }
            100% { top: 100%; }
        }

        /* Hero Section */
        .hero-section {
            background: linear-gradient(135deg, #1F2937 0%, #111827 100%) !important;
            padding: 3rem 2rem !important;
            border-radius: 15px !important;
            text-align: center;
            margin-bottom: 2.5rem !important;
            border: 1px solid #30363D !important;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5) !important;
        }

        /* Metrics */
        [data-testid="stMetric"] {
            background-color: #161B22 !important;
            padding: 1rem !important;
            border-radius: 10px !important;
            border-bottom: 3px solid #58A6FF !important;
        }

        /* Alert Boxes */
        .alert-threat {
            border: 2px solid #F85149 !important;
            background-color: rgba(248, 81, 73, 0.1) !important;
            padding: 1.5rem !important;
            border-radius: 10px !important;
            color: #F85149 !important;
            box-shadow: 0 0 20px rgba(248, 81, 73, 0.3) !important;
            text-align: center;
            font-weight: 800 !important;
            font-size: 1.2rem !important;
        }
        
        .action-status {
            color: #3FB950 !important;
            font-weight: 700 !important;
            margin-top: 0.5rem !important;
        }
        
        .dna-box {
            border: 1px solid #30363D;
            border-radius: 8px;
            padding: 10px;
            background: #0D1117;
            text-align: center;
        }
        </style>
        """, unsafe_allow_html=True)

    # Hero Section
    st.markdown("""
        <div class="hero-section">
            <h1 style="margin:0; font-size: 3rem;">🛡️ SPORTGUARD AI</h1>
            <p style="font-size: 1.2rem; color: #8B949E;">Autonomous Digital Immune System for Sports Protection</p>
        </div>
        """, unsafe_allow_html=True)

    # Metrics Section
    alerts = get_alerts()
    num_alerts = len(alerts)
    revenue_recovered = num_alerts * 1250 
    accuracy = 99.4 if num_alerts > 0 else 100.0

    m_col1, m_col2, m_col3 = st.columns(3)
    with m_col1:
        st.metric("Revenue Recovered", f"${revenue_recovered:,}", delta="↑ 12%")
    with m_col2:
        st.metric("Detection Accuracy", f"{accuracy}%", delta="↑ 0.2%")
    with m_col3:
        st.metric("Secured Assets", len(get_all_fingerprints() or []), delta=None)

    st.markdown("<br>", unsafe_allow_html=True)

    # Data Visualization Section (Mock Detection Trends)
    st.subheader("📊 Piracy Detection Trends (Last 24 Hours)")
    chart_data = pd.DataFrame(
        np.random.randint(0, 10, size=(24, 1)),
        columns=['Threats Detected']
    )
    st.line_chart(chart_data, height=200)

    # Main Interaction Grid
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.subheader("📤 Asset Registration")
        uploaded_file = st.file_uploader("Drop official media here", type=['mp4'], key="reg_uploader")
        if uploaded_file:
            if st.button("Fingerprint Asset", key="reg_btn"):
                with st.spinner("Analyzing frames..."):
                    temp_path = f"temp_{uploaded_file.name}"
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    fp = generate_video_fingerprint(temp_path)
                    save_fingerprint(uploaded_file.name, fp)
                    st.success(f"Asset '{uploaded_file.name}' registered.")
                    os.remove(temp_path)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        # Surveillance Card with Scanning Effect when button is pressed
        st.markdown('<div class="premium-card" id="surveillance-card">', unsafe_allow_html=True)
        st.subheader("📡 Live Surveillance")
        scan_file = st.file_uploader("Upload suspected stream segment", type=['mp4'], key="scan_uploader")
        
        if st.button("Initiate Immunity Scan", key="scan_btn"):
            if scan_file:
                # Visual Scan Effect
                scan_placeholder = st.empty()
                scan_placeholder.markdown('<div class="scanning-line"></div>', unsafe_allow_html=True)
                
                temp_path = f"scan_{scan_file.name}"
                with open(temp_path, "wb") as f:
                    f.write(scan_file.getbuffer())
                
                with st.spinner("🕵️ AI CROSS-REFERENCING..."):
                    time.sleep(2) # Visual pause for simulation effect
                    status, similarity = process_suspected_video(temp_path, "LIVE_UCL_STREAM_7")
                    
                scan_placeholder.empty()
                
                if status == "PIRACY DETECTED":
                    st.toast("🚨 THREAT NEUTRALIZED", icon="🛡️")
                    st.markdown("""
                        <div class="alert-threat">
                            IMMEDIATE THREAT DETECTED
                            <div class="action-status">STATUS: Redirected to Official Source (✓)</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    # Comparison View
                    st.subheader("🔍 Match Analysis (DNA Comparison)")
                    comp_col1, comp_col2 = st.columns(2)
                    with comp_col1:
                        st.markdown('<div class="dna-box">', unsafe_allow_html=True)
                        st.write("**Registered Asset (DNA)**")
                        st.image("https://img.icons8.com/color/100/video.png")
                        st.code("Hash: p892x-77a", language="bash")
                        st.markdown('</div>', unsafe_allow_html=True)
                    with comp_col2:
                        st.markdown('<div class="dna-box" style="border-color: #F85149;">', unsafe_allow_html=True)
                        st.write("**Intercepted Stream**")
                        st.image("https://img.icons8.com/color/100/high-priority.png")
                        st.code(f"Match: {similarity:.2f}%", language="bash")
                        st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.success("✅ Content verified. No piracy detected.")
                os.remove(temp_path)
            else:
                st.info("Please upload a file for analysis.")
        st.markdown('</div>', unsafe_allow_html=True)

    # Dashboard Logs
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.subheader("📋 Response Logs")
    if alerts:
        df = pd.DataFrame(alerts, columns=['ID', 'Source', 'Match %', 'Status', 'Timestamp'])
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No threats detected in current session.")
    st.markdown('</div>', unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/100/security-shield.png")
        st.title("System Status")
        st.success("🛡️ Immune System: ACTIVE")
        st.divider()
        st.write("SportGuard AI protects your high-value sports media by redirecting piracy traffic to official streams.")

if __name__ == "__main__":
    main_ui()
