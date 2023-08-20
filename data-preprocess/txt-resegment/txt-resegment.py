import os
import re

def clean_text(text):
    a = text.replace(' ', '')  # Remove all spaces
    a = a.replace('　　', '')
    a = a.replace('　', '')
    text = a.replace('\n', '')
    text = re.sub(r'\。”', '。', text)
    text = re.sub(r'\。', '。\n', text)
    return text

def clear_directory(dir_path):
    """删除目录内的所有文件和子目录"""
    for root, dirs, files in os.walk(dir_path, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))

def reorganize_sentences(text, min_length=200, max_length=450):
    sentences = text.split('\n')
    new_paragraphs = []
    current_paragraph = []
    current_length = 0

    for sentence in sentences:
        if current_length + len(sentence) > max_length:
            new_paragraphs.append(''.join(current_paragraph))
            current_paragraph = []
            current_length = 0
        current_paragraph.append(sentence)
        current_length += len(sentence)

        # 如果累积的句子长度不足min_length，继续添加
        while current_length < min_length:
            try:
                next_sentence = sentences.pop(0)
                current_paragraph.append(next_sentence)
                current_length += len(next_sentence)
            except IndexError:  # 如果句子用完了，跳出循环
                break

    # 添加剩下的句子
    if current_paragraph:
        new_paragraphs.append(''.join(current_paragraph))
    return '\n'.join(new_paragraphs)

def process_txt_files(input_path):
    # 创建或清空输出目录
    output_path = "../../data-final/all"
    if os.path.exists(output_path):
        clear_directory(output_path)
    else:
        os.makedirs(output_path)

    # ... 其他部分与之前相同 ...

    # 遍历文件夹中的所有txt文件
    for root, _, files in os.walk(input_path):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    cleaned_content = clean_text(content)
                    processed_content = reorganize_sentences(cleaned_content)

                # 保存到新的目录
                save_path = os.path.join(output_path, file)
                with open(save_path, 'w', encoding='utf-8') as f:
                    f.write(processed_content)

# 调用函数处理
process_txt_files("../../data-origin/挑战杯复审用数据集T20230804/数据集")
