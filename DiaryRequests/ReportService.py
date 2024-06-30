import requests
import json
from DiaryRequests.BaseRequest import baseUrl, baseHeaders


def GetReportsOfUser(id: int, token: str):
    headers_with_auth = baseHeaders.copy()
    headers_with_auth['Authorization'] = f'Bearer {token}'
    response = requests.get(baseUrl + '/api/v1/Report/reports/' + str(id), headers=headers_with_auth, verify=False)
    if response.status_code == 200 or response.status_code == 400 or response.status_code == 500:
        return response.json()
    return {"responseStatusCode": response.status_code, "responseHeaders": response.headers}


def GetReportById(id: int, token: str):
    headers_with_auth = baseHeaders.copy()
    headers_with_auth['Authorization'] = f'Bearer {token}'
    response = requests.get(baseUrl + '/api/v1/Report/' + str(id), headers=headers_with_auth, verify=False)
    if response.status_code == 200 or response.status_code == 400 or response.status_code == 500:
        return response.json()
    return {"responseStatusCode": response.status_code, "responseHeaders": response.headers}


def DeleteReport(id: int, token: str):
    headers_with_auth = baseHeaders.copy()
    headers_with_auth['Authorization'] = f'Bearer {token}'
    response = requests.delete(baseUrl + '/api/v1/Report/' + str(id), headers=headers_with_auth, verify=False)
    if response.status_code == 200 or response.status_code == 400 or response.status_code == 500:
        return response.json()
    return {"responseStatusCode": response.status_code, "responseHeaders": response.headers}


def CreateReport(name: str, description: str, userId: int, token: str):
    headers_with_auth = baseHeaders.copy()
    headers_with_auth['Authorization'] = f'Bearer {token}'
    body = json.dumps({"name": name, "description": description, "userId": userId})
    response = requests.post(baseUrl + '/api/v1/Report', data=body, headers=headers_with_auth, verify=False)
    if response.status_code == 200 or response.status_code == 400 or response.status_code == 500:
        return response.json()
    return {"responseStatusCode": response.status_code, "responseHeaders": response.headers}


def UpdateReport(id: int, name: str, description: str, token: str):
    headers_with_auth = baseHeaders.copy()
    headers_with_auth['Authorization'] = f'Bearer {token}'
    body = json.dumps({"id": id, "name": name, "description": description})
    response = requests.put(baseUrl + '/api/v1/Report', data=body, headers=headers_with_auth, verify=False)
    if response.status_code == 200 or response.status_code == 400 or response.status_code == 500:
        return response.json()
    return {"responseStatusCode": response.status_code, "responseHeaders": response.headers}
