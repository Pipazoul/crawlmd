import requests
import re
import os
from tika import parser
import lib.sanitize

# Function to extract PDF URLs from a given text
def extract_pdf_urls(text, domainUrl):
    # Regular expression pattern to find all URLs ending with .pdf
    url_pattern = r'(?:https?://|/)([^ ]+\.pdf)'
    urls = re.findall(url_pattern, text)
    
    # Prepend domain to relative URLs if they start with '/'
    final_urls = []
    for url in urls:
        # if do not start with http, add domain
        if not url.startswith('http'):
            print("DOI: ", domainUrl)
            # Assuming the base URL is 'http://example.com', adjust as needed
            final_url = domainUrl + url
            final_urls.append(final_url)
        else:
            final_urls.append(url)
    
    return final_urls

def download_pdf(url, save_dir):
    try:
        # Get the response from the URL
        response = requests.get(url)
        
        # Extract the filename from the URL's last part
        filename = url.split('/')[-1]
        
        # Ensure the save directory exists; create it if necessary
        os.makedirs(save_dir, exist_ok=True)
        
        # Construct the full path to save the file
        save_path = os.path.join(save_dir, filename)
        
        print(f"Downloading: {filename}")
        
        # Write the content to the file
        with open(save_path, 'wb') as file:
            file.write(response.content)
            
    except Exception as e:
        print(f"Error downloading {url}: {str(e)}")



def pdf_to_markdown(pdf_path, save_dir):
    try:
        # Parse the PDF file
        parsed = parser.from_file(pdf_path)
        
        # Extract the content
        content = parsed['content']

        # Clean the content
        content = lib.sanitize.clean_text(content)
        
        # Construct the output filename
        filename = os.path.basename(pdf_path).replace('.pdf', '.md')
        
        # Ensure the save directory exists; create it if necessary
        os.makedirs(save_dir, exist_ok=True)
        
        # Construct the full path to save the file
        save_path = os.path.join(save_dir, filename)
        
        print(f"Converting: {filename}")
        
        # Write the content to the file
        with open(save_path, 'w') as file:
            file.write(content)
            
    except Exception as e:
        print(f"Error converting {pdf_path}: {str(e)}")
