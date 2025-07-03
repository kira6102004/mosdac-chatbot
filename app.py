# app.py
import streamlit as st
from chatbot_backend import ask_mosdac_bot
import time

st.set_page_config(page_title="MOSDAC Chatbot", page_icon="🛰️", layout="centered")

# Theme toggle
st.sidebar.header("🎨 Theme")
dark_mode = st.sidebar.toggle("Dark Mode", value=True)
if dark_mode:
    st.markdown("""
        <style>
            body, .stApp { background-color: #0f0f23; color: #e0e0f0; }
            .stTextInput>div>div>input { background-color: #1f1f3b; color: white; border: 1px solid #7b61ff; }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
            body, .stApp { background-color: #f5f5f5; color: #222; }
            .stTextInput>div>div>input { background-color: #ffffff; color: #222; border: 1px solid #7b61ff; }
        </style>
    """, unsafe_allow_html=True)

# Sidebar file uploader
st.sidebar.header("📎 Optional File Upload")
uploaded_file = st.sidebar.file_uploader("Upload a PDF", type="pdf")
if uploaded_file:
    st.sidebar.info("Note: PDF chat is not integrated in this version, file is not processed.")

# Header with animation and tip
st.markdown("""
    <div style='text-align: center;'>
        <h1 style='color: #c7b6ff; text-shadow: 0 0 12px #9b59ff; animation: pulse 2s infinite;'>🛰️ MOSDAC Chatbot</h1>
        <p style='font-style: italic; color: #aaa;'>
        <b>Pro Tip:</b> Ask things like <i>\"What are INSAT satellites?\"</i> or <i>\"Applications of SCATSAT-1\"</i> 💡
        </p>
    </div>
    <style>
        @keyframes pulse {
            0% { text-shadow: 0 0 12px #9b59ff; }
            50% { text-shadow: 0 0 20px #9b59ff, 0 0 30px #9b59ff; }
            100% { text-shadow: 0 0 12px #9b59ff; }
        }
    </style>
""", unsafe_allow_html=True)

# Typing animation function
def type_text(text, speed=0.01):
    container = st.empty()
    typed = ""
    for char in text:
        typed += char
        container.markdown(f"<div style='font-size: 18px; line-height: 1.6;'>{typed}</div>", unsafe_allow_html=True)
        time.sleep(speed)

# Input + Answer Section
user_input = st.text_input("Ask a question")

if user_input:
    with st.spinner("Thinking..."):
        answer, sources, speculative = ask_mosdac_bot(user_input)

        st.subheader("💬 Answer")
        type_text(answer)

        st.subheader("📚 Sources")
        query_str = user_input.strip().replace(" ", "+")
        mosdac_url = f"https://www.mosdac.gov.in/search/node/{query_str}"
        st.markdown(f"- [Related content on MOSDAC.gov.in]({mosdac_url})")

# Footer badge
st.markdown("""
    <hr style='margin-top: 40px;'/>
    <div style='text-align: right; font-size: 12px; opacity: 0.6; border: 1px solid #7b61ff; border-radius: 6px; padding: 4px 10px; display: inline-block; float: right;'>
        🛠️ Powered by <b>V-botics</b>
    </div>
""", unsafe_allow_html=True)