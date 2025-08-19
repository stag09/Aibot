import streamlit as st
import cohere
import os
import requests
from dotenv import load_dotenv

# ================= CSS Styling ==================
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #89f7fe 0%, #66a6ff 100%);
        color: #000 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .stChatMessage {
        padding: 12px;
        border-radius: 12px;
        margin-bottom: 8px;
        font-size: 16px;
        line-height: 1.4;
        color: #000 !important;
    }
    .stChatMessage.user {
        background-color: #d0f0fd;
        border-left: 5px solid #2196f3;
    }
    .stChatMessage.assistant {
        background-color: #a3d8f4;
        border-left: 5px solid #0d47a1;
    }
    div[data-baseweb="textarea"] > textarea {
        background-color: white;
        color: #000 !important;
        border-radius: 10px;
        border: 1px solid #2196f3;
        font-size: 16px;
    }
    h1 {
        text-align: center;
        color: #003366;
        font-weight: bold;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ================= Load API Key =================
load_dotenv()
cohere_api_key = os.getenv("COHERE_API_KEY")
co = cohere.ClientV2(api_key=cohere_api_key)

# ================= Streamlit Page =================
st.set_page_config(page_title="Cohere Chatbot", page_icon="🤖")
st.title("💬 AI ChatAgent with Live Data 🤖")

# ================= Helper: Live Wikipedia Fetch =================
def fetch_live_info(query):
    """Fetch summary from Wikipedia for live updates"""
    try:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query.replace(' ', '_')}"
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            data = res.json()
            return data.get("extract", "")
    except Exception:
        return ""
    return ""

# ================= Memory =================
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ================= Chat =================
if prompt := st.chat_input("Ask me anything..."):
    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Step 1: Try live Wikipedia data
    live_info = fetch_live_info(prompt)

    # Step 2: Ask Cohere with live info injected
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = co.chat(
                model="command-a-03-2025",  # ✅ latest chat model
                messages=[{"role": "user", "content": f"Question: {prompt}\n\nLive Data: {live_info}"}]
            )
            reply = response.message.content[0].text.strip()

            # Prefer Wikipedia if available
            if live_info:
                reply = f"{live_info}\n\n(Source: Wikipedia)\n\nCohere adds: {reply}"

            st.markdown(reply)

    # Save assistant message
    st.session_state.messages.append({"role": "assistant", "content": reply})
