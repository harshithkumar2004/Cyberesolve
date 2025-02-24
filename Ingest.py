import os
from google.colab import drive
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS

# Step 1: Mount Google Drive
try:
    drive.mount("/content/drive", force_remount=True)
    print("Google Drive mounted successfully.")
except Exception as e:
    print(f"Error mounting Google Drive: {str(e)}")

# Step 2: Define Directory Path for PDFs
drive_directory = "/content/drive/MyDrive/data"  # Path to the folder containing PDF files

# Ensure the directory exists
if not os.path.exists(drive_directory):
    os.makedirs(drive_directory)
    print(f"Created directory: {drive_directory}")

# Step 3: Load Documents from the Directory (e.g., PDFs)
try:
    loader = DirectoryLoader(drive_directory, glob="*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()
    if documents:
        print(f"Loaded {len(documents)} documents from {drive_directory}.")
    else:
        print(f"No PDF documents found in the directory: {drive_directory}.")
except Exception as e:
    print(f"Error loading documents: {str(e)}")
    documents = []

# Step 4: Split Documents into Chunks for Efficient Embedding Generation
try:
    if documents:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=200)
        texts = text_splitter.split_documents(documents)
        print(f"Split into {len(texts)} text chunks.")
    else:
        texts = []
        print("No documents available to split into chunks.")
except Exception as e:
    print(f"Error splitting documents: {str(e)}")
    texts = []

# Step 5: Generate Embeddings using HuggingFaceEmbeddings
try:
    embeddings = HuggingFaceEmbeddings(
        model_name="nomic-ai/nomic-embed-text-v1",
        model_kwargs={"trust_remote_code": True, "revision": "289f532e14dbbbd5a04753fa58739e9ba766f3c7"}
    )
    print("Embeddings initialized successfully.")
except Exception as e:
    embeddings = None
    print(f"Error initializing embeddings: {str(e)}")

# Step 6: Create FAISS Vector Store from Documents and Embeddings
faiss_db = None
try:
    if embeddings and texts:
        faiss_db = FAISS.from_documents(texts, embeddings)
        print(f"FAISS vector store created with {len(faiss_db.index)} items.")
    else:
        print("Failed to create FAISS vector store: embeddings or texts are empty.")
except Exception as e:
    print(f"Error creating FAISS vector store: {str(e)}")

# Step 7: Define the Path to Save the FAISS Database
faiss_db_path = "/content/drive/MyDrive/ipc_vector_db"  # Change to your desired path

# Ensure the directory for FAISS database exists
try:
    if not os.path.exists(faiss_db_path):
        os.makedirs(faiss_db_path)
        print(f"Directory '{faiss_db_path}' created for FAISS database.")
except Exception as e:
    print(f"Error creating directory for FAISS database: {str(e)}")

# Step 8: Save the FAISS Database Locally
try:
    if faiss_db:
        faiss_db.save_local(faiss_db_path)
        print(f"FAISS database saved at '{faiss_db_path}'")
    else:
        print("No FAISS database to save.")
except Exception as e:
    print(f"Error saving FAISS database: {str(e)}")
