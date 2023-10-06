import streamlit as st
from dotenv import load_dotenv
import os
from pypdf import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain, LLMChain
from langchain.llms.google_palm import GooglePalm
from chat_template import css, bot_template, user_template, summarize_template
import google.generativeai as palm

load_dotenv()


def convert_pdf_to_text(pdfdocs):
    txt = ''
    for pdf in pdfdocs:
        reader = PdfReader(pdf)
        for page in reader.pages:
            txt += page.extract_text()
    return txt


def getChunks(rawtxt):
    splitText = CharacterTextSplitter(
        separator='\n',
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = splitText.split_text(rawtxt)
    return chunks


def get_vectors(txt_list):
    # load the value from .env file to get the huggingface api key
    embeddings = HuggingFaceInferenceAPIEmbeddings(
        api_key=os.getenv('HUGGINGFACEHUB_API_TOKEN'),
        model_name="BAAI/bge-large-en-v1.5"
    )
    vector_store = FAISS.from_texts(txt_list, embeddings)
    return vector_store


def getConversation(vector):
    model = 'models/text-bison-001'
    api_key = os.getenv('PALM_API')
    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    llm = GooglePalm(
        google_api_key=api_key,
        model_name=model
    )

    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vector.as_retriever(),
        memory=memory
    )
    return chain


def handle_input(user_q):
    try:
        response = st.session_state.converse({'question': user_q})
        # st.write(response)
        st.session_state.chat_history = response['chat_history']
        for i, message in enumerate(st.session_state.chat_history):
            if i % 2 == 0:
                # with st.chat_message('user'):
                #    st.write(message.content)
                st.write(user_template.replace(
                    '{{MSG}}', message.content), unsafe_allow_html=True)
                # message(message.content, is_user=True)
            else:
                # with st.chat_message('assistant'):
                #    st.write(message.content)
                st.write(bot_template.replace(
                    '{{MSG}}', message.content), unsafe_allow_html=True)
                # message(message.content)
    except TypeError:
        st.toast('Please Upload a Document to chat with it')

# Summarize contents of a document using Langchain


def summarize(file):
    try:
        # get text from pdf
        rawtxt = convert_pdf_to_text(file)
        # get text chunks
        txt_list = getChunks(rawtxt)
        # create vector store
        vector = get_vectors(txt_list)
        chain = getConversation(vector)
        response = chain({'question': 'Simplify the pdf using plain language and easy to understand terms. If available state relevant information such as parties involved, terms of the agreement, and other necessary details.'})
        st.write(summarize_template.replace('{{TXT}}', response['answer']), unsafe_allow_html=True)
    except KeyError:
        st.error(' :warning: Please Upload a Document First :warning:')


def auto_drafter_input(sender, receiver, doc_type, more_info):
    model = 'models/text-bison-001'
    api_key = os.getenv('PALM_API')
    palm.configure(api_key=api_key)
    
    llm = GooglePalm(
        google_api_key=api_key,
        model_name=model
    )
    prompt_template = PromptTemplate.from_template(
        "{doc_type} is the type of Legal Document that must be created, {sender} is the sender of this document who is sending the legal document to someone, {receiver} is the receiver of this document who is the one the document is dedicated to, {more_info} is the additional information that must be included in the resultant legal document. Draft a legal document in plain language and using easy-to-understand terms. Ask for more input to get information to customize the generated legal document based on the specific needs of the user."
    )

    chain = LLMChain(llm=llm, prompt=prompt_template)

    return chain.run(doc_type=doc_type, sender=sender,
                     receiver=receiver, more_info=more_info)
