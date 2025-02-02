import argparse
from firecrawl import FirecrawlApp
import time
import os
import json
import re
import dotenv
from urllib.parse import urlparse
import lib.pdf as pdf

def sanitize_text(text):
    return re.sub(r'[^a-zA-Z0-9]', '', text)

def sanitize_url(url):
    return re.sub(r'https?://', '', sanitize_text(url))

def cleanData(folder_path):
    # loop in data.json and get "markdown" field
    data = []
    with open(f'{folder_path}/data.json', 'r') as f:
        data = json.load(f)

    pdf_urls = []
    for i, item in enumerate(data):
        text = item['markdown']
        print(f'Cleaning item {i}')
        # append pdf urls to pdf_urls
        url = urlparse(item['metadata']['url'])
        pdf_urls += pdf.extract_pdf_urls(text, f'{url.scheme}://{url.netloc}/')

    # save in pdf_urls.json
    with open(f'{folder_path}/pdf_urls.json', 'w') as f:
        json.dump(pdf_urls, f)

    # download pdfs
    for i, pdf_url in enumerate(pdf_urls):
        print(f'Downloading PDF {i}')
        # create pdf folder if it does not exist
        if not os.path.exists(f'{folder_path}/pdf'):
            os.makedirs(f'{folder_path}/pdf')
        pdf.download_pdf(pdf_url, f'{folder_path}pdf')


dotenv.load_dotenv()

# Set up argument parsing
parser = argparse.ArgumentParser(description='Scrape a website and save articles.')
parser.add_argument('--url', '-u', type=str, default=None, help='The URL to crawl')
parser.add_argument('--limit', '-l', type=int, default=0, help='Limit the number of items to scrape (optional)')
parser.add_argument('--clean', '-c', type=str, help='Clean out the contents of a folder (path to the folder)')

args = parser.parse_args()

FIRECRAWL_API_KEY = os.getenv('FIRECRAWL_API_KEY')
FIRECRAWL_API_URL = os.getenv('FIRECRAWL_API_URL')

app = FirecrawlApp(
    api_key=FIRECRAWL_API_KEY,
    api_url=FIRECRAWL_API_URL
)

if args.clean:
    cleanData(args.clean)
else:

    if args.url is None:
        print("No URL specified. Please provide a URL.")
        exit(1)


    url = args.url
    limit = args.limit
    params = {'scrapeOptions': {'formats': ['markdown']}}
    
    if limit > 0:
        params['limit'] = limit
    
    # Initialize the crawl and get status
    crawl_status = app.async_crawl_url(url, params)
    print(crawl_status)
    
    data = []
    while True:
        status = app.check_crawl_status(crawl_status['id'])
        print(status['status'], f"{status['completed']} / {status['total']}")
        
        if status['status'] == 'completed':
            data = status['data']
            break
        time.sleep(2)
    
    domain = url.split('/')[2]
    output_path = domain.replace('.', '_')
    
    # Create output folder if it does not exist
    if not os.path.exists(output_path):
        os.makedirs(output_path)
        
    # Create articles subfolder inside the output folder
    if not os.path.exists(f'{output_path}/articles'):
        os.makedirs(f'{output_path}/articles')
        
    with open(f'{output_path}/data.json', 'w') as f:
        json.dump(data, f)
    
    # Write README.md file
    with open(f'{output_path}/README.md', 'w') as f:
        f.write(f'# {time.strftime("%Y-%m-%d %H:%M:%S")}\n')
        f.write(f'## Number of articles: {len(data)}\n')
    
    print(f"Number of items: {len(data)}")
    
    for i, item in enumerate(data):
        sanitized_url = sanitize_url(item['metadata']['sourceURL'])
        title = item['metadata']['title'] if 'title' in item['metadata'] else sanitized_url
        title = sanitize_text(title)
        title = title[:50]
        
        content = item['markdown']
        
        with open(f'{output_path}/articles/{title}.md', 'w') as f:
            f.write(content)
            print(f'File {title}.md written successfully')