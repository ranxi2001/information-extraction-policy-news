def truncate_line(line):
    # 查找最后一个句号的位置
    last_dot_position = line.rfind("。")
    # 如果找到句号，根据句号位置截取
    if last_dot_position != -1:
        truncated = line[:last_dot_position + 1]
        # 检查截断后的行是否至少有30个字符
        if len(truncated) >= 30:
            return truncated
    return None  # 如果没有句号，或者截断后的行少于30个字符，则不返回任何内容

def process_file(input_filename, output_filename):
    with open(input_filename, 'r', encoding='utf-8') as infile, open(output_filename, 'w', encoding='utf-8') as outfile:
        for line in infile:
            truncated = truncate_line(line.strip())
            if truncated:  # 确保行不为空
                outfile.write(truncated + "\n")

# 使用方法
input_filename = "your_output_file2.txt"
output_filename = "your_output_file3.txt"
process_file(input_filename, output_filename)
