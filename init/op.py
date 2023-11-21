import json

from init.databaseOperator import executeBatch, search_similar_vectors, initDataBaseForNormalDataV2
from openaiOperator import get_batch_embeddings, get_single_embedding, classify_apps_batch

BATCH_SIZE = 100

filepath = 'gpthunter.json'


def loadJsonFile(filepath):
    # 读取 JSON 数据
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)
    print("finish load data")
    return data


def process_batch(batch_data):
    gizmo_ids, texts = zip(*batch_data)
    embeddings = get_batch_embeddings(texts)

    print("embeddings finished")

    tuples_to_insert = list(zip(gizmo_ids, embeddings))
    executeBatch(tuples_to_insert)

    print("insert finished")


def insertVectorData(data):
    # 读取 JSON 数据
    gizmo_data = [(item['data']['gizmo']['id'],
                   f"{item['data']['gizmo']['display']['name']} {item['data']['gizmo']['display']['description']}")
                  for item in data]

    for i in range(0, len(gizmo_data), BATCH_SIZE):
        batch_data = gizmo_data[i:i + BATCH_SIZE]
        process_batch(batch_data)


def insertDataToDatabase(data):
    print("finis read")
    initDataBaseForNormalDataV2(data)
    print("finis init")


def queryData(user_query):
    query_vector = get_single_embedding(user_query)
    similar_gpts = search_similar_vectors(query_vector)
    # 假设你有一个函数来根据 gpt_id 获取 GPT 对象的详细信息


def filterData(data, uuids):
    # [item for item in data if item["data"]["gizmo"]["id"] not in uuids]
    filtered_data = []
    for item in data:
        if item["data"]["gizmo"]["id"] not in uuids:
            filtered_data.append(item)
    return filtered_data


def clarrify(data):
    app_data = data[:1000]

    classify_apps_batch(app_data)


def initData():
    # getDataJsonFromGit(filepath)
    data = loadJsonFile(filepath)
    # uuids = getAllGptsIDs()
    # filtered_data = filterData(data, uuids)
    # print("new data lenth ", len(filtered_data))
    # insertDataToDatabase(filtered_data)
    # insertVectorData(filtered_data)
    clarrify(data)

if __name__ == '__main__':
    initData()
