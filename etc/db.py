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
        subject.append((info['과목번호']['number'], info['과목']['title'][0]['text']['content']))
        
    subject.sort(key=lambda x: x[0])
    
    return list(map(lambda x: x[1], subject))

def create_subject(new_subject, database_id=database_id['subject'], headers=headers):
    # todo: create 파일에 있는 create_subject 옮기기 (왜 안 되는지는 모름)
    pass

def get_professor_inform(database_id=database_id['professor']):
    data = get_db(database_id)
    
    professor_introduction = dict()
    
    for info in list(map(lambda x: x['properties'], data)):
        professor_introduction[info['학번']['title'][0]['text']['content']] = info['소개']['rich_text'][0]['text']['content']
        
    return professor_introduction