import  json
with open("your_output_file3.txt", "r", encoding="utf-8") as review_file:
    review_samples = review_file.readlines()
def split_sentence_v2(sentence):
    """Split the sentence based on the middle punctuation mark."""
    punctuation_marks = ['，', '；', '、']

    # Find all positions of punctuation marks
    positions = [i for i, char in enumerate(sentence) if char in punctuation_marks]

    # If there are punctuation marks, choose the middle one as the split point
    if positions:
        split_position = positions[len(positions) // 2] + 1  # +1 to include the punctuation mark in the truncated part
    else:
        split_position = len(sentence) // 2

    return sentence[:split_position], sentence[split_position:]


# Process the review samples again
processed_data_v2 = []
for sentence in review_samples:
    truncated, supplement = split_sentence_v2(sentence.strip())
    entry = {
        "original_sentence": sentence.strip(),
        "truncated_sentence": truncated,
        "supplement_sentence": supplement
    }
    processed_data_v2.append(entry)

# Save the processed data to JSON format
output_path_v2 = "processed_reviews_v2.json"
with open(output_path_v2, "w", encoding="utf-8") as json_file:
    json.dump(processed_data_v2, json_file, ensure_ascii=False, indent=4)


