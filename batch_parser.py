import os
from resume_parser import parse_resume
import pandas as pd
import json

# Loop through all resumes in sample_resumes folder
for file_name in os.listdir("sample_resumes"):
    if file_name.endswith((".pdf", ".docx")):
        with open(f"sample_resumes/{file_name}", "rb") as f:
            file_type = file_name.split(".")[-1]
            result = parse_resume(f, file_type)
            
            # Save output files with resume name
            base_name = file_name.split(".")[0]
            pd.DataFrame([result]).to_csv(f"outputs/{base_name}_parsed.csv", index=False)
            with open(f"outputs/{base_name}_parsed.json", "w") as jf:
                json.dump(result, jf, indent=4)

print("All resumes parsed successfully! Check outputs/ folder.")
