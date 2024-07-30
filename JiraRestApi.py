
import requests
from requests.auth import HTTPBasicAuth
import json


# In the url mention the Jira url used
url = "https://sodbileg89.atlassian.net/rest/api/2/issue/"

# We are using HTTPBasicAuth authentication method here.
# For that create a JIRA api token and mention your userid and token down in the brackets()
with open('test.json') as f:
    test = json.load(f)
auth = HTTPBasicAuth(test["t1"], test["t2"])

headers = {
   "Accept": "application/json",
   "Content-Type": "application/json"
}

def getInitiative(id):
    url = "https://sodbileg89.atlassian.net/rest/api/2/issue/" + str(id) 
    response = requests.request(
         "GET",
         url,
         headers=headers,
         auth=auth
      )
    
    return response


def createInitiative(data):
   payload = json.dumps( 
      {
         "fields": {
            "project":
            {
               "key": "TP"   
            },
            "summary": data["name"],
            "customfield_10033": data["acceptance_criteria"],
            "issuetype": {
               "name": "Initiative"
            }
         }
      })
   response = requests.request(
      "POST",
      url,
      data=payload,
      headers=headers,
      auth=auth
   )

   print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))

   return response

def createEpic(data
               # ,initKey
               ):
   payload = json.dumps( 
      {
         "fields": {
            "project":
            {
               "key": "TP"   
            },
            "summary": data["name"],
            "description": data["description"],
            # "parent": {
            #    "key": str(initKey)
            # },
            "issuetype": {
               "name": "Epic"
            }
         }
      })
   response = requests.request(
      "POST",
      url,
      data=payload,
      headers=headers,
      auth=auth
   )

   print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))

   return response

def createStory(data,epicKey):
   payload = json.dumps( 
      {
         "fields": {
            "project":
            {
               "key": "TP"   
            },
            "summary": data["name"],
            "description": data["description"],
            "parent": {
               "key": str(epicKey)
            },
            "issuetype": {
               "name": "Story"
            }
         }
      })
   response = requests.request(
      "POST",
      url,
      data=payload,
      headers=headers,
      auth=auth
   )

   print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))

   return response
   
def createJira():   
   with open('gptdata.json') as f:
      data = json.load(f)
      initiative = createInitiative(data["initiative"])

      for ep in data["initiative"]["epics"]:
         epic = createEpic(ep
                           #   ,json.loads(initiative.text)["key"]
                           )
         for st in ep["stories"]:
               story = createStory(ep
                           ,json.loads(epic.text)["key"]
                           )
            
   #  response = getInitiative("TP-19")
   #  print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
    

    

