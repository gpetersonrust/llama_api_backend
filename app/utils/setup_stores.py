def setup_environment():
    import os

    # Create necessary directories for vector stores
    os.makedirs("Stores/faiss_index", exist_ok=True)

    print("✅ Environment ready – vector store folders created.")
