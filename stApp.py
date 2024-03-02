from gemma_instruct import llm as gemma
from openai_chatgpt import chatgpt
import os
from generateVectorDB import get_collection, process_pdf
from retriever import get_documents_by_query
import streamlit as st

upload_dir = "./DB/"

collection = get_collection()

sidebar = st.sidebar
with sidebar.form(key='file-handler', clear_on_submit=True):
    uploaded_file = st.file_uploader(label="Upload your doc", type="pdf",
                                     accept_multiple_files=False, key="pdf_upload")
    submitted = st.form_submit_button("Upload")
    if uploaded_file and submitted:
        file_name = os.sep.join([upload_dir, uploaded_file.name])
        with open(file_name, "wb") as f:
            f.write(uploaded_file.getbuffer())
        process_pdf(file_name, collection)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["message"])

bot_choice = st.radio(
    "Which bot would you like to use?",
    [":zany_face: LocalGPT", ":sunglasses: ChatGPT"],
    captions=["gemma", "chatGPT"])

if query := st.chat_input("Ask a question!"):
    with st.chat_message("user"):
        st.markdown(query)
        st.session_state.messages.append({"role": "user",
                                          "message": query})
    with st.chat_message("assistant"):
        with st.spinner("Bot thinking ..."):
            if bot_choice == ":zany_face: LocalGPT":
                alternate_search_query = gemma(f"Rewrite the following question encase in backticks, "
                                               f"adding more context, for retrieving information.\n`{query}`")
                context_docs = '\n===========\n'.join(get_documents_by_query(alternate_search_query, collection))
                print(context_docs)
                bot_response = gemma(f"Given the following pages, answer the question to the best of your "
                                     f"ability.\n\nPages:\n{context_docs}\n\nQuestion: {query}")

            else:
                alternate_search_query = chatgpt(f"Rewrite the following question encase in backticks, "
                                                 f"adding more context, for retrieving information.\n`{query}`")
                context_docs = '\n===========\n'.join(get_documents_by_query(alternate_search_query, collection))
                print(context_docs)
                bot_response = chatgpt(f"Given the following pages, answer the question to the best of your "
                                       f"ability.\n\nPages:\n{context_docs}\n\nQuestion: {query}")

        # bot_response = f"{bot}: {query}"
        # bot_response = chatbot_response(query)
        st.markdown(bot_response)
        st.session_state.messages.append({"role": "assistant",
                                          "message": bot_response})
