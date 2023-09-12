import jieba
import jieba.posseg as pseg
import re

# 读取源文件内容
with open("your_output_file3.txt", "r", encoding="utf-8") as file:
    content = file.read()

# 使用jieba进行词性标注
words_pos = pseg.cut(content)

# 过滤结果
filtered_words = set()  # 使用集合以去重
for word, flag in words_pos:
    if len(word) > 1 and not re.search(r"\d|[\W_]+", word) and 'n' in flag:
        filtered_words.add(word)

# 保存结果到userdict.txt文件
with open("userdict.txt", "w", encoding="utf-8") as file:
    for word in filtered_words:
        file.write(word + "\n")

print("分词完成，结果已保存到userdict.txt文件中。")
