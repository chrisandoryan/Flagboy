import requests
import os
from dotenv import load_dotenv
load_dotenv()

BASE_URL = os.environ["CTFD_URL"]
TOKEN = os.environ["CTFD_TOKEN"]

headers = {
    "Authorization": f"Bearer {TOKEN}"
}

def create_challenge(name, description, category):
    url = f"{BASE_URL}/api/v1/challenges"
    data = {
        "name": name, 
        "category": category,
        "description": description, 
        "initial": "1000",
        "function": "logarithmic", 
        "decay": "4", 
        "minimum": "600", 
        "state": "visible", 
        "type": "dynamic"
    }
    return requests.post(url, headers=headers, json=data).json()


def create_flag(challenge_id, flag):
    url = f"{BASE_URL}/api/v1/flags"
    data = {
        "challenge_id": challenge_id,
        "content": flag,
        "type":"static",
        "data":""
    }
    return requests.post(url, headers=headers, json=data).json()

def update_flag(challenge_id, updated_flag):
    url = f"{BASE_URL}/api/v1/flags/{challenge_id}"
    data = {
        "id": challenge_id,
        "content": updated_flag,
        "data":"",
        "type":"static"
    }
    return requests.patch(url, headers=headers, json=data).json()