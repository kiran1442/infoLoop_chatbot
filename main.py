import requests
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from apscheduler.schedulers.background import BackgroundScheduler
import os
import pickle

# Initialize model and FAISS index
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
dimension = 384
index = faiss.IndexFlatL2(dimension)
metadata = []

# Load existing index and metadata if available
if os.path.exists("faiss_index.bin") and os.path.exists("metadata.pkl"):
    index = faiss.read_index("faiss_index.bin")
    with open("metadata.pkl", "rb") as f:
        metadata = pickle.load(f)

def fetch_data_from_sources():
    """
    Fetch data from predefined sources (e.g., RSS feeds or websites).
    """
    sources = [
        "http://feeds.feedburner.com/TechCrunch/"  # Replace with actual RSS feed
          
    ]
    new_data = []
    for source in sources:
        try:
            response = requests.get(source)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Parse RSS feeds
            for item in soup.find_all("item"):
                title = item.find("title")
                description = item.find("description")
                
                # Extract and clean content
                title_text = title.text.strip() if title else "No Title"
                if description:
                    # Remove nested HTML tags in the description
                    description_soup = BeautifulSoup(description.text, "html.parser")
                    description_text = description_soup.get_text(strip=True)
                else:
                    description_text = "No Description"
                
                new_data.append(f"{title_text}: {description_text}")
        except Exception as e:
            print(f"Error fetching from {source}: {e}")
    return new_data

def process_and_store_data(data):
    """
    Process new data and store embeddings in the FAISS index.
    """
    global metadata
    new_embeddings = []
    new_metadata = []

    for item in data:
        if item not in metadata:
            embedding = embedding_model.encode(item, convert_to_numpy=True)
            new_embeddings.append(embedding)
            new_metadata.append(item)
    
    if new_embeddings:
        new_embeddings = np.array(new_embeddings)
        index.add(new_embeddings)
        metadata.extend(new_metadata)
        
        # Save updates to disk
        faiss.write_index(index, "faiss_index.bin")
        with open("metadata.pkl", "wb") as f:
            pickle.dump(metadata, f)
        print(f"Added {len(new_embeddings)} new items to the database.")

def query_knowledge_base(query, top_k=5):
    """
    Search the FAISS database for the most relevant entries to a query.
    """
    query_embedding = embedding_model.encode(query, convert_to_numpy=True).reshape(1, -1)
    distances, indices = index.search(query_embedding, top_k)
    results = [(metadata[i], distances[0][idx]) for idx, i in enumerate(indices[0]) if i < len(metadata)]
    return results

# Periodic updater
def update_knowledge_base():
    """
    Fetch and update the knowledge base.
    """
    print("Updating knowledge base...")
    new_data = fetch_data_from_sources()
    process_and_store_data(new_data)

# Schedule periodic updates
scheduler = BackgroundScheduler()
scheduler.add_job(update_knowledge_base, "interval", hours=1)
scheduler.start()

# Initial population
update_knowledge_base()
