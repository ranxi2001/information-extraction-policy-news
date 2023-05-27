import os

# Define the function to convert .wps files to .txt files
def wps_to_txt(input_path,output_path):
    # Loop through all files in the specified folder
    for filename in os.listdir(input_path):
        # Check if the file is a .wps file
        if filename.endswith('.wps'):
            # Create the input and output file paths
            file_path = os.path.join(input_path, filename)
            newfile_path = os.path.join(output_path, filename[:-4] + '.txt')
            # Open the input and output files
            with open(file_path, 'rb') as input_file, open(newfile_path, 'w') as output_file:
                # Read the input file as bytes and decode as utf-8
                file_content = input_file.read().decode('utf-8')
                # Write the decoded content to the output file
                output_file.write(file_content)

# Call the function with the specified folder path
wps_to_txt('../../data-origin/挑战杯数据T20230308/news', 'data-preprocessed/new-news/news-wps')  # Replace '/path/to/folder' with the actual folder path