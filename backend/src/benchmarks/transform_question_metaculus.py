import openai
from tqdm import tqdm
import json
from concurrent.futures import ProcessPoolExecutor

from dotenv import load_dotenv
import os
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

TEMPLATE = '''I have questions that need to be transformed for clarity.

Here are some examples:
Example 1:
Before: Who will win the 2022-2023 Premier League? (Leicester City)
After: Will Leicester City win the 2022-2023 Premier League?

Example 2:
Before: What coalition will govern Berlin after the 2023 repeat state election? (SPD+Greens)
After: Will SPD+Greens govern Berlin after the 2023 repeat state election?

Example 3:
Before: If Republicans win control of the House of Representatives in the 2022 election, who will be the next Majority Whip of the U.S. House of Representatives? (Rep. Jim Banks)
After: If Republicans win control of the House of Representatives in the 2022 election, will Jim Banks be the next Majority Whip of the U.S. House of Representatives?

Example 4:
Before: Economic Trouble: Will a country’s currency depreciate 15% or more in the second half of 2022? (Thai Baht ฿)
After: Economic Trouble: Will the Thai Baht ฿ currency depreciate 15% or more in the second half of 2022?

Example 5:
Before: How many of the claims from study 3 of "Behavioral nudges reduce failure to appear for court" (Science, 2020) replicate?
After: Will exactly 2 claims from study 3 of "Behavioral nudges reduce failure to appear for court" (Science, 2020) replicate?

Now transform the following question. Please only return the transformed question. No yapping!

Before: {question}
After: :'''

def transform(item):
    question = item['question']
    client = openai.OpenAI(api_key=OPENAI_API_KEY) 
    input = TEMPLATE.format(question=question)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": input}
        ],
        max_tokens=64
    )

    response = response.choices[0].message.content.replace("After: ", "").strip()
    item['question'] = response
    
    return item

def label_data(data, num_processes=40):
    results = []
    for item in tqdm(data):
        item = transform(item)
        results.append(item)
    return results

with open("data/metaculus_sample_test.json") as file:
    data = json.load(file)
data = label_data(data)

# print("data=",data)
with open("data/metaculus_sample_test.json", "w") as file:
    json.dump(data, file, indent=2)
