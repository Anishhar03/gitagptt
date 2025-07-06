import chromadb
from chromadb.utils import embedding_functions
from PyPDF2 import PdfReader

# Load and clean text
reader = PdfReader("gita_book.pdf")
full_text = " ".join([p.extract_text() for p in reader.pages if p.extract_text()])

# Split into passages (customize this splitting if needed)
gita_chunks = [chunk.strip() for chunk in full_text.split("\n\n") if len(chunk.strip()) > 50]

# Embedding function
embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

# Initialize Chroma client
client = chromadb.Client()
collection = client.create_collection(name="gita", embedding_function=embedding_func)

# Add to collection
for idx, chunk in enumerate(gita_chunks):
    collection.add(documents=[chunk], ids=[str(idx)])

print(f"✅ Vector DB created with {len(gita_chunks)} chunks.")
