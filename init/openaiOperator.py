import os

import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_batch_embeddings(texts):
    responses = openai.Embedding.create(
        input=texts,
        model="text-embedding-ada-002"
    )
    return [response['embedding'] for response in responses['data']]

def get_single_embedding(text):
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response['data'][0]['embedding']

def classify_apps_batch(app_data):
    # 创建一个包含多个输入的列表
    classifications = []

    # 分成大小为100的子批次
    batch_size = 20
    for i in range(0, len(app_data), batch_size):
        batch = app_data[i:i+batch_size]

        # 创建子批次的输入
        batch_inputs = []
        for app_info in batch:
            name = app_info['data']['gizmo']['display']['name']
            description = app_info['data']['gizmo']['display']['description']
            input_text = f"Please classify the following application based on its name and description:\n\nApplication Name: {name}\nApplication Description: {description}"
            batch_inputs.append(input_text)

        # 使用 OpenAI API 调用生成分类结果，每个子批次只生成一个选择
        responses = openai.Completion.create(
            engine="text-davinci-003",
            prompt=batch_inputs,  # 将子批次的输入作为列表传递
            max_tokens=1024,
            n=len(batch),  # 指定生成的回应数量为子批次大小
        )

        # 提取生成的分类结果并添加到总的分类列表中
        batch_classifications = [response.choices[0].text.strip() for response in responses]
        classifications.extend(batch_classifications)
    return classifications
