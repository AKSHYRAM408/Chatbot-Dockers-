# CI/CD test
import streamlit as st
import os
import threading
from dotenv import load_dotenv
from mistralai import Mistral
from prometheus_client import start_http_server, Counter, Histogram
import time
def start_metrics_server():
    start_http_server(8000)

threading.Thread(target=start_metrics_server, daemon=True).start()

from prometheus_client import REGISTRY

if 'chatbot_requests_total' not in REGISTRY._names_to_collectors:
    REQUEST_COUNT = Counter('chatbot_requests_total', 'Total chat requests')
    RESPONSE_TIME = Histogram('chatbot_response_seconds', 'Response time in seconds')
else:
    REQUEST_COUNT = REGISTRY._names_to_collectors['chatbot_requests_total']
    RESPONSE_TIME = REGISTRY._names_to_collectors['chatbot_response_seconds']

# Load environment variables from .env file
load_dotenv()

# --- Page Config ---
st.set_page_config(
    page_title="Ask Me AnyThing",
    page_icon=" ",
    layout="centered",
)

# --- Custom CSS for a polished look ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .main-header {
        text-align: center;
        padding: 1.5rem 0 0.5rem 0;
    }

    .main-header h1 {
        background: linear-gradient(135deg, #6366f1, #8b5cf6, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.4rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }

    .main-header p {
        color: #94a3b8;
        font-size: 1rem;
        margin-top: 0;
    }

    .stChatMessage {
        border-radius: 12px !important;
        margin-bottom: 0.5rem !important;
    }

    div[data-testid="stChatInput"] textarea {
        border-radius: 12px !important;
    }

    .footer {
        text-align: center;
        color: #64748b;
        font-size: 0.78rem;
        padding: 2rem 0 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
<div class="main-header">
    <h1>Ask me anything</h1>
    <p>Any thime <strong>AnyWhere</strong> — Ask me anything!</p>
</div>
""", unsafe_allow_html=True)

st.divider()

api_key = os.getenv("MISTRAL_API_KEY")

if not api_key:
    st.error("⚠️ **MISTRAL_API_KEY** not found! Please set it in your `.env` file.")
    st.stop()

client = Mistral(api_key=api_key)
MODEL = "mistral-large-latest"

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hey there! 👋 I'm your Personal AI assistant. How can I help you today?",
        }
    ]

# --- Display Chat History ---
for message in st.session_state.messages:
    avatar = "🤖" if message["role"] == "assistant" else "🧑‍💻"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

if prompt := st.chat_input("Type your message here..."):
    # Increment request counter
    REQUEST_COUNT.inc()

    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)

    # Call Mistral API with full chat history
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Thinking..."):
            try:
                start = time.time()
                response = client.chat.complete(
                    model=MODEL,
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ],
                )
                RESPONSE_TIME.observe(time.time() - start)
                assistant_reply = response.choices[0].message.content
            except Exception as e:
                assistant_reply = f"❌ Error: {str(e)}"

        st.markdown(assistant_reply)

    # Add assistant reply to history
    st.session_state.messages.append(
        {"role": "assistant", "content": assistant_reply}
    )

# --- Footer ---
st.markdown("""
<div class="footer">
    Built with ❤️ using Streamlit & Mistral AI &nbsp;|&nbsp; Dockerized for deployment on Railway.app
</div>
""", unsafe_allow_html=True)
