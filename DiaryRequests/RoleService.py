import requests
import json
from DiaryRequests.BaseRequest import baseUrl, baseHeaders


def CreateRole(name: str, token: str):
    headers_with_auth = baseHeaders.copy()
    headers_with_auth['Authorization'] = f'Bearer {token}'
    body = json.dumps({"name": name})
    response = requests.post(baseUrl + '/api/Role?api-version=1', data=body, headers=headers_with_auth, verify=False)
    if response.status_code == 200 or response.status_code == 400 or response.status_code == 500:
        return response.json()
    return f'{response.status_code}\n{response.headers}'


def UpdateRole(id: int, name: str, token: str):
    headers_with_auth = baseHeaders.copy()
    headers_with_auth['Authorization'] = f'Bearer {token}'
    body = json.dumps({"id": id, "name": name})
    response = requests.put(baseUrl + '/api/Role?api-version=1', data=body, headers=headers_with_auth, verify=False)
    if response.status_code == 200 or response.status_code == 400 or response.status_code == 500:
        return response.json()
    return f'{response.status_code}\n{response.headers}'


def DeleteRole(id: int, token: str):
    headers_with_auth = baseHeaders.copy()
    headers_with_auth['Authorization'] = f'Bearer {token}'
    response = requests.delete(baseUrl + '/api/Role/' + str(id) + '?api-version=1', headers=headers_with_auth,
                               verify=False)
    if response.status_code == 200 or response.status_code == 400 or response.status_code == 500:
        return response.json()
    return f'{response.status_code}\n{response.headers}'


def AddRoleForUser(login: str, roleName: str, token: str):
    headers_with_auth = baseHeaders.copy()
    headers_with_auth['Authorization'] = f'Bearer {token}'
    body = json.dumps({"login": login, "roleName": roleName})
    response = requests.post(baseUrl + '/api/Role/add-role?api-version=1', data=body, headers=headers_with_auth,
                             verify=False)
    if response.status_code == 200 or response.status_code == 400 or response.status_code == 500:
        return response.json()
    return f'{response.status_code}\n{response.headers}'


def DeleteRoleOfUser(login: str, roleId: int, token: str):
    headers_with_auth = baseHeaders.copy()
    headers_with_auth['Authorization'] = f'Bearer {token}'
    body = json.dumps({"login": login, "roleId": roleId})
    response = requests.delete(baseUrl + '/api/Role/delete-role?api-version=1', data=body, headers=headers_with_auth,
                               verify=False)
    if response.status_code == 200 or response.status_code == 400 or response.status_code == 500:
        return response.json()
    return f'{response.status_code}\n{response.headers}'


def UpdateRoleForUser(login: str, fromRoleId: int, toRoleId: int, token: str):
    headers_with_auth = baseHeaders.copy()
    headers_with_auth['Authorization'] = f'Bearer {token}'
    body = json.dumps({"Login": login, "FromRoleId": fromRoleId, "ToRoleId": toRoleId})
    response = requests.put(baseUrl + '/api/Role/update-role?api-version=1', data=body, headers=headers_with_auth,
                            verify=False)
    if response.status_code == 200 or response.status_code == 400 or response.status_code == 500:
        return response.json()
    return f'{response.status_code}\n{response.headers}'
