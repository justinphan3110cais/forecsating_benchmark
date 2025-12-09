import os

split = 'test'
model = "gpt-4o"
# model = "o3-mini"
model = "research-grok-3-latest"

model = "grok-3-beta"
# model = "research-grok-3-reasoning"
os.system("ray stop --force")
# os.system(f"python3 new_benchmark.py --time_chunk '3' --input_file data/metaculus_sample_val_0304.json --search_type news --model {model} --output_file new_output/{model}.json --parallel 32 --breadth 7 --prompt_type v15")
# os.system(f"python3 new_benchmark.py --time_chunk '0' --input_file data/metaculus_sample_{split}_1101_min20.json --search_type news --model {model} --output_file new_output/{model}_1101_{split}_min20.json --parallel 64 --breadth 7 --prompt_type v15")

os.system(f"python3 new_benchmark.py --time_chunk '0' --input_file data/metaculus_sample_{split}_1101_min20.json --search_type news --model {model} --output_file new_output/{model}_1101_{split}_min20_grok_prompt.json --parallel 64 --breadth 7 --prompt_type grok_reasoning")

# os.system("ray stop --force")


# os.system(f"python3 new_benchmark.py --time_chunk '0' --input_file data/metaculus_sample_{split}_1101_min20.json --search_type news --model {model} --output_file new_output/{model}_1101_{split}_min20.json --parallel 32 --breadth 7 --prompt_type v15")

# breadth = 7
# for run in range(0, 1):
#     os.system("ray stop --force")
#     os.system(f"python3 new_benchmark.py --time_chunk '0' --input_file data/metaculus_sample_{split}_1101_min20.json --search_type news --model {model} --output_file new_output/{model}_1101_{split}_min20_breadth{breadth}_run{run}.json --parallel 64 --breadth {breadth} --prompt_type v15_grok")


# os.system("ray stop --force")
# os.system(f"python3 new_benchmark.py --time_chunk '0' --input_file data/metaculus_sample_{split}_1101_min20.json --search_type news --model {model} --output_file new_output/{model}_1101_{split}_min20.json --parallel 32 --breadth 7 --prompt_type v15")



# os.system("ray stop --force")
# os.system(f"python3 new_benchmark.py --time_chunk '3' --input_file data/metaculus_sample_full.json --search_type news --model gpt-4o --output_file new_output/test_metaculus_full_v14_1_5.json --breadth 7 --prompt_type v15")
