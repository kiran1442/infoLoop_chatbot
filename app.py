import streamlit as st
from main import query_knowledge_base, update_knowledge_base, metadata, index

# Streamlit configuration
st.set_page_config(page_title="Dynamic Knowledge Base", layout="wide")

st.title("Dynamic Knowledge Base System")
st.sidebar.header("Control Panel")

# Query Section
st.subheader("Query the Knowledge Base")
user_query = st.text_input("Enter your query:")

if st.button("Search"):
    if user_query:
        with st.spinner("Searching the knowledge base..."):
            results = query_knowledge_base(user_query)
        st.write("### Results:")
        for result, distance in results:
            st.write(f"- **Result:** {result} (Relevance: {1 - distance:.4f})")
    else:
        st.warning("Please enter a query before searching.")

# Sidebar for updates
st.sidebar.subheader("Knowledge Base Status")
if st.sidebar.button("Update Now"):
    with st.spinner("Updating the knowledge base..."):
        update_knowledge_base()
    st.sidebar.success("Knowledge base updated!")

# Display current status
st.sidebar.write("### Metadata Summary")
st.sidebar.write(f"- **Items in Knowledge Base:** {len(metadata)}")
st.sidebar.write(f"- **FAISS Index Size:** {index.ntotal}")
