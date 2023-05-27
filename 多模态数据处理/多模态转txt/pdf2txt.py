import os
import PyPDF2

# specify the folder path containing the PDF files
input_path = "../../data-origin/挑战杯数据T20230308/news"
output_path = "../../data-preprocessed/new-news/news-pdf"
# loop through all files in the folder
for filename in os.listdir(input_path):
    if filename.endswith(".pdf"):
        # open the PDF file
        with open(os.path.join(input_path, filename), "rb") as pdf_file:
            # create a PDF reader object
            pdf_reader = PyPDF2.PdfFileReader(pdf_file)
            # create a string to hold the text from the PDF
            text = ""
            # loop through each page in the PDF
            for page_num in range(pdf_reader.getNumPages()):
                # extract the text from the page
                page = pdf_reader.getPage(page_num)
                text += page.extractText()
            # create a new file with the same name as the PDF but with a .txt extension
            with open(os.path.join(output_path, filename[:-4] + ".txt"), "w", encoding="utf-8") as txt_file:
                # write the text to the new file
                txt_file.write(text)