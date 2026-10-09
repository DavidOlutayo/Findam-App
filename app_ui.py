import streamlit as st
import requests

st.title("🎙️ FindAm - Voice Address Resolver")
st.subheader("Send voice note, make we FindAm!")

st.write("Record or upload an audio file describing an address in Pidgin, Hausa, Yoruba, Igbo, or English.")

audio_file = st.file_uploader("Upload or Record Audio", type=["wav", "mp3", "ogg", "m4a"])
user_phone = st.text_input("Your Name / Phone Number (For testing count)", "Tester_1")

if st.button("Process Address with N-ATLAS"):
    if audio_file is not None:
        files = {"file": (audio_file.name, audio_file.getvalue(), audio_file.type)}
        data = {"user_phone": user_phone}
        
        with st.spinner("N-ATLAS AI is parsing your voice note..."):
            try:
                response = requests.post("http://127.0.0.1:8000/api/v1/voice-address", files=files, data=data)
                
                if response.status_code == 200:
                    res = response.json()
                    st.success("Address Successfully Resolved!")
                    st.write(f"**Raw Transcript:** {res['raw_transcript']}")
                    st.write(f"**Digital Postcode:** `{res['digital_postcode']}`")
                    st.json(res['parsed_address'])
                else:
                    st.error("Error connecting to FindAm engine.")
            except Exception as e:
                st.error("Make sure your main.py server is running!")
    else:
        st.warning("Please record or upload an audio file first!")

st.divider()

# Live interaction counter for NAIC competition requirements
try:
    stats = requests.get("http://127.0.0.1:8000/api/v1/validation-stats").json()
    st.metric(label="Total Real User Interactions Recorded", value=f"{stats['total_real_user_interactions']} / 50")
except Exception:
    pass