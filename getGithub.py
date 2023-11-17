import requests

# GitHub 仓库的 Raw 文件 URL
github_raw_url = "https://github.com/airyland/gpts-data/blob/master/data.json"

# 替换为你的 GitHub 访问令牌
github_access_token = "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"

# 添加 Authorization 请求头
headers = {
    "Authorization": f"token {github_access_token}"
}

# 发起 GET 请求来获取文件内容，传入请求头
response = requests.get(github_raw_url, headers=headers)


# 检查响应状态码
if response.status_code == 200:
    # 获取文件内容
    file_content = response.text

    # 打印文件内容（这里只会打印部分内容，因为文件可能很大）
    print(file_content[:500])  # 打印文件的前500个字符
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")
