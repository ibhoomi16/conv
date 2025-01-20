import streamlit as st
import json
import re

# Function to extract recommendations from Markdown content
def extract_recommendations(md_content):
    pattern = r"\d+\.\s+(.*)"
    matches = re.findall(pattern, md_content)

    recommendations = []
    for match in matches:
        recommendations.append({
            "recommendation_content": match.strip(),
            "recommendation_class": "1",
            "rating": "C-LD"
        })
    
    return recommendations

# Function to generate JSON chunks
def generate_json_chunks(recommendations):
    base_json = {
        "title": "Distal Radius Fracture Rehabilitation",
        "subCategory": [],
        "guide_title": "Distal Radius Fracture Rehabilitation",
        "stage": ["Rehabilitation"],
        "disease": ["Fracture"],
        "rationales": [],
        "references": [],
        "specialty": ["orthopedics"]
    }
    
    json_chunks = []
    for rec in recommendations:
        chunk = base_json.copy()
        chunk.update(rec)
        json_chunks.append(chunk)
    
    return json_chunks

# Streamlit app
st.title("Markdown to JSON Converter")

uploaded_file = st.file_uploader("Upload a Markdown (.md) file", type=["md"])

if uploaded_file is not None:
    # Read the file content
    md_content = uploaded_file.read().decode("utf-8")
    
    # Extract recommendations from the Markdown content
    recommendations = extract_recommendations(md_content)
    
    # Generate JSON chunks
    json_chunks = generate_json_chunks(recommendations)
    
    # Display the JSON chunks
    st.write("Generated JSON:")
    st.json(json_chunks)
    
    # Option to download JSON file
    json_output = json.dumps(json_chunks, indent=2)
    st.download_button(
        label="Download JSON",
        data=json_output,
        file_name="output.json",
        mime="application/json"
    )
