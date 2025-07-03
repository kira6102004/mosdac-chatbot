# chatbot_backend.py
from pathlib import Path
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.chat_models import ChatOllama
from langchain.chains import RetrievalQA
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate

# Load documents with safer relative path handling
BASE_DIR = Path(__file__).resolve().parent
loader = TextLoader(str(BASE_DIR / "data.txt"), encoding="utf-8")
raw_documents = loader.load()

# Split into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
documents = text_splitter.split_documents(raw_documents)

# Embedding model
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = FAISS.from_documents(documents, embedding_model)
vectorstore.save_local(str(BASE_DIR / "mosdac_vector_index"))
retriever = vectorstore.as_retriever()

# Language model setup
llm = ChatOllama(model="phi3")
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True, output_key="answer")

# Prompt
prompt_template = """
You are a helpful assistant for MOSDAC (Meteorological and Oceanographic Satellite Data Archival Centre).
Answer the question using the context provided below. If you don’t know the answer, say so.

Context:
{context}

Question: {question}
"""
prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

# QA Chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    memory=memory,
    return_source_documents=True,
    chain_type_kwargs={"prompt": prompt},
    output_key="answer"
)

# Function for chatbot

def ask_mosdac_bot(query):
    result = qa_chain.invoke({"query": query})

    # Extract grounded answer and documents
    answer = result.get("answer", "").strip()
    source_docs = result.get("source_documents", [])

    sources = []
    for doc in source_docs:
        metadata = doc.metadata
        source_url = metadata.get("source") or metadata.get("url")
        if source_url and source_url not in sources:
            sources.append(source_url)

    # Determine if speculative insight is needed
    speculative = ""
    if not answer or "I do not have enough data" in answer or "not contain information" in answer:
        speculative = f"It seems the exact details aren't present in the current documents. Based on typical uses of satellites like SCATSAT, it likely serves atmospheric or oceanographic observation purposes."

    return answer, sources, speculative
