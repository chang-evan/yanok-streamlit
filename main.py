import langchain_helper as lch
import streamlit as st



response = lch.generate_pet_name()

st.title("Yanok.AI - Your Best Next Future")
text = st.header(response)
st.text("")
st.text("")


q = st.text_input("Ask us a question:", "What is Yanok.AI?")
x = lch.ask_question(q)
st.subheader(x)