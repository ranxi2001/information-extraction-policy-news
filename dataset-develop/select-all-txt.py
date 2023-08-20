import os
import random


def random_select_paragraphs(file_path, num=2):
    with open(file_path, 'r', encoding='utf-8') as f:
        paragraphs = f.readlines()
        # 如果段落数小于num，则选择所有段落
        if len(paragraphs) < num:
            return paragraphs
        # 否则随机选择num个段落
        return random.sample(paragraphs, num)


def gather_paragraphs(input_path, output_path):
    selected_paragraphs = []

    # 遍历文件夹中的所有txt文件
    for root, _, files in os.walk(input_path):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                selected_paragraphs.extend(random_select_paragraphs(file_path))

    # 创建输出目录，如果它不存在
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 将选中的段落写入汇总文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(selected_paragraphs)


# 指定输入和输出路径
input_path = "../data-final/all/"
output_path = "../data-final/review/select-all.txt"

# 调用函数
gather_paragraphs(input_path, output_path)
