import requests, json

def updatePage(page_id, headers):
    update_data = {
        "properties": {
            "조교님": {
                "rich_text": [
                    {
                        "text": {
                            "content": "asdf"
                        }
                    }
                ]
            }
        }
    }


    response = requests.patch(f'https://api.notion.com/v1/pages/{page_id}', headers=headers, data=json.dumps(update_data))
        
token = "secret_KqzDNQ5Ieq9mbswQCvhQyxYj9h8g7OQVctziq5im1JU"

databaseId = "5b51b804b0204c5badc31ebc69ec9bea"
page_id = 'c610a807ae8a4ff2b3a7b6821f434299'


headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json",
    "Notion-Version": "2022-02-22"
}

updatePage(page_id, headers)