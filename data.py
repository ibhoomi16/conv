import streamlit as st
import json
import re

# Function to extract recommendations along with lor and cor from Markdown content
def extract_recommendations(md_content):
    # Regex pattern to capture recommendation content, lor, and cor
    pattern = r"(\d+)\.\s+(.*?)\s*lor:\s*(\w+)\s*cor:\s*(\d+)"
    matches = re.findall(pattern, md_content, re.DOTALL)

    recommendations = []
    for match in matches:
        recommendation_number = match[0]
        recommendation_content = match[1].strip()
        lor = match[2].strip()
        cor = match[3].strip()

        recommendations.append({
            "recommendation_content": recommendation_content,
            "lor": lor,
            "cor": cor
        })
    
    return recommendations

# Mapping of LOR to Rating and COR to Recommendation Class
lor_to_rating = {
    "A": "A",
    "B": "B",
    "C": "C",
    "D": "D"
}

cor_to_class = {
    "1": "High Confidence",
    "2": "Moderate Confidence",
    "3": "Low Confidence"
}

# Function to map lor and cor to rating and recommendation class
def map_lor_cor(recommendation):
    lor = recommendation["lor"]
    cor = recommendation["cor"]
    
    # Mapping lor to rating and cor to recommendation_class
    recommendation["rating"] = lor_to_rating.get(lor, "C")  # Default to "C" if lor is not found
    recommendation["recommendation_class"] = cor_to_class.get(cor, "Low Confidence")  # Default to "Low Confidence" if cor is not found
    
    return recommendation

# Function to generate JSON chunks
def generate_json_chunks(metadata, recommendations):
    base_json = {
        "title": metadata["title"],
        "guide_title": metadata["guide_title"],
        "subCategory": [],
        "stage": metadata["stage"],
        "disease": metadata["disease"],
        "rationales": [],
        "references": [],
        "specialty": metadata["specialty"]
    }
    
    json_chunks = []
    for rec in recommendations:
        rec = map_lor_cor(rec)  # Apply mapping of lor and cor to rating and recommendation_class
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
    
    # Extract metadata (title, guide_title, stage, disease, specialty) using regex
    metadata_pattern = r"#\s*(.*?):\s*(.*)"
    metadata_matches = re.findall(metadata_pattern, md_content)
    metadata = {match[0].strip(): match[1].strip() for match in metadata_matches}
    
    # If metadata keys do not exist, use default values
    metadata = {
        "title": metadata.get("Title", "Default Title"),
        "guide_title": metadata.get("Guide Title", "Default Guide Title"),
        "stage": metadata.get("Stage", "Rehabilitation").split(","),
        "disease": metadata.get("Disease", "Fracture").split(","),
        "specialty": metadata.get("Specialty", "orthopedics").split(",")
    }
    
    # Extract recommendations along with lor and cor values
    recommendations = extract_recommendations(md_content)
    
    # Generate JSON chunks
    json_chunks = generate_json_chunks(metadata, recommendations)
    
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
