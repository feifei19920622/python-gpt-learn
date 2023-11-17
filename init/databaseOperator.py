import json
import os
from urllib.parse import urlparse

import psycopg2
from psycopg2 import pool
from psycopg2.extras import execute_values

database_url = os.getenv("DATABASE_URL")
url = urlparse(database_url)

# 创建连接池
connection_pool = psycopg2.pool.SimpleConnectionPool(
    10,  # 最小连接数
    100,  # 最大连接数
    host=url.hostname,
    user=url.username,
    password=url.password,
    database=url.path[1:],
)


def executeBatch(tuples_to_insert):
    conn = connection_pool.getconn()
    try:
        # 使用连接...
        cursor = conn.cursor()
        # 执行数据库操作...
        cursor.executemany(
            "INSERT INTO vsearch (gizmo_id, embedding) VALUES (%s, %s) ON CONFLICT DO NOTHING",
            tuples_to_insert
        )

        cursor.close()
        conn.commit()
        print(f"Inserted {cursor.rowcount} rows")
    except Exception as e:
        print("An error occurred:", e)
        conn.rollback()  # 回滚事务以撤销任何部分执行的操作
    finally:
        # 将连接返回到连接池
        connection_pool.putconn(conn)


def search_similar_vectors(query_vector, limit=5):
    conn = connection_pool.getconn()

    """在数据库中搜索与 query_vector 最相似的向量，并返回 top-N 结果的 id"""
    # 示例 SQL 语句，根据你的具体数据库结构和相似度计算方式进行调整
    sql = """
    SELECT id, gizmo_id, 
           sqrt(sum(pow(vector[i] - query_vector[i], 2))) as distance
    FROM gpt_data, 
         unnest(vector) with ordinality as v1(vector, i), 
         unnest(%s) with ordinality as v2(query_vector, i) 
    WHERE v1.i = v2.i
    GROUP BY id, gpt_id
    ORDER BY distance
    LIMIT %s;
    """
    try:
        # 使用连接...
        cursor = conn.cursor()
        cursor.execute(sql, (query_vector, limit))
        return cursor.fetchall()
    except Exception as e:
        print("An error occurred:", e)
    finally:
        # 将连接返回到连接池
        connection_pool.putconn(conn)


def initDataBaseForNormalDataV2(data):
    conn = connection_pool.getconn()
    cursor = conn.cursor()
    gpts_data = []
    for item in data:
        gizmo = item['data']['gizmo']
        author = gizmo['author']
        # 构造每条记录的数据
        record = (
            gizmo['id'],  # 假设 gizmo 的 id 是 uuid
            gizmo['organization_id'],
            gizmo['display']['name'],
            gizmo['display']['description'],
            gizmo['display']['profile_picture_url'],
            gizmo['short_url'],
            author['user_id'],
            author['display_name'],
            item['created_at'],  # 确保这个字段存在于你的数据中
            gizmo['updated_at'],
            json.dumps(item),  # 整个 item 对象作为详情
            0  # index_updated_at 的默认值
        )
        gpts_data.append(record)

    def batch_insert(cursor, data, batch_size=100):
        # 分批处理数据
        for i in range(0, len(data), batch_size):
            try:
                batch = data[i:i + batch_size]
                execute_values(cursor,
                               "INSERT INTO gpts (uuid, org_id, name, description, avatar_url, short_url, author_id, author_name, created_at, updated_at, detail, index_updated_at) VALUES %s ON CONFLICT (uuid) DO NOTHING",
                               batch)
                conn.commit()
                print("finish batch one")
            except psycopg2.Error as e:
                print(f"Database error during batch insert: {e}")
                conn.rollback()

    # 插入数据
    batch_insert(cursor, gpts_data)


def initDataBaseForNormalData(data):
    conn = connection_pool.getconn()
    cursor = conn.cursor()
    gizmos_data = []
    authors_data = []
    voices_data = []
    displays_data = []
    tags_data = []
    tools_data = []
    product_features_data = []

    def batch_insert():
        try:
            if gizmos_data:
                execute_values(cursor,
                               "INSERT INTO gizmos (id, organization_id, short_url, workspace_id, model, instructions, settings, share_recipient, updated_at, last_interacted_at, version, live_version, training_disabled, allowed_sharing_recipients, review_info, appeal_info, vanity_metrics) VALUES %s ON CONFLICT DO NOTHING",
                               gizmos_data)
            if authors_data:
                execute_values(cursor,
                               "INSERT INTO authors (user_id, display_name, link_to, selected_display, is_verified, gizmo_id) VALUES %s ON CONFLICT DO NOTHING",
                               authors_data)
            if voices_data:
                execute_values(cursor, "INSERT INTO voices (voice_id, gizmo_id) VALUES %s ON CONFLICT DO NOTHING", voices_data)
            if displays_data:
                execute_values(cursor,
                               "INSERT INTO displays (name, description, welcome_message, profile_picture_url, categories, gizmo_id) VALUES %s ON CONFLICT DO NOTHING",
                               displays_data)
            if tags_data:
                execute_values(cursor, "INSERT INTO tags (tag, gizmo_id) VALUES %s ON CONFLICT DO NOTHING", tags_data)
            if tools_data:
                execute_values(cursor,
                               "INSERT INTO tools (tool_id, type, settings, metadata, gizmo_id) VALUES %s ON CONFLICT DO NOTHING",
                               tools_data)
            if product_features_data:
                execute_values(cursor,
                               "INSERT INTO product_features (attachments, gizmo_id) VALUES %s ON CONFLICT DO NOTHING",
                               product_features_data)
            conn.commit()
            print("finish batch one")
        except psycopg2.Error as e:
            print(f"Database error during batch insert: {e}")
            conn.rollback()

    for item in data:
        gizmo = item['data']['gizmo']

        # 准备 gizmos 数据
        gizmos_data.append((
            gizmo['id'], gizmo['organization_id'], gizmo['short_url'], gizmo['workspace_id'], gizmo['model'],
            gizmo['instructions'], json.dumps(gizmo['settings']), gizmo['share_recipient'], gizmo['updated_at'],
            gizmo['last_interacted_at'], gizmo['version'], gizmo['live_version'], gizmo['training_disabled'],
            json.dumps(gizmo['allowed_sharing_recipients']), json.dumps(gizmo['review_info']),
            json.dumps(gizmo['appeal_info']), json.dumps(gizmo['vanity_metrics'])
        ))

        # 准备 authors 数据
        author = gizmo['author']
        authors_data.append((
            author['user_id'], author['display_name'], author.get('link_to', ''), author.get('selected_display', ''),
            author.get('is_verified', False), gizmo['id']
        ))

        # 准备 voices 数据
        voice = gizmo.get('voice', {'id': None})
        if voice['id']:
            voices_data.append((voice['id'], gizmo['id']))

        # 准备 displays 数据
        display = gizmo['display']
        displays_data.append((
            display['name'], display['description'], display['welcome_message'],
            display['profile_picture_url'], json.dumps(display['categories']), gizmo['id']
        ))

        # 准备 tags 数据
        for tag in gizmo['tags']:
            tags_data.append((tag, gizmo['id']))

        # 准备 tools 数据
        for tool in item['data']['tools']:
            tools_data.append((tool['id'], tool['type'], json.dumps(tool.get('settings', {})), json.dumps(tool.get('metadata', {})), gizmo['id']))

        # 准备 product_features 数据
        product_features = item['data']['product_features']
        product_features_data.append((json.dumps(product_features['attachments']), gizmo['id']))

        # 每当累积到 batch_size 条数据时，执行一次批量插入
        if len(gizmos_data) >= 100:
            batch_insert()
            # 清空累积的数据
            gizmos_data.clear()
            authors_data.clear()
            voices_data.clear()
            displays_data.clear()
            tags_data.clear()
            tools_data.clear()
            product_features_data.clear()


    # 插入剩余的数据
    batch_insert()
    cursor.close()
    connection_pool.putconn(conn)