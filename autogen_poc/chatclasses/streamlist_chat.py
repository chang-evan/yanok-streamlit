import streamlit as st
from openai import OpenAI
import os

class StreamlitAppBase:
    def __init__(self, systemprompt="You are a helpful Chatbot", systemprompt2=None):
        os.getenv("OPENAI_API_KEY")
        self.client = OpenAI()
        self.messages = []
        if "systemprompt" not in st.session_state:
            st.session_state.systemprompt = systemprompt
        if systemprompt2:
            if "systemprompt" not in st.session_state:
                st.session_state.systemprompt2 = systemprompt2
            
        self.initialize_streamlit()



    def initialize_streamlit(self):
        # Define session state variables
        if "record" not in st.session_state:
            st.session_state.record = []

        if "openai_model" not in st.session_state:
            st.session_state.openai_model = "gpt-4-turbo-preview"

        if "internal" not in st.session_state:
            st.session_state.internal = []
    

    def openai_chat(self, chathistory, bool_stream):
        # Implement openai_chat functionality
        messages = [
            {"role": message["role"], "content": message["content"]}
            for message in chathistory
        ]

        if bool_stream:
            response = self.client.chat.completions.create(
                model=st.session_state.openai_model,
                messages=messages,
                stream=bool_stream,
            )
        else:
            response = self.client.chat.completions.create(
                model=st.session_state.openai_model,
                messages=messages,
                stream=bool_stream,
            ).choices[0].message.content

        return response

    def update_message(self, chathistory, role, response):
        chathistory.append({"role": role, "content": response})
        

    def run(self):

        st.subheader("Yanok.ai")
        st.markdown(':rainbow[_Powered by GPT-4._]')

        for message in st.session_state.record:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if user_prompt:= st.chat_input("What is up?"):

            with st.chat_message("user"):
                st.markdown(user_prompt)

                self.update_message(st.session_state.internal, "system", st.session_state.systemprompt)
                self.update_message(st.session_state.internal, "user", user_prompt)
                self.update_message(st.session_state.record, "user", user_prompt)

            with st.chat_message("assistant"):
                stream = self.openai_chat(st.session_state.internal, True)
                response = st.write_stream(stream)

            self.update_message(st.session_state.internal, "assistant", response)
            self.update_message(st.session_state.record, "assistant", response)
            self.messages = st.session_state.record[-1]

if __name__ == "__main__":
    app = StreamlitAppBase()
    app.run()