from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import create_retrieval_chain, create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage

import streamlit as st
from dotenv import load_dotenv
load_dotenv()

def build_chat_history(chat_history_list):
    # this function takes in the chat history messages in a list of tuples format
    # and turns it into a series of human and AI messages objects
    chat_history = []
    for message in chat_history_list:
        chat_history.append(HumanMessage(content=message[0]))
        chat_history.append(AIMessage(content=message[1]))
    return chat_history


def query(question, chat_history):
    """
    this function does the following:
    1. receives two parameters - 'question' - a string and 'chat_history' - a Python list of tuples contain accumulating questions-answer pairs
    2. load the local FAISS database where the entire website is stored as embedding vectors
    3. create a conversationalBufferMemory object with 'chat_history'
    4. create a conversationalRetrievalChain object with FAISS DB as the retriever (LLM lets us create Retriever object against data stores)
    5. invoke the retriever object with the query and chat history
    6. return the response 
    """

    chat_history = build_chat_history(chat_history)
    embeddings = OpenAIEmbeddings()
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    llm = ChatOpenAI(model="gpt-4o", temperature=0.0)

    condense_question_system_template = (
        "Given a chat history and latest user question "
        "which might reference context in the chat history,"
        "formulate a standalone question which can be understood "
        "without the chat history. DO NOT answer the question, "
        "just reformulate it if needed and otherwise return it as is."
    )

    condense_question_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", condense_question_system_template),
            ("placeholder", "{chat_history}"),
            ("human", "{input}"),
        ]
    )

    history_aware_retriever = create_history_aware_retriever(
        llm,new_db.as_retriever(),condense_question_prompt
    )

    system_prompt = (
        "You are a helpful assistant that answers questions about HR policies. "
        "You answer based on the information provided in the chat history and "
        "the retrieved documents. If you don't know the answer, say so."
        "don't know. Use three sentences maximum and keep the answer concise."
        "\n\n"
        "{context}"
    )

    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("placeholder", "{chat_history}"),
            ("human", "{input}"),
        ]
    )

    qa_chain = create_stuff_documents_chain(
        llm=llm,
        prompt=qa_prompt
    )
    convo_qa_chain = create_retrieval_chain(
        retriever=history_aware_retriever,
        combine_docs_chain=qa_chain
    )

    return convo_qa_chain.invoke(
        {
            "input": question,
            "chat_history": chat_history
        }
    )

def show_ui():
    """
    this function does the following:
    1. creates a Streamlit UI with a text input for the question and a button to submit the question
    2. displays the chat history and the response from the query function
    """
    
    st.title("HR ChatBot")
    st.image("src/img/hr-logo.jpeg", width=200)
    st.subheader("Ask your HR related questions")

    # initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.chat_history = []

    # Display chat messages from history on app return 
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt :=st.chat_input("Enter your HR policy related query: "):
        # invoke the function with the retriever with the chat history and display in chat container in query
        with st.spinner("Working in your query... "):
            response = query(question=prompt,chat_history=st.session_state.chat_history)
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                st.markdown(response["answer"])

            #  Append user messages to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.messages.append({"role": "assistant", "content": response["answer"]})
            st.session_state.chat_history.extend([(prompt, response["answer"])])


if __name__ == "__main__":
    show_ui()