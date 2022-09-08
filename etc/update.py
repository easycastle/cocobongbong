import requests, json

def updatePage(page_id, headers):
    updateUrl = f"https://api.notion.com/v1/pages/{page_id}"

    updateData = {
        "properties": {
            "과목": {
                "title": [
                    {
                        "text": {
                            "content": "C"
                        }
                    }
                ]
            },
            "과목번호": {
                "number": 7
            }
        }
    }

    data = json.dumps(updateData)

    response = requests.request('PATCH', updateUrl, headers=headers, data=data)

    print(response.status_code)
    print(response.text)
        
token = "secret_WAK9yZqCfV0rMKmE13WqHEnqxNJEWnpQVuNjYzmtUXv"

databaseId = "5b51b804b0204c5badc31ebc69ec9bea"
page_id = '2b4b6eee2bb244a3b709e4e074634147'


headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json",
    "Notion-Version": "2022-02-22"
}

updatePage(page_id, headers)