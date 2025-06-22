from langchain.document_loaders import PyMuPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
import os
import streamlit as st
from dotenv import load_dotenv
load_dotenv()

# Load PDF documents from ./docs directory
def load_documents():
    docs = []
    for filename in os.listdir("./docs"):
        if filename.endswith(".pdf"):
            loader = PyMuPDFLoader(f"./docs/{filename}")
            docs.extend(loader.load())
    return docs

# Create vector store from documents
def build_vector_store(docs):
    embedding = OpenAIEmbeddings()
    db = Chroma.from_documents(docs, embedding)
    return db

# Create QA chain
def create_qa_chain(vector_store):
    retriever = vector_store.as_retriever()
    llm = ChatOpenAI(model="gpt-4")
    qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    return qa

# Ask a question
def ask_dcc(question, qa):
    return qa.run(question)

# Streamlit interface
def main():
    st.title("📄 California DCC AI Compliance Assistant")
    st.write("Ask regulatory questions based on Department of Cannabis Control (DCC) documentation.")

    st.info("Loading and indexing documents... this may take a few seconds on first load.")
    docs = load_documents()
    vector_store = build_vector_store(docs)
    qa = create_qa_chain(vector_store)

    question = st.text_input("Enter your question:")
    if question:
        answer = ask_dcc(question, qa)
        st.markdown("### 🧠 Answer")
        st.write(answer)

if __name__ == "__main__":
    main()
