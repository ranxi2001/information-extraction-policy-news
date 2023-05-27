import os
import random
import shutil

# set the paths of the three folders
folder1_path = '../data-preprocessed/new-news/news-docx'
folder2_path = '../data-preprocessed/new-news/news-pdf'
folder3_path = '../data-preprocessed/new-news/news-wps'

# create a list of all txt files in the three folders
txt_files = []
for folder_path in [folder1_path, folder2_path, folder3_path]:
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.txt'):
            txt_files.append(os.path.join(folder_path, file_name))

# randomly select 34 txt files and move them to a new folder
random_files = random.sample(txt_files, 100)
new_folder_path = '../data-final/news/train'
os.makedirs(new_folder_path, exist_ok=True)
for file_path in random_files:
    shutil.copy(file_path, new_folder_path)

# move the remaining files to another folder
remaining_files = set(txt_files) - set(random_files)
other_folder_path = '../data-final/news/test'
os.makedirs(other_folder_path, exist_ok=True)
for file_path in remaining_files:
    shutil.copy(file_path, other_folder_path)
