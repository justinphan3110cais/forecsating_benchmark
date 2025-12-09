import os

# run = 4
# for time_chunk in range(3,4):
#     os.system("ray stop --force")
#     os.system(f"python3 manifold.py --time_chunk '{time_chunk}' --input_file data/metaculus_sample_full.json --search_type news --model gpt-4o --output_file public_output/test_metaculus_full_v15_chunk{time_chunk}_run{run}.json --breadth 7 --prompt_type v15")


# prompt_type = "halawi"
# # run=1
# for run in (5,6):
#     for time_chunk in range(3,4):
#         os.system("ray stop --force")
#         os.system(f"python3 manifold.py --time_chunk '{time_chunk}' --input_file data/metaculus_sample_full.json --search_type news --model gpt-4o-2024-05-13 --output_file public_output/test_metaculus_full_{prompt_type}_chunk{time_chunk}_run{run}.json --breadth 7 --prompt_type {prompt_type}")

# os.system("ray stop --force")
# os.system(f"python3 manifold.py --time_chunk '3' --input_file data/halawi_dataset.json --search_type news --model gpt-4o-2024-05-13 --output_file halawi_output/halawi_v15_0.json --breadth 10 --prompt_type v15")

# os.system(f"python3 manifold.py --time_chunk '0,1,2,3' --input_file data/halawi_dataset_polymarket.json --search_type news --model gpt-4o-2024-05-13 --output_file halawi_output/halawi_v15_polymarket_run0.json --breadth 7 --prompt_type v15")

# for run in range(3,5):
#     os.system(f"python3 manifold.py --time_chunk '0,1,2,3,4' --input_file data/halawi_dataset_metaculus_full.json --search_type news --model gpt-4o-2024-05-13 --output_file halawi_output/halawi_v15_metaculus_full_run{run}.json --breadth 10 --prompt_type v15")

# for i in range(5,7):
#     os.system(f"python3 manifold.py --time_chunk '0,1,2,3,4' --input_file data/halawi_dataset_metaculus_full.json --search_type news --model gpt-4o-2024-05-13 --output_file halawi_output/halawi_v15_metaculus_full_breadth7_run{i}.json --breadth 7 --prompt_type v15")

# model = "grok-2-latest"
# for i in range(0,5):
#     os.system(f"python3 manifold.py --time_chunk '0,1,2,3,4' --input_file data/halawi_dataset_metaculus_full.json --search_type news --model {model} --output_file halawi_output/halawi_v15_metaculus_{model}_breadth7_run{i}.json --breadth 7 --prompt_type v15")

# model = "grok-2-latest"
# os.system(f"python3 manifold.py --time_chunk '0,1,2,3,4' --input_file data/halawi_dataset_metaculus_full.json --search_type news --model {model} --output_file halawi_output/halawi_v15_metaculus_{model}_breadth10_run0.json --breadth 10 --prompt_type v15")

# model = "o1-preview"
# prompt_type = "v16"
# for i in range(1,5):
#     os.system(f"python3 benchmark.py --time_chunk '0,1,2,3,4' --input_file data/halawi_dataset_metaculus_full.json --search_type news --model {model} --output_file halawi_output/halawi_v15_metaculus_{model}_breadth7_run{i}.json --breadth 7 --prompt_type v16")



model = "gpt-4o-2024-05-13"
prompt_type = "v16"
for i in range(3,5):
    os.system(f"python3 benchmark.py --time_chunk '0,1,2,3,4' --input_file data/halawi_dataset_metaculus_full.json --search_type news --model {model} --output_file halawi_output/halawi_{prompt_type}_metaculus_{model}_breadth7_run{i}.json --breadth 7 --prompt_type v16")

# os.system(f"python3 manifold.py --time_chunk '3' --input_file data/metaculus_sample_full.json --search_type news --model {model} --output_file public_output/test_metaculus_full_{prompt_type}_{model}_chunk{3}_run{0}.json --breadth 7 --prompt_type {prompt_type}")


# for i in range(1,3):
#     os.system(f"python3 manifold.py --time_chunk '0,1,2,3,4' --input_file data/halawi_dataset_metaculus_full.json --search_type news --model gpt-4o-2024-05-13 --output_file halawi_output/halawi_halawi_metaculus_full_run{i}.json --breadth 10 --prompt_type halawi")

# os.system("ray stop --force")
# os.system(f"python3 manifold.py --time_chunk '3' --input_file data/metaculus_sample_full.json --search_type news --model gpt-4o --output_file stagging_output/test_metaculus_full_v14_1_1.json --breadth 7 --prompt_type v14_1")
# os.system("ray stop --force")
# os.system(f"python3 manifold.py --time_chunk '3' --input_file data/metaculus_sample_full.json --search_type news --model gpt-4o --output_file stagging_output/test_metaculus_full_v14_1_2.json --breadth 7 --prompt_type v14_1")
# os.system("ray stop --force")
# os.system(f"python3 manifold.py --time_chunk '3' --input_file data/metaculus_sample_full.json --search_type news --model gpt-4o --output_file stagging_output/test_metaculus_full_v14_1_3.json --breadth 7 --prompt_type v15")
# os.system("ray stop --force")
# os.system(f"python3 manifold.py --time_chunk '3' --input_file data/metaculus_sample_full.json --search_type news --model gpt-4o --output_file stagging_output/test_metaculus_full_v14_1_4.json --breadth 7 --prompt_type v15")
