import openai
from tqdm import tqdm
import json
from concurrent.futures import ProcessPoolExecutor

from dotenv import load_dotenv
import os
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

TEMPLATE = '''Given the a forecasting Q, please transform it into a "What is the probability of..." type question.. Please only return the "Probability Q", no yapping, no description!

Your turn:
Q: {question}
Probability Q:
'''

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

    response = response.choices[0].message.content.replace("Probability Q:", "").strip()
    item['question_org'] = question
    item['question'] = response
    
    return item

def label_data(data, num_processes=40):
    results = []
    for item in tqdm(data):
        item = transform(item)
        results.append(item)
    return results

with open("data/metaculus_sample_val.json") as file:
    data = json.load(file)
data = label_data(data)

# print("data=",data)
with open("data/metaculus_sample_val_probaility.json", "w") as file:
    json.dump(data, file, indent=2)
