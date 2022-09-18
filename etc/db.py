import requests, json

database_id = {
    'subject':                '5b51b804b0204c5badc31ebc69ec9bea', 
    'professor':              '82fe41190f4041979003f40c2adc4797', 
    'student':                '304c611cfcac44a482b80a52badc6cec', 
}

token = 'secret_KqzDNQ5Ieq9mbswQCvhQyxYj9h8g7OQVctziq5im1JU'

headers = {
    'Authorization': 'Bearer ' + token, 
    'Accept': 'application/json',
    'Notion-Version': '2022-02-22'
}

def get_db(database_id, headers=headers):
    read_url = f'https://api.notion.com/v1/databases/{database_id}/query'
    
    res = requests.post(read_url, headers=headers)
    data = res.json()['results']
    
    return data

def get_subject(database_id=database_id['subject']):
    data = get_db(database_id)
    
    subject = []
    
    for info in list(map(lambda x: x['properties'], data)):
        subject.append(info['과목']['title'][0]['text']['content'])
    
    return subject