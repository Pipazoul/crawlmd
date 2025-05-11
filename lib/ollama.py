from ollama import chat
from ollama import Client
from pydantic import BaseModel
import json
import dotenv

dotenv.load_dotenv()
host = os.getenv('OLLAMA_URL')

client = Client(
  host=host,
)

model = 'qwen2.5:14b'
class IsUseful(BaseModel):
    is_useful: bool

def check_article_usefulness(content):
    response = chat(
        messages=[
            {
                'role': 'user',
                'content': f'Is the following article useful? Please answer in JSON format with a boolean. Content: {content}',
            }
        ],
        model = model
    )
    
    return IsUseful.model_validate_json(response.message.content).is_useful

class ArticleSummary(BaseModel):
    summary: str

def create_article_summary(content):
    response = chat(
        messages=[
            {
                'role': 'user',
                'content': f'Please provide a concise summary of the following article. Content: {content}',
            }
        ],
        model = model
    )
    
    return ArticleSummary.model_validate_json(response.message.content).summary

class Tags(BaseModel):
    tags: list[str]

def extract_tags(content):
    response = chat(
        messages=[
            {
                'role': 'user',
                'content': f'Generate a list of relevant tags for the following content. Return as a JSON array. Content: {content}',
            }
        ],
        model = model
    )
    
    return Tags.model_validate_json(response.message.content).tags

class HasDate(BaseModel):
    has_date: bool

def check_for_date(content):
    response = chat(
        messages=[
            {
                'role': 'user',
                'content': f'Is there a date mentioned in the following content? Please answer in JSON format with a boolean. Content: {content}',
            }
        ],
        model = model
    )
    
    return HasDate.model_validate_json(response.message.content).has_date

def get_date(content):
    response = chat(
        messages=[
            {
                'role': 'user',
                'content': f'Please extract the date mentioned in the following content and return it as a string. If no date is found, respond with "No date found". Content: {content}',
            }
        ],
        model = model
    )
    
    return json.loads(response.message.content)