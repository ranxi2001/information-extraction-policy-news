# Recompute the plain text representation
def ner_to_text(output_list, text):
    """
    Convert NER output to plain text representation.

    Parameters:
    - output_list: The structured NER output list.
    - text: The original text.

    Returns:
    - Text representation of the NER output.
    """
    # Flatten entities from the list
    entities = []
    for output in output_list:
        for entity_type, entity_list in output.items():
            for entity in entity_list:
                entities.append({
                    'type': entity_type,
                    'start': entity['start'],
                    'end': entity['end'],
                    'text': entity['text'],
                    'probability': entity['probability'],
                    'relations': entity.get('relations', {})
                })

    # Sort entities based on their start position
    entities = sorted(entities, key=lambda x: x['start'])

    # Generate the text representation
    text_parts = []
    last_end = 0
    for entity in entities:
        # Add the text before the entity
        text_parts.append(text[last_end:entity['start']])
        # Add the entity with [type] prefix
        text_parts.append(f"[{entity['type']}] {entity['text']} ({entity['probability']:.2f})")
        last_end = entity['end']
    # Add the remaining text
    text_parts.append(text[last_end:])

    return ''.join(text_parts)


# Recompute the plain text representation
text_representation = ner_to_text(output_list=[
    {'人名': [{'end': 20,
             'probability': 0.9998250081677469,
             'relations': {'身份': [{'end': 17,
                                   'probability': 0.9958833689313842,
                                   'start': 11,
                                   'text': '民革中央主席'}]},
             'start': 17,
             'text': '万鄂湘'}],
     '人的代称': [{'end': 17,
               'probability': 0.9854348625920579,
               'start': 11,
               'text': '民革中央主席'}]}], text="民革中央主席万鄂湘...")

print(text_representation)
