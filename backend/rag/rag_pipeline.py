import os

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

# Absolute path to the knowledge_base folder (two levels up from this file)
KNOWLEDGE_BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "knowledge_base")
)

# Where the FAISS index is saved on disk (inside backend/rag/)
FAISS_INDEX_PATH = os.path.join(os.path.dirname(__file__), "faiss_index")

# Module-level cache so we only load the index once per server run
_vector_store = None


def _get_embeddings() -> OpenAIEmbeddings:
    """Use OpenAI's hosted embeddings API instead of a local model to keep memory usage low."""
    return OpenAIEmbeddings(
        model="text-embedding-3-small",
        api_key=os.getenv("OPENAI_API_KEY"),
    )


def build_vector_store() -> FAISS:
    """
    Step 1 - Load all .txt files from knowledge_base/
    Step 2 - Split each document into small overlapping chunks
    Step 3 - Generate embeddings for every chunk
    Step 4 - Store embeddings in a FAISS vector store and save to disk
    """
    print("[RAG] Building vector store from knowledge base...")

    # Step 1: Load documents
    loader = DirectoryLoader(
        KNOWLEDGE_BASE_DIR,
        glob="*.txt",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
    )
    documents = loader.load()
    print(f"[RAG] Loaded {len(documents)} documents from {KNOWLEDGE_BASE_DIR}")

    # Step 2: Split into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n---\n", "\n\n", "\n", " "],
    )
    chunks = splitter.split_documents(documents)
    print(f"[RAG] Split into {len(chunks)} chunks")

    # Step 3 + 4: Embed and store in FAISS
    embeddings = _get_embeddings()
    vector_store = FAISS.from_documents(chunks, embeddings)
    vector_store.save_local(FAISS_INDEX_PATH)
    print(f"[RAG] Vector store saved to {FAISS_INDEX_PATH}")

    return vector_store


def load_vector_store() -> FAISS:
    """
    Load the FAISS index from disk if it exists.
    If not found, build it first from the knowledge base documents.
    Uses a module-level cache so the index is only loaded once.
    """
    global _vector_store

    if _vector_store is not None:
        return _vector_store

    embeddings = _get_embeddings()

    if os.path.exists(FAISS_INDEX_PATH):
        print("[RAG] Loading existing FAISS index from disk...")
        _vector_store = FAISS.load_local(
            FAISS_INDEX_PATH,
            embeddings,
            allow_dangerous_deserialization=True,
        )
        print("[RAG] Vector store loaded successfully")
    else:
        _vector_store = build_vector_store()

    return _vector_store


def retrieve_context(query: str, k: int = 3) -> str:
    """
    Step 5 - Receive the user's question
    Step 6 - Search the vector store for the top-k most relevant chunks
    Step 7 - Return the chunks as a single string (context for the LLM)
    """
    try:
        vs = load_vector_store()
        docs = vs.similarity_search(query, k=k)
        if not docs:
            return ""
        return "\n\n".join([doc.page_content for doc in docs])
    except Exception as e:
        print(f"[RAG] Retrieval error: {e}")
        return ""


def rebuild_vector_store() -> FAISS:
    """Force rebuild the vector store (call this when knowledge base files change)."""
    global _vector_store
    _vector_store = None
    return build_vector_store()
