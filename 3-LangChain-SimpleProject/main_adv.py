from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

# Load OpenAI Key
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Step 1: Load your document
pdf_path = "hr-bot-doc.pdf"
loader = PyPDFLoader(pdf_path)
pages = loader.load()  # Returns a list of LangChain Document objects

# Step 2: Split the pages into smaller overlapping chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,       # Each chunk will be approx 500 characters
    chunk_overlap=50      # Overlap of 50 characters between chunks
)
chunks = splitter.split_documents(pages)

# Step 3: Convert text chunks into embeddings (vector format)
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

# Step 4: Store those embeddings in FAISS for similarity search
vectorstore = FAISS.from_documents(chunks, embeddings)

# Step 5: Setup retriever to fetch similar chunks to the query
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})  # top 5 similar chunks

# Step 6: Add memory to remember previous Q&A turns
memory = ConversationBufferMemory(
    memory_key="chat_history",  # Variable name used in the chain
    return_messages=True        # Return full messages, not just strings
)

# Step 7: Use ConversationalRetrievalChain which supports memory
qa_chain = ConversationalRetrievalChain.from_llm(
    llm=ChatOpenAI(openai_api_key=openai_api_key, temperature=0, model="gpt-4"),
    retriever=retriever,
    memory=memory,
    return_source_documents=False  # Optional: set True if you want to see source chunks
)

# Step 8: Start asking questions in loop
print("📄 Ask questions about your PDF (type 'exit' to quit):")
chat_history = []  # Needed for tracking multi-turn conversation

while True:
    query = input("\nYou: ")
    if query.lower() in ["exit", "quit"]:
        print("👋 Exiting.")
        break

    result = qa_chain({"question": query, "chat_history": chat_history})
    print("🤖 Answer:", result['answer'])

    # Store conversation for context (LangChain handles this internally too)
    chat_history.append((query, result['answer']))
