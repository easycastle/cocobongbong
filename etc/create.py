import requests, json

token = "secret_KqzDNQ5Ieq9mbswQCvhQyxYj9h8g7OQVctziq5im1JU"

database_id = "5b51b804b0204c5badc31ebc69ec9bea"

headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json",
    "Notion-Version": "2022-02-22"
}
        
def create_subject(new_subject, database_id=database_id, headers=headers):
    read_url = f'https://api.notion.com/v1/databases/{database_id}/query'
        
    read_res = requests.post(read_url, headers=headers)
    read_data = read_res.json()['results']
    
    subject_id = len(read_data)

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
            "과목번호": {
                "number": subject_id
            }
        }
    }
    data = json.dumps(new_subject_data)

    requests.post(url=create_url, headers=headers, data=data)