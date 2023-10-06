import streamlit as st
from parse import *


def main():
    st.set_page_config(page_title='Legal Lens',
                       page_icon='https://i.ibb.co/VQHJR2H/Legal-Lens-modified-modified.png',
                       layout='wide',
                       initial_sidebar_state='auto')
    st.image('https://i.ibb.co/VQHJR2H/Legal-Lens-modified-modified.png', width=200)
    st.title('Legal Lens')
    st.write(css, unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(['Summarize', 'Chat', 'Auto Drafting'])

    with tab2:
        st.subheader('Chat with your Legal document')
        if 'converse' not in st.session_state:
            st.session_state.converse = None

        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = None

        st.write('Upload your Legal Documents and ask questions regarding them')
        st.markdown('---')
        user_q = st.text_input('Ask your question:')
        if user_q:
            handle_input(user_q)    
        

    with st.sidebar:
        st.subheader('Your documents')
        pdfdocs = st.file_uploader('Upload your PDFs', type=[
                                   'pdf'], accept_multiple_files=True)
        if st.button('Process documents'):
            with st.status('Processing your documents...') as status:
                # get pdf text
                st.write('Converting into text...')
                rawtxt = convert_pdf_to_text(pdfdocs)
                # st.write(rawtxt)
                # get text chunks
                st.write('Converting the text into vectors...')
                txt_list = getChunks(rawtxt)
                # create vector store
                st.write('Storing it in vector store...')
                vector = get_vectors(txt_list)
                status.update(label='Documents are processed!! ',
                              state="complete")
            # create conversation chain
            st.session_state.converse = getConversation(vector)
        st.warning('''We intend to give the perfect responses to you. However AI responses can be sometimes misleading.

If you have any doubts ask a lawyer about your queries.''')
        

    with tab1:
        st.subheader('Summarise your Legal document')
        st.write('Summarize your documents using the Langchain')
        st.markdown('---')
        summarize(pdfdocs)

    with tab3:
        st.subheader('Auto Drafting of Legal Documents')

        with st.form("auto_drafter_form"):
            sender = st.text_input('Sender')
            receiver = st.text_input('Receiver')
            doc_type = st.text_input('Type of Legal Document')
            more_info = st.text_area('More Info')

            submit = st.form_submit_button('Submit')

        if submit:
            output= st.container()
            output.markdown(f''' ### Auto Drafted Document
                            {auto_drafter_input(sender, receiver, doc_type, more_info)}''')


if __name__ == "__main__":
    main()
