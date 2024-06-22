import requests
import json
from DiaryRequests.BaseRequest import baseUrl, baseHeaders


def RefreshToken(accessToken: str, refreshToken: str):
    body = json.dumps({"accessToken": accessToken, "refreshToken": refreshToken})
    response = requests.post(baseUrl + '/api/Token/refresh?api-version=1', data=body, headers=baseHeaders, verify=False)
    if response.status_code == 200 or response.status_code == 400 or response.status_code == 500:
        return response.json()
    return f'{response.status_code}\n{response.headers}'
