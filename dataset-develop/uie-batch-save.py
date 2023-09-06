import requests
# Step 1: 读取输入文件
input_filename = "long_sentences.txt"
output_filename = "long_output.txt"
# Step 2: 对每一行文本发送HTTP请求到后端API
with open(input_filename, 'r', encoding='utf-8') as infile:
    lines = infile.readlines()

# 获取总行数
total_lines = len(lines)
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

        else:
            print(f"Failed to process line {current_line_number}. Status code: {response.status_code}")