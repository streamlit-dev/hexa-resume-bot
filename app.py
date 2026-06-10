import streamlit as st
from groq import Groq

st.set_page_config(page_title="Suman's Resume Bot", page_icon="🤖")
st.title("🤖 Ask Me About Suman's Resume")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask about my experience..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are Suman's resume assistant. Suman is a Data Analyst with 3+ years experience in Python, SQL, Power BI, Streamlit. Built 20+ dashboards. Expert in data visualization and automation."},
                *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
