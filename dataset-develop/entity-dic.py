# 打开output.txt进行读取
with open('output.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

# 提取每隔2行的实体信息
entities_set = set()  # 使用集合来避免重复实体
for idx, line in enumerate(lines):
    # idx从0开始，所以取余数为1的行是我们需要的实体标注行
    if idx % 3 == 1:
        # 从文本中解析Python列表结构
        entity_list_outer = eval(line.strip())
        for entity_dict in entity_list_outer:
            # 遍历每种类型的实体，提取实体文本并加入集合
            for entity_type, entity_list in entity_dict.items():
                for entity_info in entity_list:
                    entities_set.add(entity_info['text'])

# 将实体信息写入entity_dic.txt
with open('entity_dic.txt', 'w', encoding='utf-8') as file:
    for entity in sorted(entities_set):  # 可以对实体进行排序，也可以直接写入
        file.write(entity + '\n')
