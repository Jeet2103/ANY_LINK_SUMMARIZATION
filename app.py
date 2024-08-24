import os
from dotenv import load_dotenv
load_dotenv()
groq_api_key = os.getenv('GROQ_API_KEY')
from langchain_groq import ChatGroq
llm = ChatGroq(model="gemma2-9b-it", groq_api_key = groq_api_key)
response = llm.invoke("Hello My name is Jeet Nandigrami")
print(response.content)