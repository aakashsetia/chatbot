import json
import boto3
from boto3.dynamodb.conditions import Key
kb_table = boto3.resource('dynamodb').Table('REOProductKnowledgeBase')



def build_response(message):
    
    response = {
        "dialogAction": {
            "type": "ElicitIntent",
            "message": {
              "contentType": "PlainText",
              "content": message
            },
                "responseCard": {
      "version": 1,
      "contentType": "application/vnd.amazonaws.card.generic",
      "genericAttachments": [
          {

             "subTitle": "Select YES if you want more information and NO to say goodbye!",
             "buttons":[
          {
            "text": "Yes",
            "value": "Yes Trigger REOorgIntent"
          },
          {
            "text": "No",
            "value": "Trigger Goodbye "
          }
        ]
           } 
       ] 
    }
}               
       
                }
    

    return response
     
def lambda_handler(event, context):
    # Search for Response in DynamoDB Table
    
    print(event)
    Tool  = event['currentIntent']['slots']['Tool']
    Qcard = event['currentIntent']['slots']['Qcard']
    
    response_db = kb_table.query(
        
         KeyConditionExpression=Key('Tool').eq(Tool) & Key('Qcard').eq(Qcard)
         
)
    items = response_db['Items']
    
    if len(items) == 0:
        msg = "No record found in Knowledge Base on "+Tool+" "+Qcard+ " We are working on adding more data to help you better" 
    else:
        msg = response_db['Items'][0]['Response']
    return build_response(msg) 

