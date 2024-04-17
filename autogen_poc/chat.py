from openai import OpenAI
import streamlit as st
import os


def getupdatedprompt(prompt: str, robomessages: list):
    robomessages.append({"role": "user", "content": prompt})
    adjustmentsprompt = robo2robo(robomessages)
    prompt = prompt + "Here is the vocabulary the student has not demonstrated fluency with: " + adjustmentsprompt
    return prompt


def robo2robo(robomessages: list):
    roboprompt = client.chat.completions.create(
    model=st.session_state["openai_model"],
    messages=[
        {"role": m["role"], "content": m["content"]}
        for m in robomessages
    ],
    stream=False,
)
    return roboprompt.choices[0].message.content

def resetchat():
    st.session_state.record = []
    st.session_state.internalmessages = []
    st.session_state.internalmessages.append({"role": "system", "content": f"You are a language teacher for {option}. Giving instructions in English, please print the top 3 nouns and verbs in {option} only and ask the user to translate. Do not provide the English translations. Based on the user's performance, switch to {option} if the user translates over 9/10 correctly."})
    robomessages = []
    robomessages.append({"role": "system", "content": "You analyze learning outcomes based on inputs from the student. The teacher will provide you with student inputs, and you maintain a list of vocabulary the student has not demonstrated fluency with, and share this back to the teacher as a structured list, with the instruction 'These are the terms the student may need to focus on:'."})



os.getenv("OPENAI_API_KEY")

st.subheader("Yanok Language Training")
st.markdown(':rainbow[_Powered by GPT-4. Get ready to learn!_]')

with st.sidebar:
    st.header('Language Options')
    st.session_state.option = st.selectbox('Choose an option:', ["Ukrainian",'Chinese', 'Malay', 'French'], on_change=resetchat)
    option = st.session_state.option
    st.write(f"Classroom is operating in {option}")
    resetchat()


client = OpenAI()

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4-turbo-preview"

if "record" not in st.session_state:
    st.session_state.record = []
    st.session_state.internalmessages = []
    option = st.session_state.option
    st.session_state.internalmessages.append({"role": "system", "content": f"You are a language teacher for {option}. Giving instructions in English, please print the top 3 nouns and verbs in {option} only and (in English) ask the user to translate. Based on the user's performance, switch to {option} if the user translates over 9/10 correctly."})

robomessages = []
robomessages.append({"role": "system", "content": "You analyze learning outcomes based on inputs from the student. The teacher will provide you with student inputs, and you maintain a list of vocabulary the student has not demonstrated fluency with, and share this back to the teacher as a structured list, with the instruction 'These are the terms the student may need to focus on:'."})


for message in st.session_state.record:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.record.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    revisedprompt = getupdatedprompt(prompt, robomessages)    
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