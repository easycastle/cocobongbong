import requests, json

token = "secret_KqzDNQ5Ieq9mbswQCvhQyxYj9h8g7OQVctziq5im1JU"

database_id = "5b51b804b0204c5badc31ebc69ec9bea"

headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json",
    "Notion-Version": "2022-02-22"
}
        
def create_subject(new_subject, professor_id, database_id=database_id, headers=headers):
    create_url = "https://api.notion.com/v1/pages"

    new_subject_data = {
        "parent": {"database_id": database_id},
        "properties": {
            "과목": {
                "title": [
                    {
                        "text": {
                            "content": new_subject
                        }
                    }
                ]
            }, 
            "교수님": {
                "rich_text": [
                    {
                        "text": {
                            "content": professor_id
                        }
                    }
                ]
            }, 
        }
    }
    data = json.dumps(new_subject_data)

    requests.post(url=create_url, headers=headers, data=data)