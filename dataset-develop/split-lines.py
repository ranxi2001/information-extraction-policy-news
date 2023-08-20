def split_lines(input_path, output_path, min_length=250, split_length=450):
    with open(input_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    new_lines = []

    for line in lines:
        line = line.strip()  # 删除前后的空白字符
        # 如果行的长度小于min_length，直接跳过
        if len(line) < min_length:
            continue

        # 检查指定位置前的最后一个有效符号，如果行的长度大于split_length则在split_length位置进行检查
        check_length = min(len(line), split_length)
        last_valid_idx = max(line.rfind('。', 0, check_length),
                             line.rfind('》', 0, check_length),
                             line.rfind('）', 0, check_length))

        # 如果找到了有效的符号，只保留到该符号的部分
        if last_valid_idx != -1:
            line = line[:last_valid_idx + 1]
        else:  # 如果没找到有效的符号，直接截断
            line = line[:check_length]

        new_lines.append(line + "\n")

    with open(output_path, "w", encoding="utf-8") as file:
        file.writelines(new_lines)

def remove_empty_lines(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # 保留非空行
    non_empty_lines = [line for line in lines if line.strip()]

    with open(output_path, "w", encoding="utf-8") as file:
        file.writelines(non_empty_lines)

input_path = "input.txt"
output_path = "input.txt"
split_lines(input_path, output_path)
remove_empty_lines(input_path, output_path)
