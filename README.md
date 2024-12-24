# INFOLOOP: Dynamic Knowledge Base System

## overview 

This project implements a dynamic knowledge base system that fetches, processes, and stores information from external sources (such as RSS feeds) into a searchable vector database. The system is designed to periodically update its knowledge base and allow users to query the most relevant results via a Streamlit interface.

## Features

1. Dynamic Knowledge Updates:

    - Periodically fetches new content from predefined sources.
    
    - Parses and cleans RSS feed data to extract meaningful text without HTML tags.

2. Vector-Based Search:

    - Encodes content into high-dimensional vector representations using the SentenceTransformer model.
    
    - Stores these vectors in a FAISS index for efficient similarity search.

3. User-Friendly Interface:

    - Interactive query system built using Streamlit.
    
    - Displays search results with relevance scores.

4. Scalable and Persistent:

    - FAISS index and metadata are persisted to disk for reuse across sessions.
    
    - Scheduled updates ensure the knowledge base remains current.

## Technologies Used

- requests: For fetching RSS feed content.

- BeautifulSoup: For parsing and cleaning HTML content.

- sentence-transformers: For embedding text into vector representations.

- faiss: For efficient similarity-based search.

- apscheduler: For scheduling periodic updates.

- streamlit: For creating an interactive web-based user interface.

## Installation

<!--start code-->

#### Install dependencies:

    pip install -r requirements.txt
    
<!--end code-->

<!--start code-->

#### Run the Streamlit app:

    streamlit run app.py
    
<!--end code-->

## How It Works

1. Data Fetching:

    - The system fetches data from predefined RSS feeds.
    
    - It parses the feed to extract titles and descriptions, ensuring all HTML tags are stripped for clean text.

2. Data Processing:

    - Extracted text is encoded into vector embeddings using a pre-trained SentenceTransformer model.
    
    - Embeddings are added to a FAISS index for fast similarity search.

3. Knowledge Base Updates:

    - The apscheduler library periodically triggers updates to fetch and process new data.
    
    - The FAISS index and metadata are saved to disk to ensure persistence across sessions.

4. Query System:

    - Users input a query in the Streamlit interface.
    
    - The query is encoded and compared against the FAISS index to retrieve the most relevant entries.
    
    - Results are displayed with relevance scores.

## Usage

### Query the Knowledge Base

1. Open the Streamlit app.

2. Enter a query in the input field and click "Search".

3. View the top results with relevance scores.

### Update the Knowledge Base

1. Updates are performed automatically every hour.

2. Use the "Update Now" button in the Streamlit sidebar to manually trigger updates.
