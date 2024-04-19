from openai import OpenAI
import streamlit as st
import os


os.getenv("OPENAI_API_KEY")

client = OpenAI()

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4-0125-preview"

if "record" not in st.session_state:
    st.session_state.record = []

st.subheader("GPT-4")

for message in st.session_state.record:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.record.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.record
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.record.append({"role": "assistant", "content": response})
