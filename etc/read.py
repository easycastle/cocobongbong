import requests, json

def readDatabase(databaseId, headers):
    
    readUrl = f"https://api.notion.com/v1/databases/{databaseId}/query"

    res = requests.post(readUrl, headers=headers)
    print(res.text)

    data = res.json()['results']
    with open("./db.json", "w", encoding="utf8") as f:
        json.dump(data, f, ensure_ascii=False)
        
token = "secret_KqzDNQ5Ieq9mbswQCvhQyxYj9h8g7OQVctziq5im1JU"

databaseId = "5b51b804b0204c5badc31ebc69ec9bea"

headers = {
    "Authorization": "Bearer " + token,
    "Notion-Version": "2022-02-22"
}

readDatabase(databaseId, headers)