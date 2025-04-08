import os

import spacy
import pymupdf4llm
from docx import Document
from celery import shared_task
from resumes.models import Resume

nlp = spacy.load('en_core_web_sm')

# Load skills from file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS_FILE = os.path.join(BASE_DIR, 'resumes', 'skills.txt')

with open(SKILLS_FILE, 'r') as f:
    SKILLS = {line.strip().lower() for line in f if line.strip()}

@shared_task
def process_resume(resume_id):
    resume = Resume.objects.get(id=resume_id)
    file_path = resume.file.path

    # Extract raw text
    if file_path.endswith('.pdf'):
        # Use pymupdf4llm for PDF extraction
        doc = pymupdf4llm.to_markdown(file_path)
        raw_text = doc  # Returns a string in Markdown format
    elif file_path.endswith('.docx'):
        doc = Document(file_path)
        raw_text = '\n'.join(paragraph.text for paragraph in doc.paragraphs)
    else:
        return

    # Clean text: normalize whitespace
    cleaned_text = ' '.join(word for word in raw_text.split() if word.strip())
    cleaned_text = ''.join(char for char in cleaned_text if char.isprintable())  # Remove non-printable chars

    # Extract skills
    text_lower = cleaned_text.lower()
    words = set(text_lower.split())
    skills = [skill for skill in SKILLS if skill in words]

    # Optional: spaCy for additional entities
    doc = nlp(text_lower)
    extra_entities = [ent.text for ent in doc.ents if ent.label_ in ['SKILLS']]
    print(extra_entities)
    skills.extend(extra_entities)

    extracted_data = {
        'skills': list(set(skills)),  # Remove duplicates
        'text': cleaned_text[:5000],
    }

    resume.extracted_data = extracted_data
    resume.processed = True
    resume.save()