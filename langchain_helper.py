from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from dotenv import load_dotenv



load_dotenv()

def generate_pet_name():
    prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a copy writer for an exciting, young startup"),
    ("user", "{input}")
    ])

    llm = ChatOpenAI(temperature=0, api_key= "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")

    output_parser = StrOutputParser()

    chain = prompt | llm | output_parser

    name = chain.invoke({"input": "Write a brief but warm greeting for the company webpage, company name Yanok.ai. Include a mission statement for the company which is to 'Launch your Best Next Future'"})
               
    return name

def ask_question(question):
    prompt2 = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant"),
    ("user", "{input}")
    ])

    llm = ChatOpenAI(temperature=0)

    output_parser = StrOutputParser()

    chain = prompt2 | llm | output_parser

    name = chain.invoke({"input": question})
               
    return name



if __name__ == "__main__":
    
    response = generate_pet_name()
    print(response)