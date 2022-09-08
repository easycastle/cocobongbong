import requests, json

def readDatabase(databaseId, headers):
    
    readUrl = f"https://api.notion.com/v1/databases/{databaseId}/query"

    res = requests.post(readUrl, headers=headers)
    print(res.text)

    data = res.json()['results']
    with open("./db.json", "w", encoding="utf8") as f:
        json.dump(data, f, ensure_ascii=False)
        
token = "secret_VNFjX2dIU8pYvRT9Mdgax09UPWrN4Z6qBMWb7ANtHFq"

databaseId = "82fe41190f4041979003f40c2adc4797"

headers = {
    "Authorization": "Bearer " + token,
    "Notion-Version": "2022-02-22"
}

readDatabase(databaseId, headers)