import requests, json

database_id = {
    'subject':                '5b51b804b0204c5badc31ebc69ec9bea', 
    'professor_role':         '76f7e517847047cfaa37aef759f444c0', 
    'student_role':           '1db0280bb07b4bb1a884710638dd900a', 
    'professor':              '17ce9c31628d415e8cc2646bed60a598', 
    'student':                '304c611cfcac44a482b80a52badc6cec', 
}

token = 'secret_WAK9yZqCfV0rMKmE13WqHEnqxNJEWnpQVuNjYzmtUXv'

headers = {
    'Authorization': 'Bearer ' + token, 
    'Accept': 'application/json',
    'Notion-Version': '2022-02-22'
}

def check_subject(database_id=database_id['subject'], headers=headers):
    read_url = f'https://api.notion.com/v1/databases/{database_id}/query'
    
    res = requests.post(read_url, headers=headers)
    data = res.json()['results']
    
    subject = []
    
    for info in list(map(lambda x: x['properties'], data)):
        subject.append((info['과목번호']['number'], info['과목']['title'][0]['text']['content']))
        
    subject.sort(key=lambda x: x[0])
    
    return list(map(lambda x: x[1], subject))