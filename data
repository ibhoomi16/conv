import streamlit as st
import markdown_it
import re
import json

# Function to parse markdown content and convert it to JSON
def parse_markdown_to_json(markdown_content):
    md = markdown_it.MarkdownIt()
    
    # Convert markdown to HTML (optional, for visualization)
    html_content = md.render(markdown_content)

    # Split markdown into lines
    lines = markdown_content.split("\n")
    
    # Initialize variables to store the extracted data
    title = ""
    recommendation = ""
    lor_rating = "Unknown"
    cor_class = "Unknown"
    
    # Loop through each line and extract relevant information
    for line in lines:
        if "title" in line:
            title = line.strip()  # Extract the title from the line
        elif "recommendation_content" in line:
            recommendation = line.strip()  # Extract recommendation content
        elif "lor:" in line:
            lor_match = re.search(r'lor:\s*(\w)', line)
            lor_rating = lor_match.group(1) if lor_match else "Unknown"
        elif "cor:" in line:
            cor_match = re.search(r'cor:\s*(\w)', line)
            cor_class = cor_match.group(1) if cor_match else "Unknown"

    # Build the JSON structure
    json_data = [{
        "title": title,
        "guide_title": title,  # Set guide_title to be the same as title
        "recommendation_content": recommendation,
        "rating": lor_rating,  # From 'lor'
        "recommendation_class": cor_class,  # From 'cor'
        "disease": ["Pain"],  # Example disease field
        "stage": ["Rehabilitation"],  # Example stage
        "specialty": ["Orthopedics"],  # Example specialty
        "rationales": [],  # Placeholder for rationales
        "references": [],  # Placeholder for references
        "subCategory": []  # Placeholder for subcategories
    }]
    
    return json_data

# Streamlit App UI and Logic
def main():
    st.title("Markdown to JSON Converter")
    
    # Upload markdown file
    uploaded_file = st.file_uploader("Upload a Markdown file", type=["md"])
    
    if uploaded_file is not None:
        # Read the file content
        markdown_content = uploaded_file.read().decode("utf-8")
        
        # Display the uploaded markdown content
        st.subheader("Uploaded Markdown Content")
        st.text(markdown_content)

        # Convert to JSON
        json_data = parse_markdown_to_json(markdown_content)
        
        # Display the converted JSON
        st.subheader("Converted JSON Output")
        st.json(json_data)
        
        # Provide a download button for the JSON file
        json_output = json.dumps(json_data, indent=4)
        st.download_button(
            label="Download JSON",
            data=json_output,
            file_name="output.json",
            mime="application/json"
        )

if __name__ == "__main__":
    main()
