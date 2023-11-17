import json
import os

import json
import requests
import base64

# 指定包含JSON文件的目录路径
directory_path = './'  # 替换为实际的目录路径

# 初始化一个空的JSON数组，用于存储所有JSON数据
all_json_data = []
exists = []
# 遍历目录中的所有文件
for filename in os.listdir(directory_path):
    if filename.endswith('.json'):
        file_path = os.path.join(directory_path, filename)
        try:
            # 读取JSON文件并解析数据
            with open(file_path, 'r', encoding='utf-8') as json_file:
                json_data = json.load(json_file)
                exists.extend(json_data)
                print(f"已初始化文件：{file_path}")
        except Exception as e:
            print(f"初始化文件时出错：{file_path}", str(e))

# 将合并后的数据写入输出文件（覆盖已存在的文件内容）
with open("aTotal.json", 'w') as output_json:
    json.dump(exists, output_json, indent=4)


# GitHub设置
# token = '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'
token = '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'
repo = 'feifei19920622/thegpts'
branch = 'main'
path = 'public/jsons/aTotal.json'  # GitHub中的路径
url = f'https://api.github.com/repos/{repo}/contents/{path}'

# 获取文件的当前SHA
headers = {
    'Authorization': f'token {token}',
    'Content-Type': 'application/json',
}
response = requests.get(url, headers=headers)

if response.status_code == 200:
    sha = json.loads(response.content)['sha']
else:
    print('Error getting file SHA:', response.content)
    exit()

# 要上传的文件
file_content = open('aTotal.json', 'rb').read()
b64_content = base64.b64encode(file_content)

# API请求（更新文件）
data = {
    'message': 'commit message',
    'branch': branch,
    'content': b64_content.decode('utf-8'),
    'sha': sha  # 添加sha值
}

response = requests.put(url, headers=headers, json=data)

if response.status_code in [200, 201]:
    print('File uploaded/updated successfully')
else:
    print('Error:', response.content)