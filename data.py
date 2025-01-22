import streamlit as st
from pymongo import MongoClient
import json

# Predefined MongoDB Configuration
MONGO_DB_URL = "mongodb+srv://<bhoomi16>@cluster0.5vcgj.mongodb.net/?retryWrites=true&w=majority"
DB_NAME = "document"
COLLECTION_NAME = "data"

# Function to connect to MongoDB
def connect_to_mongo(db_url, db_name, collection_name):
    """
    Connect to MongoDB and return the collection.
    """
    try:
        client = MongoClient(db_url)
        db = client[db_name]
        return db[collection_name]
    except Exception as e:
        raise Exception(f"Error connecting to MongoDB: {e}")

# Function to fetch recommendations from MongoDB based on job ID
def fetch_recommendations_from_mongo(collection, job_id):
    """
    Fetch recommendations and related data from MongoDB collection using the provided job ID.
    """
    try:
        documents = collection.find({"job_id": job_id})
        recommendations = []
        for document in documents:
            recommendations.append({
                "source": document.get("source", ""),
                "type": document.get("type", ""),
                "page": document.get("page", ""),
                "category": document.get("category", ""),
                "index": document.get("index", ""),
                "content": document.get("content", "").strip()
            })
        return recommendations
    except Exception as e:
        raise Exception(f"Error fetching recommendations: {e}")

# Streamlit app
st.title("Recommendations Fetcher with MongoDB Integration")

# Input for job ID
job_id = st.text_input("Job ID (used for fetching MongoDB data)", "")

# Input for metadata fields
st.header("Metadata Fields")
title = st.text_input("Guide Title", "Distal Radius Fracture Rehabilitation")
stage = st.text_input("Stage", "Rehabilitation")
disease = st.text_input("Disease Title", "Fracture")
specialty = st.text_input("Specialty", "Orthopedics")

# Process the data when the button is clicked
if st.button("Fetch Recommendations"):
    if job_id:
        try:
            # Connect to MongoDB and fetch data
            st.info("Connecting to MongoDB...")
            collection = connect_to_mongo(MONGO_DB_URL, DB_NAME, COLLECTION_NAME)

            st.info("Fetching recommendations from MongoDB...")
            fetched_data = fetch_recommendations_from_mongo(collection, job_id)

            if fetched_data:
                st.success(f"Fetched {len(fetched_data)} recommendations from the database.")

                # Add metadata to the results
                metadata = {
                    "job_id": job_id,
                    "title": title,
                    "stage": stage,
                    "disease": disease,
                    "specialty": specialty,
                    "recommendations": fetched_data
                }

                # Display the combined metadata and fetched data
                st.subheader("Fetched Data with Metadata:")
                st.json(metadata)

                # Option to download JSON file
                json_output = json.dumps(metadata, indent=2)
                st.download_button(
                    label="Download JSON",
                    data=json_output,
                    file_name="output_with_metadata.json",
                    mime="application/json"
                )
            else:
                st.warning("No recommendations found for the provided Job ID in the database.")
        except Exception as e:
            st.error(f"Error processing data: {e}")
    else:
        st.warning("Please enter a valid Job ID.")
