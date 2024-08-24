import os
from dotenv import load_dotenv
load_dotenv()
groq_api_key = os.getenv('GROQ_API_KEY')
from langchain_groq import ChatGroq
llm = ChatGroq(model="gemma2-9b-it", groq_api_key = groq_api_key)
from langchain_core.prompts import PromptTemplate
import validators
import streamlit as st
from langchain_community.document_loaders import YoutubeLoader, UnstructuredURLLoader,WebBaseLoader
from langchain.chains.summarize import load_summarize_chain

prompt_template="""
Provide a summary of the following content and only show the important point:
Content:{text}

"""
prompt=PromptTemplate(template=prompt_template,input_variables=["text"])

## sstreamlit APP
st.set_page_config(page_title="LangChain: Summarize Text From YT or Website", page_icon="🦜")
st.title("🦜 LangChain: Summarize Text From YT or Website")
st.subheader('Summarize URL')

generic_url = st.text_input("URL", label_visibility= "collapsed")

if st.button("Summarize the content from YT or website"):
    # Validate all the inputs
    if not generic_url.strip():
        st.error("Please enter a URL")
    elif not validators.url(generic_url):
        st.error("Please enter a valid ypu tube or any website url")
    else:
        try:
            with st.spinner("Waiting..."):
            # Load the content from the URL
                if "youtube.com" in generic_url:
                    loader = YoutubeLoader.from_youtube_url(generic_url,add_video_info = True)
                else:
                    # loader = UnstructuredURLLoader(urls=[generic_url], ssl_verify = False,
                    #                                headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"})
                    loader = WebBaseLoader(generic_url)
                data = loader.load()

                ## Chain for summarization

                chain = load_summarize_chain(
                    llm=llm,
                    prompt=prompt,
                    chain_type= "stuff"
                )
                output_summary = chain.run(data)
                print(output_summary)
                st.subheader("Summary : ")
                st.success(output_summary)
        except Exception as e:
            st.exception(f"Exception : {e}")


