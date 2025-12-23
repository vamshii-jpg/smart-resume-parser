import streamlit as st
import pandas as pd
import json
import os
from resume_parser import parse_resume

# Set Streamlit page configuration
st.set_page_config(page_title="Smart Resume Parser", layout="centered")
st.title("📄 Smart Resume Parser using NLP")

# Create outputs folder if it doesn't exist
if not os.path.exists("outputs"):
    os.makedirs("outputs")

# File uploader
uploaded_file = st.file_uploader(
    "Upload Resume (PDF or DOCX)",
    type=["pdf", "docx"]
)

if uploaded_file:
    file_type = uploaded_file.name.split(".")[-1]  # Get file extension
    resume_name = uploaded_file.name.split(".")[0]  # Name without extension

    if st.button("Parse Resume"):
        # Parse the resume
        result = parse_resume(uploaded_file, file_type)

        # Display results in UI
        st.subheader("🔍 Extracted Information")
        for key, value in result.items():
            st.write(f"**{key}:** {value}")

        # Convert result to DataFrame
        df = pd.DataFrame([result])

        # Save CSV and JSON using resume name
        csv_path = f"outputs/{resume_name}_parsed.csv"
        json_path = f"outputs/{resume_name}_parsed.json"

        df.to_csv(csv_path, index=False)
        with open(json_path, "w") as f:
            json.dump(result, f, indent=4)

        st.success(f"Resume parsed successfully! Files saved in outputs/ folder.")

        # Download buttons
        st.download_button(
            "Download CSV",
            data=df.to_csv(index=False),
            file_name=f"{resume_name}_parsed.csv",
            mime="text/csv"
        )

        st.download_button(
            "Download JSON",
            data=json.dumps(result, indent=4),
            file_name=f"{resume_name}_parsed.json",
            mime="application/json"
        )
