import streamlit as st
from groq import Groq

# Page Configuration
st.set_page_config(
    page_title="Suman's Resume Bot",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Ask Me About Suman's Resume")

# Initialize Groq Client
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# System Prompt
SYSTEM_PROMPT = """
You are Suman's Resume Assistant.

Suman is a Data Analyst with 3+ years of experience in:
- Python
- SQL
- Power BI
- Streamlit

Achievements:
- Built 20+ dashboards
- Expert in data visualization
- Skilled in automation and reporting
- Strong analytical and problem-solving abilities

Answer questions professionally and confidently.
"""

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Previous Messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User Input
prompt = st.chat_input("Ask about my experience...")

if prompt:
    # Save User Message
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Response
    with st.chat_message("assistant"):
        response_placeholder = st.empty()

        stream = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                *st.session_state.messages
            ],
            stream=True
        )

        response = st.write_stream(stream)

    # Save Assistant Response
    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )
