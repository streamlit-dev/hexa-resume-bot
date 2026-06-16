import streamlit as st
from groq import Groq

client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)
# Page Configuration
st.set_page_config(
    page_title="Suman's Resume Bot",
    page_icon="🤖",
    layout="centered"
)

# Title
st.title("🤖 Ask Me About Suman's Resume")

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Previous Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Resume Information
SYSTEM_PROMPT = """
You are Suman's Resume Assistant.

Suman is a Data Analyst with 3+ years of experience in:
- Python
- SQL
- Power BI
- Streamlit

Key Achievements:
- Built 20+ interactive dashboards
- Automated reporting processes
- Strong expertise in data visualization
- Skilled in data cleaning and analysis
- Experienced in business intelligence solutions

Answer questions professionally and confidently based on this information.
"""

# User Input
prompt = st.chat_input("Ask about my experience, skills, or projects...")

if prompt:
    # Show User Message
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Initialize Groq Client
        client = Groq(
            api_key=st.secrets["GROQ_API_KEY"]
        )

        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model="llama-3.1-8b-instant",
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

    except KeyError:
        st.error(
            "GROQ_API_KEY not found. Please add it to Streamlit secrets."
        )

    except Exception as e:
        st.error(f"Error: {str(e)}")
