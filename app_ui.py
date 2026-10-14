import streamlit as st
import requests
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="FindAm Voice Resolver",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Deep Navy Blue Palette & Centered Mic Control Styling
st.markdown("""
    <style>
    /* Global App Background */
    .stApp {
        background-color: #F8FAFC !important;
        color: #0F172A;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    /* Top Header */
    .brand-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background-color: #FFFFFF;
        padding: 16px 28px;
        border-radius: 12px;
        border: 1px solid #CBD5E1;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 24px;
    }
    .brand-title {
        font-size: 24px;
        font-weight: 800;
        color: #1E3A8A !important;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .brand-sub {
        font-size: 13px;
        background-color: #EFF6FF;
        color: #1E3A8A;
        padding: 6px 16px;
        border-radius: 20px;
        font-weight: 700;
        border: 1px solid #BFDBFE;
    }

    /* Hero Postcode Box */
    .postcode-card {
        background-color: #FFFFFF;
        border: 2px solid #1E3A8A;
        padding: 24px;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 10px 15px -3px rgba(30, 58, 138, 0.08);
        margin-bottom: 20px;
    }
    .postcode-label {
        font-size: 12px;
        letter-spacing: 2px;
        text-transform: uppercase;
        font-weight: 800;
        color: #1E3A8A;
        margin-bottom: 8px;
    }
    .postcode-value {
        font-size: 36px;
        font-weight: 900;
        letter-spacing: 3px;
        color: #1E3A8A;
    }

    /* Spatial Metadata Cards */
    .info-card {
        background-color: #FFFFFF;
        border: 1px solid #CBD5E1;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 12px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
    }
    .info-label {
        font-size: 11px;
        text-transform: uppercase;
        color: #1E3A8A;
        font-weight: 800;
        letter-spacing: 1.5px;
        margin-bottom: 6px;
    }
    .info-value {
        font-size: 18px;
        font-weight: 700;
        color: #0F172A;
    }

    /* Centered Action Dock Container */
    .voice-card-container {
        background-color: #FFFFFF;
        border: 2px solid #1E3A8A;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 8px 20px rgba(30, 58, 138, 0.08);
        text-align: center;
        margin-top: 10px;
    }
    .voice-instruction {
        font-size: 18px;
        font-weight: 800;
        color: #1E3A8A !important;
        margin-bottom: 12px;
        text-align: center;
    }

    /* Center and enlarge the native Streamlit audio input controls */
    div[data-testid="stAudioInput"] {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        width: 100% !important;
        margin: 0 auto !important;
    }
    div[data-testid="stAudioInput"] > div {
        width: 100% !important;
        border-radius: 12px !important;
        border: 1px solid #BFDBFE !important;
        background-color: #EFF6FF !important;
        padding: 8px !important;
    }

    /* Custom Styling for Primary Navy Blue Button */
    button[data-testid="stBaseButton-primary"], 
    div.stButton > button {
        background-color: #1E3A8A !important;
        border-color: #1E3A8A !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        border-radius: 10px !important;
        height: 48px !important;
        box-shadow: 0 4px 6px -1px rgba(30, 58, 138, 0.2) !important;
        margin-top: 12px;
    }
    button[data-testid="stBaseButton-primary"]:hover, 
    div.stButton > button:hover {
        background-color: #1E40AF !important;
        border-color: #1E40AF !important;
    }
    </style>
""", unsafe_allow_html=True)

# 1. TOP HEADER
st.markdown("""
    <div class="brand-header">
        <h1 class="brand-title">🎙️ FindAm Voice Resolver</h1>
        <span class="brand-sub">Powered by N-ATLAS</span>
    </div>
""", unsafe_allow_html=True)

# Session state initialization
if "resolved_data" not in st.session_state:
    st.session_state.resolved_data = None

# 2. MAIN RESULTS DISPLAY AREA
results_container = st.container()

with results_container:
    if st.session_state.resolved_data:
        res = st.session_state.resolved_data
        parsed = res['parsed_address']
        coords = res.get('coordinates', {"latitude": 9.0765, "longitude": 7.4985})

        # Hero Postcode Card
        st.markdown(f"""
            <div class="postcode-card">
                <div class="postcode-label">Generated Digital Postcode</div>
                <div class="postcode-value">{res['digital_postcode']}</div>
            </div>
        """, unsafe_allow_html=True)

        # 2x2 Spatial Information Grid
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"""
                <div class="info-card">
                    <div class="info-label">State</div>
                    <div class="info-value">🇳🇬 {parsed['state']}</div>
                </div>
                <div class="info-card">
                    <div class="info-label">Neighborhood</div>
                    <div class="info-value">🏘️ {parsed['neighborhood']}</div>
                </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
                <div class="info-card">
                    <div class="info-label">LGA</div>
                    <div class="info-value">🏛️ {parsed['lga']}</div>
                </div>
                <div class="info-card">
                    <div class="info-label">Landmark</div>
                    <div class="info-value">📍 {parsed['landmark']}</div>
                </div>
            """, unsafe_allow_html=True)

        # Map display
        map_df = pd.DataFrame([{'lat': coords['latitude'], 'lon': coords['longitude']}])
        st.map(map_df, zoom=13, size=20, use_container_width=True)
    else:
        # Clean Empty Placeholder State
        st.markdown("""
            <div class="postcode-card" style="border: 2px dashed #94A3B8; background-color: #F1F5F9;">
                <div class="postcode-label" style="color: #475569;">Digital Postcode Placeholder</div>
                <div class="postcode-value" style="color: #1E3A8A;">FC-XXX-XXXXXX</div>
            </div>
        """, unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="info-card"><div class="info-label">State</div><div class="info-value" style="color: #94A3B8;">--</div></div>', unsafe_allow_html=True)
            st.markdown('<div class="info-card"><div class="info-label">Neighborhood</div><div class="info-value" style="color: #94A3B8;">--</div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="info-card"><div class="info-label">LGA</div><div class="info-value" style="color: #94A3B8;">--</div></div>', unsafe_allow_html=True)
            st.markdown('<div class="info-card"><div class="info-label">Landmark</div><div class="info-value" style="color: #94A3B8;">--</div></div>', unsafe_allow_html=True)

# 3. CENTERED VOICE INPUT & TESTER DETAILS DOCK
st.markdown("<br>", unsafe_allow_html=True)

_, center_col, _ = st.columns([1, 2, 1])

with center_col:
    st.markdown('<div class="voice-card-container">', unsafe_allow_html=True)
    st.markdown('<div class="voice-instruction">🎙️ Tap the Microphone Icon Below to Speak</div>', unsafe_allow_html=True)
    
    # Audio recorder widget
    recorded_audio = st.audio_input("Record audio", label_visibility="collapsed")
    
    # Tester details input
    t_col1, t_col2 = st.columns(2)
    with t_col1:
        tester_name = st.text_input("Tester Name", value="David Johnson", placeholder="Enter your name")
    with t_col2:
        tester_phone = st.text_input("Phone Number", value="08000000000", placeholder="Enter phone number")
        
    process_btn = st.button("🚀 Resolve Address", type="primary", use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    if process_btn:
        if recorded_audio is None:
            st.warning("Please record audio before tapping Resolve Address.")
        else:
            files = {"file": ("recorded_mic.wav", recorded_audio.getvalue(), "audio/wav")}
            data = {
                "tester_name": tester_name,
                "user_phone": tester_phone
            }
            
            with st.spinner("N-ATLAS Engine parsing voice..."):
                try:
                    response = requests.post("http://127.0.0.1:8000/api/v1/voice-address", files=files, data=data)
                    if response.status_code == 200:
                        st.session_state.resolved_data = response.json()
                        st.rerun()
                    else:
                        st.error("Engine response error. Check backend logs.")
                except Exception:
                    st.error("Engine offline. Ensure main.py is running on port 8000.")