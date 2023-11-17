import json


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


# 从文件中读取 JSON 数据
with open('aTotal.json', 'r', encoding='utf-8') as input_file:
    exists = json.load(input_file)


data = []
for value in exists:
    value['category'] = nuanced_categorization(value['desp'])
    value.pop('catalog', None)  # 如果'catalog'不存在，返回None而
    data.append(value)


# 将合并后的数据写入输出文件（覆盖已存在的文件内容）
with open("aTotal.json", 'w') as output_json:
    json.dump(exists, output_json, indent=4)