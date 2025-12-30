import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
import datetime

# --- CONFIGURATION ---
API_KEY = ""
client = genai.Client(api_key=API_KEY)

st.set_page_config(page_title="Gemini 3 Full Hub", layout="wide")

# --- INITIALIZE STATE ---
if "history" not in st.session_state:
    st.session_state.history = []
if "viewing_history" not in st.session_state:
    st.session_state.viewing_history = None

# Callback to clear view when new input is started
def start_new_query():
    st.session_state.viewing_history = None

# --- SIDEBAR: CLICKABLE HISTORY ---
with st.sidebar:
    st.title("📜 History")
    if st.button("➕ New Chat"):
        start_new_query()
        st.rerun()
    
    st.divider()
    
    # Create a button for each history entry
    for i, entry in enumerate(reversed(st.session_state.history)):
        # button label shows time and snippet
        if st.sidebar.button(f"🕒 {entry['time']} - {entry['mode']}", key=f"hist_{i}"):
            st.session_state.viewing_history = entry
            st.rerun()

# --- MAIN UI LOGIC ---

# 1. IF USER IS VIEWING HISTORY
if st.session_state.viewing_history:
    hist = st.session_state.viewing_history
    st.title(f"🔍 Viewing History: {hist['mode']}")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(f"**Prompt:**\n> {hist['prompt']}")
    with col2:
        st.subheader("Gemini's Response:")
        st.success(hist['response'])
    
    if st.button("← Back to Workspace"):
        start_new_query()
        st.rerun()

# 2. IF USER IS IN ACTIVE WORKSPACE
else:
    st.title("🤖 Gemini 3 Active Workspace")
    mode = st.selectbox("Select Mode:", ["Text Mode", "Image Mode", "Speech Mode"])
    
    contents = []
    prompt_text = ""

    if mode == "Text Mode":
        prompt_text = st.text_area("Message:", on_change=start_new_query)
        contents = [prompt_text]

    elif mode == "Image Mode":
        prompt_text = st.text_input("Instruction:", on_change=start_new_query)
        uploaded_img = st.file_uploader("Upload Image", on_change=start_new_query)
        if uploaded_img:
            img = Image.open(uploaded_img)
            st.image(img, width=300)
            contents = [prompt_text, img]

    elif mode == "Speech Mode":
        prompt_text = st.text_input("Instruction:", on_change=start_new_query)
        audio_val = st.audio_input("Record Voice", on_change=start_new_query)
        if audio_val:
            contents = [prompt_text, types.Part.from_bytes(data=audio_val.read(), mime_type="audio/wav")]

    if st.button("Run Gemini 3"):
        if contents:
            try:
                with st.spinner("Processing..."):
                    response = client.models.generate_content(model='gemini-3-flash-preview', contents=contents)
                
                # Save to history
                new_entry = {
                    "time": datetime.datetime.now().strftime("%H:%M:%S"),
                    "mode": mode,
                    "prompt": prompt_text,
                    "response": response.text
                }
                st.session_state.history.append(new_entry)
                st.write(response.text)
            except Exception as e:
                st.error(f"Error: {e}")