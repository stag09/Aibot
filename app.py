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

# Initialize Cohere client (V2 SDK)
co = cohere.ClientV2(api_key=cohere_api_key)

# ================= Streamlit Page =================
st.set_page_config(page_title="Cohere Chatbot", page_icon="🤖")
st.title("💬 AI ChatAgent 🤖")

# Store messages in session
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ================= Helper: Live Data Fetch =================
def fetch_live_info(query):
    try:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query.replace(' ', '_')}"
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            data = res.json()
            return data.get("extract", "")
    except:
        pass
    return ""

# ================= User Input =================
if prompt := st.chat_input("Type your question..."):
    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get live info
    live_info = fetch_live_info(prompt)

    # Cohere response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = co.chat(
                model="command-a-03-2025",  # Latest model
                messages=[
                    {"role": "user", "content": f"{prompt}. Context: {live_info}"}
                ]
            )
            reply = response.message.content[0].text.strip()
            st.markdown(reply)

    # Save assistant message
    st.session_state.messages.append({"role": "assistant", "content": reply})
