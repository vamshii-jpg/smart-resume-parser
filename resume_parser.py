import re
import fitz  # PyMuPDF
import docx
import spacy
from skills import SKILLS

nlp = spacy.load("en_core_web_sm")

def extract_text(file, file_type):
    text = ""
    if file_type == "pdf":
        pdf = fitz.open(stream=file.read(), filetype="pdf")
        for page in pdf:
            text += page.get_text()
    else:
        doc = docx.Document(file)
        for para in doc.paragraphs:
            text += para.text + "\n"
    return text


def extract_email(text):
    match = re.search(r"\S+@\S+", text)
    return match.group() if match else "Not Found"


def extract_phone(text):
    match = re.search(r"\+?\d[\d\s\-]{8,}", text)
    return match.group() if match else "Not Found"


def extract_name(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return "Not Found"


def extract_skills(text):
    text = text.lower()
    found_skills = [skill for skill in SKILLS if skill in text]
    return list(set(found_skills))


def extract_education(text):
    education_keywords = ["b.tech", "bachelor", "degree", "m.tech", "master"]
    lines = text.lower().split("\n")
    edu = [line for line in lines if any(k in line for k in education_keywords)]
    return edu if edu else ["Not Found"]


def parse_resume(file, file_type):
    text = extract_text(file, file_type)
    return {
        "Name": extract_name(text),
        "Email": extract_email(text),
        "Phone": extract_phone(text),
        "Skills": extract_skills(text),
        "Education": extract_education(text)
    }
