def truncate_line(line):
    # 如果行的长度超过512字符
    if len(line) > 200:
        # 截取前512个字符
        truncated_line = line[:200]
        # 查找最后一个句号的位置
        last_dot_position = truncated_line.rfind(".")
        # 如果找到句号，根据句号位置截取
        if last_dot_position != -1:
            return truncated_line[:last_dot_position + 1]
        else:
            return truncated_line
    return line

def process_file(input_filename, output_filename):
    with open(input_filename, 'r', encoding='utf-8') as infile, open(output_filename, 'w', encoding='utf-8') as outfile:
        for line in infile:
            truncated = truncate_line(line.strip())
            if truncated:  # 确保行不为空
                outfile.write(truncated + "\n")

# 使用方法
input_filename = "select-all.txt"
output_filename = "your_output_file2.txt"
process_file(input_filename, output_filename)
