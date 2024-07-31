
import requests
from requests.auth import HTTPBasicAuth
import json
from datetime import datetime


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
            "summary": data["name"] if "name" in data else "New initiative",
            "customfield_10033": data["acceptance_criteria"] if "acceptance_criteria" in data else "New acceptance_criteria",
            "customfield_10008": data["actual_start"] if "actual_start" in data else "2024-07-31",
            "customfield_10034": data["implementation_benefit"] if "implementation_benefit" in data else "New implementation_benefit",
            "customfield_10035": data["value_addition"] if "value_addition" in data else "New value_addition",
            "labels": data["labels"] if "labels" in data else ["Newlabel"],
            "issuetype": {
               "name": "Initiative"
            }
         }
      })
   
   print(payload)
   response = requests.request(
      "POST",
      url,
      data=payload,
      headers=headers,
      auth=auth
   )
   print(response.status_code)

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
            "summary": data["name"] if "name" in data else "New Epic",
            "description": data["description"] if "description" in data else "New description",
            # "customfield_10001": data["team"] if "team" in data else "New team",
            "customfield_10033": data["acceptance_criteria"] if "acceptance_criteria" in data else "New acceptance_criteria",
            "customfield_10034": data["implementation_benefit"] if "implementation_benefit" in data else "New implementation_benefit",
            "customfield_10035": data["value_addition"] if "value_addition" in data else "New value_addition",
            "customfield_10036": data["components"] if "components" in data else ["components"],
            "customfield_10039": data["team"] if "team" in data else "team",
            "labels": data["labels"] if "labels" in data else ["Newlabel"],
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
            "summary": data["name"] if "name" in data else "New Story",
            "description": data["description"] if "name" in data else "New description",
            "customfield_10033": data["acceptance_criteria"] if "acceptance_criteria" in data else "New acceptance_criteria",
            "customfield_10034": data["implementation_benefit"] if "implementation_benefit" in data else "New implementation_benefit",
            "customfield_10035": data["value_addition"] if "value_addition" in data else "New value_addition",
            "customfield_10037": data["team"] if "team" in data else "team",
            "customfield_10016": data["estimate"] if "estimate" in data else 5,
            "labels": data["labels"] if "labels" in data else ["Newlabel"],
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
      if "initiative" in data:
         initiative = createInitiative(data["initiative"])

         if "epics" in data["initiative"]:
            for ep in data["initiative"]["epics"]:
               epic = createEpic(ep
                                 #   ,json.loads(initiative.text)["key"]
                                 )
               if "stories" in ep:
                  for st in ep["stories"]:
                        story = createStory(ep
                                    ,json.loads(epic.text)["key"]
                                    )
            
   #  response = getInitiative("TP-19")
   #  print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
    

    

