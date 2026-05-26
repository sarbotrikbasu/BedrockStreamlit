import streamlit as st
import boto3
import uuid

# =========================================================
# CONFIGURATION
# =========================================================

AWS_REGION = "eu-north-1"

AGENT_ID = "WXOBDKULXJ"
AGENT_ALIAS_ID = "T2ZRFFTKLX"

# =========================================================
# BEDROCK CLIENT
# =========================================================

client = boto3.client(
    "bedrock-agent-runtime",
    region_name=st.secrets["AWS_DEFAULT_REGION"],
    aws_access_key_id=st.secrets["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=st.secrets["AWS_SECRET_ACCESS_KEY"]
)

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Orivis Alpha",
    page_icon="📈",
    layout="wide"
)

# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# =========================================================
# HEADER
# =========================================================

st.title("📈 Orivis Alpha")
st.caption("Institutional-Grade AI Forex Trading Assistant")

# =========================================================
# CHAT HISTORY
# =========================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# =========================================================
# USER INPUT
# =========================================================

prompt = st.chat_input(
    "Ask about forex market opportunities..."
)

# =========================================================
# PROCESS USER MESSAGE
# =========================================================

if prompt:

    # Store user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant response
    with st.chat_message("assistant"):

        message_placeholder = st.empty()

        full_response = ""

        try:

            response = client.invoke_agent(
                agentId=AGENT_ID,
                agentAliasId=AGENT_ALIAS_ID,
                sessionId=st.session_state.session_id,
                inputText=prompt
            )

            # Stream chunks
            for event in response.get("completion"):

                chunk = event.get("chunk")

                if chunk:

                    decoded_chunk = (
                        chunk["bytes"]
                        .decode("utf-8")
                    )

                    full_response += decoded_chunk

                    message_placeholder.markdown(
                        full_response + "▌"
                    )

            # Final response
            message_placeholder.markdown(
                full_response
            )

        except Exception as e:

            full_response = (
                f"Error: {str(e)}"
            )

            message_placeholder.error(
                full_response
            )

    # Save assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": full_response
    })

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("Orivis Alpha")

    st.markdown("""
    ### Features

    - Live Forex Market Analysis
    - Fibonacci Signals
    - RSI Analytics
    - Moving Average Signals
    - Probability Scoring
    - Institutional Trade Summaries
    """)

    st.divider()

    if st.button("Clear Chat"):

        st.session_state.messages = []

        st.session_state.session_id = (
            str(uuid.uuid4())
        )

        st.rerun()
