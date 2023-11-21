import json

import requests


def getDataJsonFromGit(filepath="D:\code\python-gpt-learn\init\gpthunter.json"):
    token = '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'
    repo = 'airyland/gpts-data'
    path = 'data.json'  # GitHub中的路径
    url = f'https://api.github.com/repos/{repo}/contents/{path}'
    print(url)
    headers1 = {'Authorization': f'token {token}'}
    response = requests.get(url, headers=headers1)

    if response.status_code == 200:
        download_url = response.json()['download_url']
    else:
        print("Error fetching file: ", response.status_code)

    response = requests.get(download_url)

    if response.status_code == 200:
        # 将文件内容写入本地文件
        with open(filepath, "wb") as file:
            file.write(response.content)
        print("File downloaded successfully.")
    else:
        print(f"Failed to download file: {response.status_code}")
