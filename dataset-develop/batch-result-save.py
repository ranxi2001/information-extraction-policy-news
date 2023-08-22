import requests

def three_relation_list(algo_output):
    """
    从算法输出结果中提取三元关系列表
    """
    relation_list = []
    for record in algo_output:
        for entity_category, entities in record.items():
            if isinstance(entities, list):  # 确保 entities 是一个列表
                for entity in entities:
                    if 'relations' in entity:
                        for relation_type, related_entities in entity['relations'].items():
                            for related_entity in related_entities:
                                # 直接构造所需的字符串格式
                                relation = f"[{entity['text'].strip()},{relation_type.strip()},{related_entity['text'].strip()}]"
                                relation_list.append(relation)
    return relation_list

# Step 1: 读取输入文件
input_filename = "long_sentences.txt"
output_filename = "long_output.txt"

# Step 2: 对每一行文本发送HTTP请求到后端API
with open(input_filename, 'r', encoding='utf-8') as infile:
    lines = infile.readlines()

# 获取总行数
total_lines = len(lines)

# 使用 'a' 以追加模式打开文件
with open(output_filename, 'a', encoding='utf-8') as outfile:
    # 初始化计数器
    current_line_number = 0

    for line in lines:
        current_line_number += 1  # 更新计数器
        print(f"Processing line {current_line_number} of {total_lines}")  # 打印进度

        line = line.strip()  # 去掉每行的前后空白
        if not line:  # 跳过空行
            continue

        # 发送POST请求到后端API
        response = requests.post('http://127.0.0.1:88', json={'text': line})

        # Step 3: 将每一次请求的结果保存到输出文件中
        if response.status_code == 200:
            result = response.json()
            outfile.write(line + '\n')
            outfile.write(str(result) + '\n')

            # 提取三元关系列表，并保存到文件第三行
            relations = three_relation_list(result)
            # 使用逗号连接所有关系并写入文件，同时添加外层的括号
            outfile.write('[' + ','.join(relations) + ']' + '\n')
        else:
            print(f"Failed to process line {current_line_number}. Status code: {response.status_code}")
