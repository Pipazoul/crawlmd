import argparse
from firecrawl import FirecrawlApp
import time
import os
import json
import re
import dotenv

def sanitize_text(text):
    return re.sub(r'[^a-zA-Z0-9]', '', text)

def sanitize_url(url):
    return re.sub(r'https?://', '', sanitize_text(url))

dotenv.load_dotenv()

# Set up argument parsing
parser = argparse.ArgumentParser(description='Scrape a website and save articles.')
parser.add_argument('url', type=str, help='The URL to crawl')
parser.add_argument('--limit', '-l', type=int, default=0, help='Limit the number of items to scrape (optional)')

args = parser.parse_args()

api_key = os.getenv('API_KEY')
api_url = os.getenv('API_URL')

app = FirecrawlApp(
    api_key=api_key,
    api_url=api_url
)

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