def process_line(line):
    # If the line is just "[]", return it as is
    if line.strip() == "[[]]":
        return line

    # Split the line by the outer brackets to get the inner lists
    inner_lists = line[2:-2].split('],[')

    # Process each inner list
    processed_lists = []
    for inner_list in inner_lists:
        items = inner_list.split(',')
        items = [
            f'“{item.strip().replace("“", "").replace("”", "").replace("]", "")}”' if item.strip() and item.strip() != '“”' else None for
            item in items]
        items = list(filter(None, items))
        if items:
            processed_list = '[' + ', '.join(items) + ']'
            processed_lists.append(processed_list)

    # Remove empty or invalid lists
    processed_lists = [lst for lst in processed_lists if lst != '[]' and lst != '[“”, “]”]']\



    return '[' + ', '.join(processed_lists) + ']\n'

# 打开文本文件
with open('output.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

# 处理每三行
for i in range(2, len(lines), 3):
    lines[i] = process_line(lines[i]).replace("“", '"').replace("”", '"')

# 将处理后的行写回文件
with open('output_modified.txt', 'w', encoding='utf-8') as file:
    file.writelines(lines)

