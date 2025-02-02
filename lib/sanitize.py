import re

def clean_text(text):
    # Remove carriage returns
    text = text.replace('\r', '')
    
    # Replace multiple newlines with a single newline
    text = re.sub(r'\n+', '\n', text)
    
    # Collapse multiple spaces into a single space
    text = re.sub(r' +', ' ', text)
    
    # Remove special characters except letters, numbers, apostrophes, hyphens, and spaces
    text = re.sub(r"[^a-zA-Z0-9'\-\s]", '', text)
    
    return text