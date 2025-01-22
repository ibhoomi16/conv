import streamlit as st
from pymongo import MongoClient
import json

# Predefined MongoDB Configuration
MONGO_DB_URL = "mongodb+srv://bhoomi16@cluster0.5vcgj.mongodb.net/?retryWrites=true&w=majority"
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
st.header("Enter Metadata for Job")
job_id = st.text_input("Job ID (used for fetching MongoDB data)", "")
title = st.text_input("Guide Title", "Distal Radius Fracture Rehabilitation")
stage = st.text_input("Stage", "Rehabilitation")
disease = st.text_input("Disease Title", "Fracture")
specialty = st.text_input("Specialty", "orthopedics")

# Process the data when the button is clicked
if st.button("Process Data"):
    if all([job_id, title, stage, disease, specialty]):
        try:
            # Connect to MongoDB and fetch data
            st.info("Connecting to MongoDB...")
            collection = connect_to_mongo(MONGO_DB_URL, DB_NAME, COLLECTION_NAME)

            st.info("Fetching recommendations from MongoDB...")
            fetched_data = fetch_recommendations_from_mongo(collection, job_id)

            if fetched_data:
                st.success(f"Fetched {len(fetched_data)} recommendations from the database.")

                # Display the fetched data
                st.subheader("Fetched Data:")
                st.json(fetched_data)

                # Option to download JSON file
                json_output = json.dumps(fetched_data, indent=2)
                st.download_button(
                    label="Download JSON",
                    data=json_output,
                    file_name="output.json",
                    mime="application/json"
                )
            else:
                st.warning("No recommendations found for the provided Job ID in the database.")
        except Exception as e:
            st.error(f"Error processing data: {e}")
    else:
        st.warning("Please fill in all required fields.")
