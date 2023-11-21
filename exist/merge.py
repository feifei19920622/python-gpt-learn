import json

import requests


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
                "id": id
            }
            new_element.append(new_item)

    # 指定要写入的 JSON 文件的文件名
    output_file_name = 'D:\code\python-gpt-learn\exist\output.json'

    # 使用 'w' 模式打开文件以写入数据
    with open(output_file_name, 'w') as output_file:
        # 将修改后的数据写入 JSON 文件
        json.dump(new_element, output_file, indent=4)  # 使用缩进美化输出

    print(f"JSON 文件 '{output_file_name}' 初始化完成！")
getDataJsonFromGit()