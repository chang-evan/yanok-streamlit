from openai import OpenAI
import streamlit as st
import os


def getupdatedprompt(prompt: str, robomessages: list):
    robomessages.append({"role": "user", "content": prompt})
    adjustmentsprompt = robo2robo(robomessages)
    prompt = prompt + adjustmentsprompt + ". Summarize areas the student can improve and move on to the next exercise. Keep the exercises fun and light to maximize engagement."
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
    st.session_state.robomessages = []






with st.sidebar:
    st.header('Language Options')
    st.session_state.option = st.selectbox('Choose an option:', ["Ukrainian",'Chinese', 'Malay', 'French'], on_change=resetchat)
    option = st.session_state.option
    st.write(f"Classroom is operating in {option}")


if "internalmessages" not in st.session_state:
    st.session_state.internalmessages = []

teacherprompt = f"""You are a language teacher for {option}, helpful and accomodating for the student's needs. You only engage with language learning topics. 
You take input from an advisor who helps analyze the student's weaknesses. Kick off by asking the student for a baseline skill level. Then provide a few options for exercises in this session, including short reading exercises (e.g. paragraphs of text) or writing exercises (i.e. Short writing prompts) with edits and advice as needed - let the student choose but then quickly start the exercise."""

st.session_state.internalmessages.append({"role": "system", "content": teacherprompt})

#robomessages.append({"role": "system", "content": roboprompt})
if "robomessages" not in st.session_state:
    st.session_state.robomessages = []

roboprompt = """You analyze learning outcomes based on inputs from the student. The teacher will provide you with student inputs,
 and you maintain a list of vocabulary the student has not demonstrated fluency with, and share this back to the teacher as a structured list,
 with the instruction 'These are the terms the student may need to focus on:'."""

robomessages = st.session_state.robomessages
robomessages.append({"role": "system", "content": roboprompt })






os.getenv("OPENAI_API_KEY")

client = OpenAI()

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4-turbo-preview"

if "record" not in st.session_state:
    st.session_state.record = []

option = st.session_state.option
st.session_state.internalmessages.append({"role": "system", "content": teacherprompt})




st.subheader("Yanok Language Training")
st.markdown(':rainbow[_Powered by GPT-4. Get ready to learn!_]')










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