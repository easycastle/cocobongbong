import requests
from etc.db import get_db

url = "https://api.notion.com/v1/blocks/28ba0702-2550-4083-9d29-5718b1288bc6"
token = "secret_WAK9yZqCfV0rMKmE13WqHEnqxNJEWnpQVuNjYzmtUXv"

headers = {
    "Authorization": "Bearer " + token,
    "Notion-Version": "2022-02-22"
}

def delete_subject(subject, database_id='5b51b804b0204c5badc31ebc69ec9bea', headers=headers):
    data = get_db(database_id=da)
    
    for page in data:
        if page['properties']['과목']['title'][0]['text']['content'] == subject:
            block_id = page['id']
            
    delete_url = f'https://api.notion.com/v1/blocks/{block_id}'
    
    requests.delete(delete_url, headers)