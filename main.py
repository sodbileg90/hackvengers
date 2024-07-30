
import JiraRestApi
from model import Todos
from fastapi import FastAPI

app = FastAPI()


@app.get("/getJira{key}")
async def getJira(key):
    result = JiraRestApi.getInitiative(key)
    return {"result": result}

@app.post("/postJira")
async def postJiraData(request: Todos):
    JiraRestApi.createJira()


