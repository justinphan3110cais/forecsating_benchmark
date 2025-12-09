import json


resolution_map_file = "data/resolution_criteria.json"

input_file = "data/metaculus_sample_test.json"
output_file = "data/metaculus_sample_test.json"

with open(resolution_map_file) as file:
    resolution_criterias = json.load(file)
    resolution_criterias = {m['background_text']: m["resolution_criteria"] for m in resolution_criterias}

with open(input_file) as file:
    data = json.load(file)

    for m in data:
        resolution_criteria = resolution_criterias[m['background_text']]
        m['resolution_criteria'] = resolution_criteria

with open(output_file, "w") as file:
    json.dump(data, file, indent=2)

