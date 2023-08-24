import json
import tqdm
from pprint import pprint
from paddlenlp import Taskflow
from pypinyin import pinyin, lazy_pinyin, Style

# 预处理的列表
pr_out = []
# 对应的拼音属性等字典列表
dir_c_out = []
def read_and_group_lines(filename):
    grouped_lines = []
    with open(filename, 'r', encoding='utf-8') as file:  # 使用 utf-8 编码打开文件
        lines = file.readlines()
        group = []
        for line in lines:
            group.append(line.strip())
            if len(group) == 3:
                grouped_lines.append(group)
                group = []
        if group:
            grouped_lines.append(group)
    return grouped_lines


filename = 'output_modified12.txt'  # 替换为你的文件名
grouped_data = read_and_group_lines(filename)

# # 测试三元组的识别
# for i in tqdm.tqdm(range(len(grouped_data))):
#     re_list = []
#     print(grouped_data[i][2])
#     grouped_data_re = eval(grouped_data[i][2])

# text_all是所有实体的名字
# probability_all是所有实体的识别概率
# start_all是实体的开始位置
# end_all=是实体的结束位置
# category_all是实体的属性
text_all = []
probability_all = []
start_all = []
end_all = []
category_all = []
# 读入实体识别的信息
for i in tqdm.tqdm(range(len(grouped_data))):
    data_string = grouped_data[i][1]
    # 将str的数据中的连续单引号导致的双引号删除
    data_string = data_string.replace('"', '')
    # 将str的数据中的单引号变成双引号，便于json文件的读取
    data_str = data_string.replace("'", "\"")
    # print(data_str)
    data = json.loads(data_str)
    text_list = []
    probability_list = []
    start_list = []
    end_list = []
    category_list = []

    # 以类别为键，提取实体信息
    for category, entities in data[0].items():
        # print(f"Category: {category}")
        for entity in entities:
            text = entity['text']
            probability = entity['probability']
            start = entity['start']
            end = entity['end']
            text_list.append(text)
            probability_list.append(probability)
            start_list.append(start)
            end_list.append(end)
            category_list.append(category)
            # print(f"Text: {text}, Probability: {probability}, Start: {start}, End: {end}")

    text_all.append(text_list)
    probability_all.append(probability_list)
    start_all.append(start_list)
    end_all.append(end_list)
    category_all.append(category_list)

pr_out.append(start_all)
pr_out.append(end_all)
# _____________________________________part1_____________________________________实体拼音
LAC = []

for i in tqdm.tqdm(range(len(text_all))):
    lac = []
    for j in range(len(text_all[i])):
        lac.append(pinyin(text_all[i][j], style=Style.TONE3, neutral_tone_with_five=True))
        # print(pinyin(text_all[i][j], style=Style.TONE3, neutral_tone_with_five=True))
    LAC.append(lac)
# print(LAC[0][-1])  # 拼音结果

# 创建一个空字典来存储元素到编码的映射
element_to_code = {'NA': 0}

# 生成编码后的数据和编码字典
current_code = 1
encoded_data = []

data = LAC
for dim1 in data:
    encoded_dim1 = []
    for dim2 in dim1:
        encoded_dim2 = []
        for dim3 in dim2:
            encoded_dim3 = []
            for element in dim3:
                if element not in element_to_code:
                    element_to_code[element] = current_code
                    current_code += 1
                encoded_dim3.append(element_to_code[element])
            encoded_dim2.append(encoded_dim3)
        encoded_dim1.append(encoded_dim2)
    encoded_data.append(encoded_dim1)

# 输出编码后的数据和编码字典
# print("原始数据:", data)
# print("编码后的数据:", encoded_data)
# print("编码字典:", element_to_code)
pr_out.append(encoded_data)
dir_c_out.append(element_to_code)
# 将字典保存到文件
with open("siti_pinyin.json", "w") as f:
    json.dump(element_to_code, f)
# # 从文件加载字典
# with open("siti_pinyin.json", "r") as f:
#     loaded_data = json.load(f)
#
# print("加载的字典:", loaded_data)
# _____________________________________part2_____________________________________实体属性
data = category_all
# 创建一个空字典来存储元素到编码的映射
element_to_code = {'NA': 0}

# 生成编码后的数据和编码字典
current_code = 1
encoded_data = []

for sample in data:
    encoded_sample = []
    for element in sample:
        if element not in element_to_code:
            element_to_code[element] = current_code
            current_code += 1
        encoded_sample.append(element_to_code[element])
    encoded_data.append(encoded_sample)

# 输出编码后的数据和编码字典
# print("原始数据:", data)
# print("编码后的数据:", encoded_data)
# print("编码字典:", element_to_code)
pr_out.append(encoded_data)
dir_c_out.append(element_to_code)
# 将字典保存到文件
with open("siti_shuxin.json", "w") as f:
    json.dump(element_to_code, f)
# _____________________________________part3_____________________________________原句拼音
data_yuju = []
# 识别初始的语句
for i in tqdm.tqdm(range(len(grouped_data))):
    data_yuju_list = []
    data_orgian = grouped_data[i][0]
    data_yuju_list.append(pinyin(data_orgian, style=Style.TONE3, neutral_tone_with_five=True))
    data_yuju.append(data_yuju_list)

# 创建一个空字典来存储元素到编码的映射
element_to_code = {'NA': 0}

# 生成编码后的数据和编码字典
current_code = 1
encoded_data = []

data = data_yuju
for dim1 in data:
    encoded_dim1 = []
    for dim2 in dim1:
        encoded_dim2 = []
        for dim3 in dim2:
            encoded_dim3 = []
            for element in dim3:
                if element not in element_to_code:
                    element_to_code[element] = current_code
                    current_code += 1
                encoded_dim3.append(element_to_code[element])
            encoded_dim2.append(encoded_dim3)
        encoded_dim1.append(encoded_dim2)
    encoded_data.append(encoded_dim1)

# 输出编码后的数据和编码字典
# print("原始数据:", data)
# print("编码后的数据:", encoded_data)
# print("编码字典:", element_to_code)
pr_out.append(encoded_data)
dir_c_out.append(element_to_code)
# 将字典保存到文件
with open("yuanju_pinyin.json", "w") as f:
    json.dump(element_to_code, f)
# _____________________________________part4_____________________________________关系拼音
re = []
for i in tqdm.tqdm(range(len(grouped_data))):
    re_list = []
    grouped_data_re = eval(grouped_data[i][2])
    for j in range(len(grouped_data_re)):
        re_list.append(pinyin(grouped_data_re[j][1], style=Style.TONE3, neutral_tone_with_five=True))
    re.append(re_list)

# 创建一个空字典来存储元素到编码的映射
element_to_code = {'NA': 0}

# 生成编码后的数据和编码字典
current_code = 1
encoded_data = []

data = re
for dim1 in data:
    encoded_dim1 = []
    for dim2 in dim1:
        encoded_dim2 = []
        for dim3 in dim2:
            encoded_dim3 = []
            for element in dim3:
                if element not in element_to_code:
                    element_to_code[element] = current_code
                    current_code += 1
                encoded_dim3.append(element_to_code[element])
            encoded_dim2.append(encoded_dim3)
        encoded_dim1.append(encoded_dim2)
    encoded_data.append(encoded_dim1)

# 输出编码后的数据和编码字典
# print("原始数据:", data)
# print("编码后的数据:", encoded_data)
# print("编码字典:", element_to_code)
pr_out.append(encoded_data)
dir_c_out.append(element_to_code)
# 将字典保存到文件
with open("guanx_pinyin.json", "w") as f:
    json.dump(element_to_code, f)
# _____________________________________part5_____________________________________关系属性
re_entity = []
for i in tqdm.tqdm(range(len(grouped_data))):
    re_entity_list = []
    grouped_data_re = eval(grouped_data[i][2])
    for j in range(len(grouped_data_re)):
        re_entity_list.append(grouped_data_re[j][1])
    re_entity.append(re_entity_list)

# 创建一个空字典来存储元素到编码的映射
element_to_code = {'NA': 0}

# 生成编码后的数据和编码字典
current_code = 1
encoded_data = []

data = re_entity
for dim1 in data:
    encoded_dim1 = []
    for element in dim1:
        if element not in element_to_code:
            element_to_code[element] = current_code
            current_code += 1
        encoded_dim1.append(element_to_code[element])
    encoded_data.append(encoded_dim1)

# 输出编码后的数据和编码字典
# print("原始数据:", data)
# print("编码后的数据:", encoded_data)
# print("编码字典:", element_to_code)
pr_out.append(encoded_data)
dir_c_out.append(element_to_code)
# 将字典保存到文件
with open("guanxi_shuxin.json", "w") as f:
    json.dump(element_to_code, f)

# ________________________________________________________________

# start、end、实体或者关系属性编码、拼音编码、              语句编码，
# 最终获得每个三元组，作为x，标签都是1，后续打乱构建负样本
# 每个三元组变成【头实体的属性编码，头实体的拼音编码，       这里直接去字典里查询
# 尾实体的属性编码，尾实体的拼音编码，
# 关系的属性编码，关系的拼音编码，   这里直接去字典里查询
# 语句编码】   这里直接去字典里查询，这里txt的用前面保存的结果
Y_dataset = []
# 计算三元组对应的向量
for i in tqdm.tqdm(range(len(grouped_data))):
    grouped_data_re = eval(grouped_data[i][2])
    # print(grouped_data_re)
    if len(grouped_data_re) != 0:
        for j in range(len(grouped_data_re)):
                Y_dataset_list = []
                # 计算头实体的相关编码
                flag_text = None
                flag_pinyin_list = None
                for k in range(len(text_all[i])):
                    if grouped_data_re[j][0] == text_all[i][k]:
                        flag_text = category_all[i][k]
                        flag_pinyin_list = LAC[i][k]
                # 计算头实体的属性编码
                if flag_text in dir_c_out[1]:
                    Y_dataset_list.append([dir_c_out[1][flag_text]])
                else:
                    Y_dataset_list.append([0])
                # 计算头实体的拼音编码
                flag_pinyin_list_list = []
                if flag_pinyin_list != None:
                    for ii in range(len(flag_pinyin_list)):
                        if flag_pinyin_list[ii][0] in dir_c_out[0]:
                            flag_pinyin_list_list.append(dir_c_out[0][flag_pinyin_list[ii][0]])
                        else:
                            flag_pinyin_list_list.append(0)
                # 添加头实体的拼音属性
                Y_dataset_list.append(flag_pinyin_list_list)

                # 计算尾实体的相关编码
                flag_text = None
                flag_pinyin_list = None
                for k in range(len(text_all[i])):
                    if grouped_data_re[j][2] == text_all[i][k]:
                        flag_text = category_all[i][k]
                        flag_pinyin_list = LAC[i][k]
                # 计算尾实体的属性编码
                if flag_text in dir_c_out[1]:
                    Y_dataset_list.append([dir_c_out[1][flag_text]])
                else:
                    Y_dataset_list.append([0])
                # 计算尾实体的拼音编码
                flag_pinyin_list_list = []
                if flag_pinyin_list != None:
                    for iii in range(len(flag_pinyin_list)):
                        if flag_pinyin_list[iii][0] in dir_c_out[0]:
                            flag_pinyin_list_list.append(dir_c_out[0][flag_pinyin_list[iii][0]])
                        else:
                            flag_pinyin_list_list.append(0)
                # 添加尾实体的属性
                Y_dataset_list.append(flag_pinyin_list_list)

                # 计算关系的属性编码并添加
                if grouped_data_re[j][1] in dir_c_out[4]:
                    Y_dataset_list.append([dir_c_out[4][grouped_data_re[j][1]]])
                else:
                    Y_dataset_list.append([0])

                # 原句的拼音编码
                yuanju_list = []
                for p1 in range(len(pr_out[4][i])):
                    for p2 in range(len(pr_out[4][i][p1])):
                        for p3 in range(len(pr_out[4][i][p1][p2])):
                            yuanju_list.append(pr_out[4][i][p1][p2][p3])
                Y_dataset_list.append(yuanju_list)
                # 所有的特征得到的样本集
                Y_dataset.append(Y_dataset_list)

# print(Y_dataset)

# 构建的数据保存到文件
with open('X_data.json', 'w') as file:
    json.dump(Y_dataset, file)