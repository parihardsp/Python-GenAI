# rag_pipeline.py

# ============ IMPORTS ============
import os
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# ============ LOAD ENV VARIABLES ============
# Load API key from .env file
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY in your .env file.")

# ============ STEP 1: LOAD PDF ============
pdf_path = "hr-bot-doc.pdf"  # Replace with your actual file path

# Load PDF and extract text from each page
loader = PyPDFLoader(pdf_path)
documents = loader.load()
print(f"[INFO] Loaded {len(documents)} pages from '{pdf_path}'.")

# ============ STEP 2: SPLIT INTO CHUNKS ============
# Split the long documents into manageable chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,       # Max characters per chunk
    chunk_overlap=50      # Overlap to preserve context
)
chunks = splitter.split_documents(documents)
print(f"[INFO] Split into {len(chunks)} text chunks.")

# ============ STEP 3: EMBEDDINGS + VECTORSTORE ============
# Convert chunks into embeddings using OpenAI
embedding_model = OpenAIEmbeddings(api_key=openai_api_key)

# Store vectors in Chroma (in-memory)
vectorstore = Chroma.from_documents(documents=chunks, embedding=embedding_model)
print("[INFO] Vectorstore created using Chroma.")

# ============ STEP 4: RETRIEVER SETUP ============
# Create a retriever for semantic similarity search
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 4})

# ============ STEP 5: USER QUERY ============
# Define your user question
question = "What are the key highlights from the report?"
print(f"[INFO] Query: {question}")

# Retrieve the most relevant document chunks
relevant_docs = retriever.get_relevant_documents(query=question)
print(f"[INFO] Retrieved {len(relevant_docs)} relevant chunks.")
print(relevant_docs)

# Combine the text from all retrieved documents
context_text = "\n\n".join([doc.page_content for doc in relevant_docs])

# ============ STEP 6: SUMMARIZATION ============
# Initialize the LLM (GPT-4 preferred)
llm = ChatOpenAI(
    model="gpt-4", 
    temperature=0, 
    api_key=openai_api_key
    )

# Create a prompt template for summarization
prompt_template = PromptTemplate(
    input_variables=["context"],
    template="""
You are a professional report summarizer.

Given the following extracted text from a report, summarize the key 3 highlights in concise bullet points:

{context}
"""
)

# Chain the LLM with the prompt
summary_chain = prompt_template | llm

# Run the chain to get a summary
summary = summary_chain.invoke({"context": context_text})

# ============ OUTPUT ============
print("\n========== ✅ FINAL SUMMARY ==========\n")
print(summary)
