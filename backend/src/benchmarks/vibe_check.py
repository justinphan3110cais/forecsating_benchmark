import sys
import os
import asyncio
import json
from typing import List, Dict
from time import time
from functools import wraps
from datetime import timedelta, datetime

import ray
from dotenv import load_dotenv
from fire import Fire
from tqdm import tqdm

# Get the absolute path of the project root directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

from api import forecasting_search_local
from prompts import planner_prompt, get_prompt, factorized_prompt
from scoring import extract_prediction

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

assert OPENAI_API_KEY and SERPER_API_KEY, "API keys not found in .env file"

os.environ['PYTHONPATH'] = PROJECT_ROOT
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
os.environ['SERPER_API_KEY'] = SERPER_API_KEY
os.environ["RAY_DEDUP_LOGS"] =  "0"
os.environ["RAY_DISABLE_FSMONITOR"] = "1"

def load_dataset(file_path: str) -> List[Dict]:
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def retry(times=3, exceptions=(Exception,)):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for attempt in range(times):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    if attempt == times - 1:  # Last attempt
                        raise
                    print(f"Attempt {attempt + 1} failed: {str(e)}. Retrying...")
        return wrapper
    return decorator

@retry(times=3)
async def forecasting_search_local_with_retry(input_data):
    return await forecasting_search_local(input_data)

def process_forecasting(full_result: str):
    response=""
    try:
        sources, chunks = full_result.split('[SEP_SOURCE]')
        if "END_FACTORIZED" in chunks:
            factorized_response, response = chunks.split('[END_FACTORIZED]')
            factorized_response = factorized_response.replace('[START_FACTORIZED]', "")
            factorized_response = json.loads(factorized_response)
        else:
            response = chunks
            factorized_response = []
        sources = json.loads(sources)
        # only log query and link
        if "<answer>" in response:
            prediction = response.split("<answer>")[-1].replace("</answer>", "")
        else:
            prediction = response.split("Final Prediction")[-1]

        prediction = extract_prediction(prediction)
        if prediction is None:
            print(f"Failed to parse prediction for: {prediction}")

        return dict(prediction=prediction, 
                    response=response, 
                    factorized_response=factorized_response,
                    sources=sources)
    except:
        return dict(prediction=None, response=response)

@ray.remote
def process_request(question: str, id: int, model: str, breadth: int, prompt_type: str="adam", search_type: str="search"):
    publisher_prompt = get_prompt(prompt_type)

    input_data = {
        "model": model,
        "messages": [{"role": "user", "content": question}],
        "breadth": breadth,
        "plannerPrompt": planner_prompt,
        "publisherPrompt": publisher_prompt,
        "beforeTimestamp": None,
        "search_type": search_type,
    }
    t0 = time()
    result = asyncio.run(forecasting_search_local_with_retry(input_data))
    response = process_forecasting(result)
    t1 = time()
    factorized_response = response.get("factorized_response", [])
    print(f"📊. Question: {question} | \
                Forecasting: {response['prediction']} | Total time: {(t1-t0):.2f}s")
    return {"id": id, "question":question, **response}

def process_requests_ray(questions: List[str], parallel: int, **forecasting_kwargs):
    env_vars = {k: str(v) for k, v in os.environ.items()}
    ray.init(runtime_env={"env_vars": env_vars})
    futures = [process_request.options(num_cpus=1).remote(q, id=id, **forecasting_kwargs) for id, q in enumerate(questions)]
    results = []
    for _ in tqdm(range(len(futures)), desc="Processing"):
        done, futures = ray.wait(futures)
        results.extend(ray.get(done))
    ray.shutdown()
    return results

def main(model: str = "gpt-4o",
         input_file: str = "data/vibe_check_questions.txt", 
         output_file: str = "data/vibe_check_outputs.json",
         breadth: int = 7, 
         parallel: int = 20,
         prompt_type: str = "adam", # og,adam,halawi
         search_type: str = "news"):
    """
    Process forecasting questions using the specified model and parameters.

    Args:
    model (str): The name of the model to use.
    input_file (str): Path to the input text file containing questions.
    output_file (str): Path to the output JSON file for results.
    breadth (int): The breadth parameter for the planner prompt. Default is 5.
    parallel (int): Number of parallel processes to use. Default is 20.
    prompt_type (str): Type of prompt to use. Default is "adam".
    """
    questions = load_dataset(input_file)
    t0 = time()
    results = process_requests_ray(questions, parallel, model=model, breadth=breadth, prompt_type=prompt_type, search_type=search_type)
    
    results = sorted(results, key=lambda x: x['id'])
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)


    preds = [str(q['prediction']*100 if q['prediction'] != None else -1) for q in results]
    print("\n".join(preds))
    t1 = time()
    print(f"Processing complete. Results written to {output_file}. Total time: {t1 - t0:.2f}s")

if __name__ == "__main__":
    Fire(main)