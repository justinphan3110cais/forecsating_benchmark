import openai
from tqdm import tqdm
import json
from concurrent.futures import ProcessPoolExecutor

from dotenv import load_dotenv
import os
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

TEMPLATE = '''Given a "What is the probability of..." Q type question. Please transform it into the negation (not) Q by adding a "not" term, but still keep the ""What is the probability of..." type.
Please avoid using double negation.
Only return the "not Q". No yapping, no description, no original Q.

Q: {question}
not Q:
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

    response = response.choices[0].message.content.replace("not Q:", "").strip()
    item['question_org'] = question
    item['question'] = response
    
    return item

def label_data(data, num_processes=40):
    results = []
    for item in tqdm(data):
        item = transform(item)
        results.append(item)
    return results

with open("data/metaculus_sample_val_probability.json") as file:
    data = json.load(file)
data = label_data(data)

# print("data=",data)
with open("data/metaculus_sample_val_probability_negation.json", "w") as file:
    json.dump(data, file, indent=2)
