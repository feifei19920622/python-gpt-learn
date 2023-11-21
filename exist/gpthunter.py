import base64
import json
import logging
import requests

# 设置日志配置
logging.basicConfig(filename='D:\code\python-gpt-learn\exist\\log.txt',  # 日志文件名
                    filemode='a',  # 模式为'a'表示追加到文件末尾，'w'表示写模式（覆盖）
                    format='%(asctime)s - %(levelname)s - %(message)s',  # 日志格式
                    level=logging.INFO)  # 日志级别



def nuanced_categorization(description):
    description = description.lower()
    if 'market' in description or 'advertise' in description or 'seo' in description or 'email' in description:
        return 'Marketing'
    elif 'educate' in description or 'learn' in description or 'school' in description or 'study' in description:
        return 'Education'
    elif 'finance' in description or 'money' in description or 'invest' in description or 'bank' in description:
        return 'Finance'
    elif 'api' in description or 'development' in description or 'dev' in description or 'developer' in description:
        return 'Development Tools'
    elif 'entertain' in description or 'game' in description or 'music' in description or 'movie' in description:
        return 'Entertainment'
    elif 'research' in description or 'info' in description or 'data' in description:
        return 'Information & Research'
    elif 'web' in description or 'software' in description or 'app' in description or 'programming' in description:
        return 'Web & Software Development'
    elif 'art' in description or 'design' in description or 'paint' in description or 'creative' in description:
        return 'Art & Design'
    elif 'social' in description or 'network' in description or 'community' in description or 'chat' in description:
        return 'Social & Networking'
    elif 'productivity' in description or 'tool' in description or 'manage' in description or 'organize' in description:
        return 'Productivity & Tools'
    elif 'travel' in description or 'geography' in description or 'tourism' in description:
        return 'Travel & Geography'
    elif 'food' in description or 'beverage' in description or 'cook' in description or 'restaurant' in description:
        return 'Food & Beverage'
    elif 'tech' in description or 'technology' in description or 'gadget' in description:
        return 'Technology'
    elif 'language' in description or 'linguistic' in description or 'translate' in description:
        return 'Language Learning'
    elif 'health' in description or 'fitness' in description or 'exercise' in description or 'wellness' in description:
        return 'Health & Fitness'
    elif 'spirituality' in description or 'religion' in description or 'faith' in description:
        return 'Spirituality & Religion'
    elif 'lifestyle' in description or 'life' in description or 'wellness' in description or 'habit' in description:
        return 'Lifestyle & Wellness'

    return 'Other'  # Default category for cases that don't match any category


def getDataJsonFromGit():
    token1 = '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'
    repo1 = 'airyland/gpts-data'
    path1 = 'data.json'  # GitHub中的路径
    url1 = f'https://api.github.com/repos/{repo1}/contents/{path1}'
    print(url1)
    headers1 = {'Authorization': f'token {token1}'}
    response1 = requests.get(url1, headers=headers1)

    if response1.status_code == 200:
        download_url = response1.json()['download_url']
    else:
        print("Error fetching file: ", response1.status_code)

    response1 = requests.get(download_url)

    if response1.status_code == 200:
        # 将文件内容写入本地文件
        with open("D:\code\python-gpt-learn\exist\gpthunter.json", "wb") as file:
            file.write(response1.content)
        print("File downloaded successfully.")
    else:
        print(f"Failed to download file: {response1.status_code}")

    # 从文件中读取 JSON 数据
    with open('D:\code\python-gpt-learn\exist\gpthunter.json', 'r', encoding='utf-8') as input_file:
        datas1 = json.load(input_file)

    # 修改 json_data 中的数据，或者进行其他操作
    new_element = []

    # 使用集合来存储已经添加过的id
    existing_ids = set()

    # 遍历 datas 列表中的每个元素
    for value in datas1:
        title = value["data"]["gizmo"]["display"]["name"]
        description = value["data"]["gizmo"]["display"]["description"]
        author = value["data"]["gizmo"]["author"]["display_name"]
        imagePath = value["data"]["gizmo"]["display"]["profile_picture_url"]
        gptLink = "https://chat.openai.com/g/" + value["data"]["gizmo"]["short_url"]
        id = value["data"]["gizmo"]["id"]

        # 检查id是否已经存在，如果不存在则添加到集合和新元素列表中
        if id not in existing_ids:
            existing_ids.add(id)
            new_item = {
                "title": title,
                "desp": description,
                "author": author,
                "picture": imagePath,
                "url": gptLink,
                # "category": nuanced_categorization(description),
                "id": id
            }
            new_element.append(new_item)

    # 指定要写入的 JSON 文件的文件名
    output_file_name = '/exist/output.txt'

    # 使用 'w' 模式打开文件以写入数据
    with open(output_file_name, 'w') as output_file:
        # 将修改后的数据写入 JSON 文件
        json.dump(new_element, output_file, indent=4)  # 使用缩进美化输出

    print(f"JSON 文件 '{output_file_name}' 初始化完成！")


getDataJsonFromGit()


exists = []
# 从文件中读取 JSON 数据
with open('D:\code\python-gpt-learn\exist\\aTotal.json', 'r', encoding='utf-8') as input_file:
    exists = json.load(input_file)

# 使用集合来存储已经添加过的id
existing_ids = []
for value in exists:
    existing_ids.append(value['id'])

# 从文件中读取 JSON 数据
new_element =[]
with open('/exist/output.txt', 'r', encoding='utf-8') as input_file:
    new_element = json.load(input_file)

# 遍历 datas 列表中的每个元素
for value in new_element:
    id = value['id']
    # 检查id是否已经存在，如果不存在则添加到集合和新元素列表中
    if id not in existing_ids:
        existing_ids.append(id)
        exists.append(value)


# 将合并后的数据写入输出文件（覆盖已存在的文件内容）
with open("D:\code\python-gpt-learn\exist\\aTotal.json", 'w') as output_json:
    json.dump(exists, output_json, indent=4)

logging.info(len(exists))
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
    logging.info('Error getting file SHA:', response.content)
    exit()

# 要上传的文件
file_content = open('D:\code\python-gpt-learn\exist\\aTotal.json', 'rb').read()
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
    logging.info('File uploaded/updated successfully')
else:
    logging.info('Error:', response.content)
