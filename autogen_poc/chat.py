from openai import OpenAI
import streamlit as st
import os

os.getenv("OPENAI_API_KEY")


def getupdatedprompt(prompt):
    prompt = prompt

    return prompt



st.title("Yanok Language Training")

client = OpenAI()

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4-turbo-preview"

if "record" not in st.session_state:
    st.session_state.record = []
    st.session_state.internalmessages = []
    st.session_state.internalmessages.append({"role": "system", "content": "You are a language teacher for Chinese. Giving instructions in English, please print the top 10 nouns and verbs in Chinese only and (in English) ask the user to translate. Based on the user's performance, switch to Chinese if the user translates over 9/10 correctly."})


for message in st.session_state.record:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.record.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    revisedprompt = getupdatedprompt(prompt)    
    st.session_state.internalmessages.append({"role": "user", "content": revisedprompt})
    
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.internalmessages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.record.append({"role": "assistant", "content": response})
    st.session_state.internalmessages.append({"role": "assistant", "content": response})