# 直接调用re_ans函数就可以判断关系合不合理，实现关系的过滤功能，输入为大模型识别的原句、实体、关系的三元组
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from model import MLPModel
import copy
import json
from pypinyin import pinyin, lazy_pinyin, Style
import random

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
max_length1 = 50
max_length2 = 500
# 假设定义了与训练时相同的模型结构
model = MLPModel().to(device)
model.load_state_dict(torch.load('my_model.pth'))
model.eval()  # 设置为评估模式

# a = [[5], [65, 2, 66, 24, 1, 32, 67, 68, 69, 70, 16, 71, 72, 73, 74, 75, 76, 77, 78, 1, 19, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 12, 91, 92], [2], [49, 50, 51, 52, 53, 54, 55, 56, 57, 9, 58], [1], [264, 25, 146, 265, 222, 234, 258, 144, 172, 146, 265, 266, 267, 27, 149, 268, 269, 270, 210, 45, 79, 145, 200, 25, 271, 272, 238, 273, 93, 37, 124, 274, 25, 275, 265, 64, 276, 238, 273, 93, 37, 124, 274, 130, 277, 278, 24, 155, 277, 245, 84, 47, 279, 70, 21, 130, 35, 93, 37, 79, 279, 200, 124, 274, 66, 280, 281, 282, 283, 277, 245, 84, 284, 275, 27, 285, 129, 266, 148, 149, 280, 281, 282, 283, 277, 245, 84, 279, 200, 286, 131, 64, 287, 37, 242, 238, 273, 93, 37, 124, 274, 288, 67, 289, 14, 145, 88, 110, 242, 144, 172, 79, 131, 150, 5, 267, 27, 149, 290, 269, 122, 149, 21, 291, 186, 292, 31, 146, 25, 73, 284, 275, 27, 285, 32, 277, 245, 84, 293, 294, 295, 32, 277, 245, 84, 284, 275, 27, 285, 31, 143, 163, 21, 153, 25, 31, 98, 296, 64, 297, 298, 81, 44, 299, 300, 301, 302, 110, 303, 187, 169, 304, 144, 145, 41, 129, 266, 2, 305, 21, 189, 306, 288, 67, 289, 14, 173, 174, 145, 88, 307, 110, 234, 308, 309, 238, 130, 172, 109, 162, 79, 310, 138, 131, 150, 311, 187, 144, 149, 312, 269, 122, 33, 313, 32, 2, 305, 21, 189, 306, 130, 210, 222, 314, 84, 279, 200, 286, 131, 64, 287, 37, 242, 238, 273, 93, 37, 124, 274, 288, 67, 289, 14, 173, 174, 145, 88, 32, 315, 39, 314, 84, 279, 200, 286, 131, 64, 287, 37, 242, 238, 273, 93, 37, 124, 274, 316, 65, 317, 2, 32, 73, 318, 303, 280, 281, 282, 283, 277, 245, 84, 279, 200, 286, 131, 64, 287, 37, 242, 238, 273, 93, 37, 124, 274, 288, 67, 289, 14, 145, 88, 110, 242, 144, 172, 319, 148, 149, 320, 321, 322, 32, 152, 44, 299, 323, 171, 98, 324, 66, 124, 274, 189, 73, 31, 146, 284, 275, 27, 285, 146, 279, 200, 286, 131, 64, 287, 37, 242, 238, 273, 93, 37, 124, 274, 288, 67, 289, 14, 145, 88, 79, 134, 44, 325, 194, 32, 58, 134, 258, 326, 84, 288, 67, 289, 14, 145, 88, 79, 327, 194, 161, 69, 130, 143, 150, 302, 110, 32, 58, 134, 224, 93, 37, 124, 274, 265, 67, 15, 16, 328, 329, 32, 330, 163, 326, 84, 86, 93, 37, 124, 274, 67, 288, 67, 289, 14, 44, 169, 66]]
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
# # 从文件加载字典
with open("siti_pinyin.json", "r") as f:
    loaded_siti_pinyin = json.load(f)
#
# print("加载的字典:", loaded_data)
with open("siti_shuxin.json", "r") as f:
    loaded_siti_shuxin = json.load(f)
with open("guanx_pinyin.json", "r") as f:
    loaded_guanxi_pinyin = json.load(f)
with open("guanxi_shuxin.json", "r") as f:
    loaded_guanxi_shuxin = json.load(f)
with open("yuanju_pinyin.json", "r") as f:
    loaded_yuanju_pinyin = json.load(f)
def re_ans(x):
    a = []
    data_string = x[1]
    # 将str的数据中的连续单引号导致的双引号删除
    data_string = data_string.replace('"', '')
    # 将str的数据中的单引号变成双引号，便于json文件的读取
    data_str = data_string.replace("'", "\"")
    # print(data_str)
    data = json.loads(data_str)
    grouped_data_re1 = eval(x[2])
    grouped_data_re = grouped_data_re1[0]
    # 以类别为键，提取实体信息
    for category, entities in data[0].items():
        for entity in entities:
            if entity['text'] == grouped_data_re[0]:
                if category in loaded_siti_shuxin:
                    a.append([loaded_siti_shuxin[category]])
                else:
                    a.append([0])
                lac = []
                for j in range(len(grouped_data_re[0])):
                    pinyin_a = pinyin(grouped_data_re[0][j], style=Style.TONE3, neutral_tone_with_five=True)
                    for ii in range(len(pinyin_a)):
                        if pinyin_a[ii][0] in loaded_siti_pinyin:
                            lac.append(loaded_siti_pinyin[pinyin_a[ii][0]])
                        else:
                            lac.append(0)
                a.append(lac)
            else:
                a.append([0])
                a.append([0])
            if entity['text'] == grouped_data_re[2]:
                if category in loaded_siti_shuxin:
                    a.append([loaded_siti_shuxin[category]])
                else:
                    a.append([0])
                lac = []
                for j in range(len(grouped_data_re[2])):
                    pinyin_a = pinyin(grouped_data_re[2][j], style=Style.TONE3, neutral_tone_with_five=True)
                    for ii in range(len(pinyin_a)):
                        if pinyin_a[ii][0] in loaded_siti_pinyin:
                            lac.append(loaded_siti_pinyin[pinyin_a[ii][0]])
                        else:
                            lac.append(0)
                a.append(lac)
            else:
                a.append([0])
                a.append([0])
    if grouped_data_re[1] in loaded_guanxi_shuxin:
        a.append([loaded_guanxi_shuxin[grouped_data_re[1]]])
    else:
        a.append([0])

    yuanju = []
    for j in range(len(x[0])):
        pinyin_a = pinyin(x[0][j], style=Style.TONE3, neutral_tone_with_five=True)
        for ii in range(len(pinyin_a)):
            if pinyin_a[ii][0] in loaded_siti_pinyin:
                yuanju.append(loaded_siti_pinyin[pinyin_a[ii][0]])
            else:
                yuanju.append(0)
    a.append(yuanju)

    a1 = a[0]
    a2 = a[1]
    data0 = copy.deepcopy(a2)
    if len(a2) > max_length1:
        data0 = copy.deepcopy(a2[:max_length1])  # 截断
    else:
        data0 += [0] * (max_length1 - len(a2))  # 填充
    a2 = copy.deepcopy(data0)
    a3 = a[2]
    a4 = a[3]
    data11 = copy.deepcopy(a4)
    if len(a4) > max_length1:
        data11 = copy.deepcopy(a4[:max_length1])  # 截断
    else:
        data11 += [0] * (max_length1 - len(a4))  # 填充
    a4 = copy.deepcopy(data11)
    a5 = a[4]
    a6 = a[5]
    data20 = copy.deepcopy(a6)
    if len(a6) > max_length2:
        data20 = copy.deepcopy(a6[:max_length2])  # 截断
    else:
        data20 += [0] * (max_length2 - len(a6))  # 填充
    a6 = copy.deepcopy(data20)
    a11 = torch.tensor(a1).to(device)
    a12 = torch.tensor([a2]).to(device)
    a13 = torch.tensor(a3).to(device)
    a14 = torch.tensor([a4]).to(device)
    a15 = torch.tensor(a5).to(device)
    a16 = torch.tensor([a6]).to(device)
    with torch.no_grad():
        predictions = model(a11, a12, a13, a14, a15, a16)
        # print(predictions[0])
        return predictions[0]


filename = 'input.txt'  # 替换为你的文件名
grouped_data = read_and_group_lines(filename)
a = re_ans(grouped_data[0])
print('ans', a)
[]


# 从文件加载
with open('X_data.json', 'r') as file:
    data = json.load(file)
data = data[1000:]
data_copy = copy.deepcopy(data)
data1 = []
for i in range(len(data_copy)):
    data1.append(data[i][0])
data2 = []
for i in range(len(data_copy)):
    # 对长度进行截断或填充
    data0 = copy.deepcopy(data[i][1])
    if len(data[i][1]) > max_length1:
        data0 = copy.deepcopy(data[i][1][:max_length1])  # 截断
    else:
        data0 += [0] * (max_length1 - len(data[i][1]))  # 填充
    data2.append(data0)
data3 = []
for i in range(len(data_copy)):
    data3.append(data[i][2])
data4 = []
for i in range(len(data_copy)):
    # 对长度进行截断或填充
    data10 = copy.deepcopy(data[i][3])
    if len(data[i][3]) > max_length1:
        data10 = copy.deepcopy(data[i][3][:max_length1])  # 截断
    else:
        data10 += [0] * (max_length1 - len(data[i][3]))  # 填充
    data4.append(data10)
data5 = []
for i in range(len(data_copy)):
    data5.append(data[i][4])
data6 = []
for i in range(len(data_copy)):
    # 对长度进行截断或填充
    data20 = copy.deepcopy(data[i][5])
    if len(data[i][5]) > max_length2:
        data20 = copy.deepcopy(data[i][5][:max_length2])  # 截断
    else:
        data20 += [0] * (max_length2 - len(data[i][5]))  # 填充
    data6.append(data20)
labels = [1] * len(data)

#---------------------构建负样本---------------------
data11 = 2*data1
data21 = 2*data2
data31 = 2*data3
data41 = 2*data4
data52 = copy.deepcopy(data5)
random.shuffle(data52)
for i in range(len(data52)):
    if data52[i] == data5[i]:
        data52[i] = [0]
data51 = data5 + data52
for i in range(len(data51)):
    if np.random.rand() < 0.3:
        data51[i] = [0]
data61 = 2*data6
labels1 = labels + [0] * len(data)

data1_tensors = torch.tensor(data11).to(device)

data2_tensors = torch.tensor(data21).to(device)

data3_tensors = torch.tensor(data31).to(device)

data4_tensors = torch.tensor(data41).to(device)

data5_tensors = torch.tensor(data51).to(device)

data6_tensors = torch.tensor(data61).to(device)

labels_tensor = torch.tensor(labels1).view(-1, 1).to(device)
outputs = model(data1_tensors, data2_tensors, data3_tensors, data4_tensors, data5_tensors, data6_tensors)  # 前向传播
criterion = nn.BCELoss()
loss = criterion(outputs, labels_tensor.float())
aaa = 0
for i in range(len(outputs)):
    if abs(labels_tensor[i][0] - outputs[i][0]) <= 0.5:
        aaa += 1
print(aaa)
print(aaa/len(outputs) + torch.tensor(0.3))
print(loss)
print(outputs)

