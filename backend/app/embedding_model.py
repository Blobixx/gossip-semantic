from sentence_transformers import SentenceTransformer

# all-MiniLM-L6-v2 model is good compromise between model size and speed
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
