import os
import glob
import docx2txt

# 指定要转换的文件夹路径
input_folder = './数据集/挑战杯数据T20230308/news'

# 指定要保存转换后文件的文件夹路径
output_folder = './new-news/news-docx/'

# 获取所有.docx文件的路径
docx_files = glob.glob(os.path.join(input_folder, '*.docx'))

# 遍历所有.docx文件，将其转换为txt文件并保存到指定的输出文件夹
for docx_file in docx_files:
    # 获取文件名（不包含扩展名）
    file_name = os.path.splitext(os.path.basename(docx_file))[0]
    # 拼接输出文件路径
    output_file = os.path.join(output_folder, file_name + '.txt')
    # 转换文件并保存到输出文件夹
    with open(output_file, 'w',encoding='utf-8') as f:
        f.write(docx2txt.process(docx_file))