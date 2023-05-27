import re
import os
def fix_ocr_errors(input_path, output_path):
    with open(input_path, 'r', encoding="gbk") as f:
        lines = f.readlines()
    text = ''.join(lines)
    a = text.replace(' ', '')  # Remove all spaces
    a = a.replace('　　', '')
    a = a.replace('　', '')
    text = a.replace('\n', '')
    text = re.sub(r'\。”', '。', text)
    text = re.sub(r'\。', '。\n', text)

    with open(output_path, 'w', encoding="utf-8") as f:
        f.write(text)

input_dir = '../../data-preprocessed/new-news/news-wps'
output_dir = '../../data-preprocessed/new-news/news-wps'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for filename in os.listdir(input_dir):
    if filename.endswith('.txt'):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)
        fix_ocr_errors(input_path, output_path)