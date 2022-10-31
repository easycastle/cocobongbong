import requests, json

token = "secret_KqzDNQ5Ieq9mbswQCvhQyxYj9h8g7OQVctziq5im1JU"

headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json",
    "Notion-Version": "2022-02-22"
}

def add_assistant(page_id, assistant_id, headers=headers):
    update_data = {
        "properties": {
            "도우미": {
                "rich_text": [
                    {
                        "text": {
                            "content": assistant_id
                        }
                    }
                ]
            }
        }
    }


    requests.patch(f'https://api.notion.com/v1/pages/{page_id}', headers=headers, data=json.dumps(update_data))
        
