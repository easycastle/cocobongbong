import requests, json

# def createPage(databaseId, headers):

#     createdUrl = "https://api.notion.com/v1/pages"

    
#     newPageData = {
#                 "parent": {"database_id": databaseId},
#                 "properties": {
#                     "과목": {
#                         "title": [
#                             {
#                                 "text": {
#                                     "content": 'asdf'
#                                 }
#                             }
#                         ]
#                     }, 
#                     "과목번호": {
#                         "number": 6
#                     }
#                 }
#             }

#     data = json.dumps(newPageData)

#     res = requests.post(createdUrl, headers=headers, data=data)

#     print(res.text)
        
def create_subject(new_subject, database_id, headers):
    create_url = "https://api.notion.com/v1/pages"
    
    # subject_id = len(get_db(database_id))

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
                "number": 9
            }
        }
    }
    data = json.dumps(new_subject_data)

    res = requests.post(url=create_url, headers=headers, data=data)
    print(res.text)
        
token = "secret_VNFjX2dIU8pYvRT9Mdgax09UPWrN4Z6qBMWb7ANtHFq"

databaseId = "5b51b804b0204c5badc31ebc69ec9bea"

headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json",
    "Notion-Version": "2022-02-22"
}

# createPage(databaseId, headers)
create_subject('new_subject', databaseId, headers)