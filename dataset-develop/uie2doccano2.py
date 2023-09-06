import json

def convert_to_doccano_format(input_filename):
    with open(input_filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    results = []

    # Assuming every three lines correspond to one data point (text, labels, and relations)
    for i in range(0, len(lines), 3):
        text = lines[i].strip()

        # Replace single quotes with double quotes and try to load JSON for model_output
        model_output_str = lines[i + 1].strip().replace("'", '"')
        model_output = json.loads(model_output_str)

        # Initialize entities list and relations list
        entities = []
        relations = []
        entity_dict = {}  # To keep track of the entity IDs

        entity_id = 0
        for entity_list in model_output:
            for entity_data in entity_list.values():
                for entity in entity_data:
                    start = entity['start']
                    end = entity['end']
                    label = list(entity_list.keys())[0]  # Using the key of the entity_list as the label
                    entities.append({
                        "id": entity_id,
                        "start_offset": start,
                        "end_offset": end,
                        "label": label
                    })
                    entity_dict[entity["text"]] = entity_id
                    entity_id += 1

        # Extract relations in a separate loop to ensure all entities are processed first
        for entity_list in model_output:
            for entity_data in entity_list.values():
                for entity in entity_data:
                    if 'relations' in entity:
                        for rel_key, rel_values in entity['relations'].items():
                            for rel_value in rel_values:
                                target_entity = rel_value['text']
                                if target_entity in entity_dict:  # Check if target entity exists in entity_dict
                                    relations.append({
                                        "from_id": entity_dict[entity["text"]],
                                        "to_id": entity_dict[target_entity],
                                        "type": rel_key
                                    })

        results.append({
            'text': text,
            'entities': entities,
            'relations': relations
        })

    with open(output_filename, 'w', encoding='utf-8') as f:
        for result in results:
            f.write(json.dumps(result, ensure_ascii=False) + '\n')

    return results

# Convert and print the output
output_filename = "converted_outputtest_v2.jsonl"
converted_data_actual = convert_to_doccano_format("outputtest.txt")

