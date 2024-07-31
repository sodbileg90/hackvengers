
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

def createInitiative(data,actual_start):
   payload = json.dumps( 
      {
         "fields": {
            "project":
            {
               "key": "TP"   
            },
            "summary": data["summary"] if "summary" in data else "New initiative",
            "summary": data["summary"] if "summary" in data else "New initiative",
            "customfield_10033": data["acceptance_criteria"] if "acceptance_criteria" in data else "New acceptance_criteria",
            "customfield_10008": data["actual_start"] if "actual_start" in data else "2024-07-31",
            "customfield_10034": data["implementation_benefit"] if "implementation_benefit" in data else "New implementation_benefit",
            "customfield_10035": data["value_addition"] if "value_addition" in data else "New value_addition",
            "description": data["description"] if "description" in data else "New description",
            "description": data["description"] if "description" in data else "New description",
            "labels": data["labels"] if "labels" in data else ["Newlabel"],
            # "customfield_10015": actual_start,
            # "customfield_10015": actual_start,
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

def createEpic(data,team,actual_start
               # ,initKey
               ):
   payload = json.dumps( 
      {
         "fields": {
            "project":
            {
               "key": "TP"   
            },
            "summary": data["summary"] if "summary" in data else "New Epic",
            "summary": data["summary"] if "summary" in data else "New Epic",
            "description": data["description"] if "description" in data else "New description",
            "customfield_10033": data["acceptance_criteria"] if "acceptance_criteria" in data else "New acceptance_criteria",
            "customfield_10034": data["implementation_benefit"] if "implementation_benefit" in data else "New implementation_benefit",
            "customfield_10035": data["value_addition"] if "value_addition" in data else "New value_addition",
            "customfield_10036": data["components"] if "components" in data else ["components"],
            "customfield_10039": team,
            "customfield_10015": actual_start,
            "customfield_10039": team,
            "customfield_10015": actual_start,
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

def createStory(data,team,actual_start,epicKey):
   with open('teambook.json') as f:
    assignees = json.load(f)
   
   accountId = "712020:32e16a5d-d072-4d65-9418-e029bebc6544"
   if "skill" in data:
      for user in assignees["users"]:
         
         for skill in user["skills"]:
            if data["skill"] == skill:
               accountId = user["userId"]
               break

   payload = json.dumps( 
      {
         "fields": {
            "project":
            {
               "key": "TP"   
            },
            "summary": data["summary"] if "summary" in data else "New Story",
            "description": data["description"] if "description" in data else "New description",
            "summary": data["summary"] if "summary" in data else "New Story",
            "description": data["description"] if "description" in data else "New description",
            "customfield_10033": data["acceptance_criteria"] if "acceptance_criteria" in data else "New acceptance_criteria",
            "customfield_10034": data["implementation_benefit"] if "implementation_benefit" in data else "New implementation_benefit",
            "customfield_10035": data["value_addition"] if "value_addition" in data else "New value_addition",
            "customfield_10037": team,
            "customfield_10015": actual_start,
            "customfield_10037": team,
            "customfield_10015": actual_start,
            "customfield_10016": data["estimate"] if "estimate" in data else 5,
            "labels": data["labels"] if "labels" in data else ["Newlabel"],
            "assignee": {
               "id": accountId
            },
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
   
   with open('data.json') as f:
      data = json.load(f)
      if "initiative" in data:
         
         team = data["team"] if "team" in data else "team"
         actual_start = data["actual_start"] if "actual_start" in data else "2024-07-31"
         initiative = createInitiative(data["initiative"],actual_start)
         
         team = data["team"] if "team" in data else "team"
         actual_start = data["actual_start"] if "actual_start" in data else "2024-07-31"
         initiative = createInitiative(data["initiative"],actual_start)
         if "epics" in data["initiative"]:
            for ep in data["initiative"]["epics"]:
               
               epic = createEpic(ep,team,actual_start
                                 #   ,json.loads(initiative.text)["key"]
                                 )
               if "stories" in ep:
                  for st in ep["stories"]:
                        story = createStory(st,team,actual_start
                                    ,json.loads(epic.text)["key"]
                                    )
            
createJira()            
# response = getInitiative("TP-230")
# print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
    

    

