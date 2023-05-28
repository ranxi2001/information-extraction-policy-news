import os
import random
import shutil

# set paths
source_path = "../../data-preprocessed/new-policy"
train_path = "../../data-final/policy/train"
test_path = "../../data-final/policy/test"

# create train and test folders if they don't exist
if not os.path.exists(train_path):
    os.makedirs(train_path)
if not os.path.exists(test_path):
    os.makedirs(test_path)

# get all txt files in source folder
txt_files = [f for f in os.listdir(source_path) if f.endswith('.txt')]

# shuffle the list of txt files
random.shuffle(txt_files)

# move first 100 files to train folder, rest to test folder
for i, file in enumerate(txt_files):
    if i < 100:
        shutil.move(os.path.join(source_path, file), os.path.join(train_path, file))
    else:
        shutil.move(os.path.join(source_path, file), os.path.join(test_path, file))
