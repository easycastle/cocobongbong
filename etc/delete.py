import requests

url = "https://api.notion.com/v1/blocks/28ba0702-2550-4083-9d29-5718b1288bc6"
token = "secret_WAK9yZqCfV0rMKmE13WqHEnqxNJEWnpQVuNjYzmtUXv"

headers = {
    "Authorization": "Bearer " + token,
    "Notion-Version": "2022-02-22"
}

response = requests.get(url, headers=headers)

print(response.json())