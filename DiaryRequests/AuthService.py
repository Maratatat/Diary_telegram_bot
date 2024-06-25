import requests
import json
from DiaryRequests.BaseRequest import baseUrl, baseHeaders


def Register(login: str, password: str, passwordConfirm: str):
    body = json.dumps({"login": login, "password": password, "passwordConfirm": passwordConfirm})
    response = requests.post(baseUrl + '/register?api-version=1', data=body, headers=baseHeaders, verify=False)
    if response.status_code == 200 or response.status_code == 400 or response.status_code == 500:
        return response.json()
    return f'{response.status_code}\n{response.headers}'


def Login(login: str, password: str):
    body = json.dumps({"login": login, "password": password})
    response = requests.post(baseUrl + '/login?api-version=1', data=body, headers=baseHeaders, verify=False)
    if response.status_code == 200 or response.status_code == 400 or response.status_code == 500:
        return response.json()
    return f'{response.status_code}\n{response.headers}'
