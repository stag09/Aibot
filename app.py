import streamlit as st
import cohere
import os
from dotenv import load_dotenv


st.markdown(
    """
    <style>
    /* Cool blue-green gradient background */
    .stApp {
        background: linear-gradient(135deg, #89f7fe 0%, #66a6ff 100%);
        color: #000 !important;  /* Black text */
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Chat bubbles */
    .stChatMessage {
        padding: 12px;
        border-radius: 12px;
        margin-bottom: 8px;
        font-size: 16px;
        line-height: 1.4;
        color: #000 !important; /* Black text inside bubbles */
    }

    /* User bubble */
    .stChatMessage.user {
        background-color: #d0f0fd;
        border-left: 5px solid #2196f3;
        color: #000 !important;
    }

    /* Assistant bubble */
    .stChatMessage.assistant {
        background-color: #a3d8f4;
        border-left: 5px solid #0d47a1;
        color: #000 !important;
    }

    /* Chat input box */
    div[data-baseweb="textarea"] > textarea {
        background-color: white;
        color: #000 !important;
        border-radius: 10px;
        border: 1px solid #2196f3;
        font-size: 16px;
    }

    /* Title */
    h1 {
        text-align: center;
        color: #003366; /* Dark navy */
        font-weight: bold;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Load environment variables
load_dotenv()
cohere_api_key = os.getenv("COHERE_API_KEY")

# Initialize Cohere client
co = cohere.Client(cohere_api_key)

# Page config
st.set_page_config(page_title="Cohere Chatbot", page_icon="🤖")
st.title("💬 AI Chatbot 🤖")

# Store messages in session
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if prompt := st.chat_input("Type your question..."):
    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get Cohere response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = co.generate(
                model="command-r-plus",
                prompt=prompt,
                max_tokens=3000
            )
            reply = response.generations[0].text.strip()
            st.markdown(reply)

    # Save assistant message
    st.session_state.messages.append({"role": "assistant", "content": reply})
