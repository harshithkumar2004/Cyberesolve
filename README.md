# CyberResolve - AI-Powered Legal Assistant

CyberResolve is an AI-driven legal assistant that helps users query and retrieve legal information efficiently. The application leverages **Mistral API** for generating responses and employs **FAISS** for vector-based document search on the IPC Law dataset (ipc\_law\.pdf).

## Features

- AI-Powered Legal Chatbot: Uses Mistral API to process and answer legal queries.
- Document Embedding & Retrieval: FAISS-based search on IPC Law dataset for relevant legal information.
- Streamlit Interface: A user-friendly chatbot interface.
- Session-based Chat History: Maintains user queries and responses.
- Efficient Text Processing: Uses LangChain for document ingestion and chunking.

## Setup & Installation

### Prerequisites

- Python 3.8+
- Streamlit
- FAISS
- LangChain
- Mistral API key
- HuggingFace Embeddings

### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/your-repo/cyberresolve.git
   cd cyberresolve
   ```

2. Set up your Mistral API key:
   ```sh
   export MISTRAL_API_KEY="your_api_key_here"
   ```

## How It Works

### Ingesting the IPC Law Dataset

1. Place `ipc_law.pdf` in the designated directory.
2. Run `Ingest.py` to process and vectorize the dataset:
   ```sh
   python Ingest.py
   ```
   This script:
   - Mounts Google Drive (for Colab users)
   - Loads and splits IPC Law documents
   - Generates text embeddings using HuggingFace models
   - Stores vectors in a FAISS database

### Running the Legal Chatbot

1. Start the Streamlit app:
   ```sh
   streamlit run app.py
   ```
2. Enter legal questions in the chat interface.
3. The chatbot retrieves context from the FAISS database and generates responses using Mistral API.

##

This project is still in progress 
