import sys
import os
import asyncio
import json
from typing import List, Dict
from time import time
from functools import wraps
from datetime import datetime
import numpy as np
import ray
from dotenv import load_dotenv
from fire import Fire
from tqdm import tqdm

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

from api import forecasting_search_local
from prompts import planner_prompt, get_prompt, factorized_prompt
from scoring import extract_prediction, average_brier_score

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

assert OPENAI_API_KEY and SERPER_API_KEY, "API keys not found in .env file"

os.environ['PYTHONPATH'] = PROJECT_ROOT
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
os.environ['SERPER_API_KEY'] = SERPER_API_KEY
os.environ["RAY_DEDUP_LOGS"] =  "0"

def load_dataset(file_path: str) -> List[Dict]:
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data

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
        if '[SEP_SOURCE]' in full_result:
            sources, chunks = full_result.split('[SEP_SOURCE]')
            sources = json.loads(sources)
        else:
            sources = {}
            chunks = full_result
        if "END_FACTORIZED" in chunks:
            factorized_response, response = chunks.split('[END_FACTORIZED]')
            factorized_response = factorized_response.replace('[START_FACTORIZED]', "")
            factorized_response = json.loads(factorized_response)
        else:
            response = chunks
            factorized_response = []
        
        # only log query and link
        if "<answer>" in response:
            prediction = response.split("<answer>")[-1].replace("</answer>", "")
        else:
            prediction = response.split("Final Prediction")[-1]

        parsed_prediction = extract_prediction(prediction)
        if parsed_prediction is None:
            print(f"Failed to parse prediction for: {prediction}")

        return dict(prediction=parsed_prediction, 
                    response=response, 
                    # factorized_response=factorized_response,
                    sources=sources
                    )
    except Exception as e:
        print("Exception: ", str(e))
        return dict(prediction=None, response=response)

@ray.remote
def process_request(example: Dict, 
                    model: str, 
                    breadth: int, 
                    prompt_type: str="adam", 
                    search_type: str="search"):
    question = example['question']
    # category = example['category']
    resolution_criteria = example.get("resolution_criteria")

    question = f"{question}\n\nBackground text:{example['background_text']}"
    if resolution_criteria:
        question += f"\n\nResolution Criteria: {resolution_criteria}"

    # question = f"{question}\n\nBackground text:{example['background_text']}\n\nStart date:{example['createdTimeStr']}\n\nEnd date:{example['resolutionTimeStr']}"

    publisher_prompt = get_prompt(prompt_type)
    # publisher_prompt = politics_publisher_prompt
    
    t0 = time()
    predictions = []
    responses = []
    sources = []
    for time_chunk in TIME_CHUNK:
        resolution_time = example['crowd_pred'][time_chunk][0]
        resolution_date = datetime.fromtimestamp(resolution_time / 1000).date()
        before_date = resolution_date
        beforeTimestamp = int(datetime.combine(before_date, datetime.min.time()).timestamp())
        beforeTimestampStr = datetime.fromtimestamp(beforeTimestamp).strftime("%Y-%m-%d")

        input_data = {
            "model": model,
            "messages": [{"role": "user", "content": question}],
            "breadth": breadth,
            "plannerPrompt": planner_prompt,
            "publisherPrompt": publisher_prompt,
            "factorizedPrompt": factorized_prompt,
            "beforeTimestamp": beforeTimestamp,
            "search_type": search_type,
        }
        result = asyncio.run(forecasting_search_local_with_retry(input_data))
        response = process_forecasting(result)

        predictions.append(response['prediction'])
        responses.append(response['response'])
        sources.append(response.get('sources', []))
    t1 = time()

        # factorized_response = response.get("factorized_response", [])
        # factorized_str = "\n".join([f"Question: {q['query']} | Forecast: {q['forecast']}" for q in factorized_response])
    crow_preds = [round(e[-1], 2) for i, e in enumerate(example['crowd_pred']) if i in TIME_CHUNK]
    print(f"📊. Question: {example['question']} | Date: {beforeTimestampStr} | \
                Forecasting: {predictions} | Crowd: {crow_preds} | Res: {float(example['resolution'])} | Total time: {(t1-t0):.2f}s")

    return {**example, "predictions": predictions, "responses":responses, "sources": sources}

def process_requests_ray(questions: List[str], parallel: int, **forecasting_kwargs):
    env_vars = {k: str(v) for k, v in os.environ.items()}
    ray.init(num_cpus=parallel, runtime_env={"env_vars": env_vars})

    futures = [process_request.options(num_cpus=4).remote(q, **forecasting_kwargs) for q in questions]
    results = []
    for _ in tqdm(range(len(futures)), desc="Processing"):
        done, futures = ray.wait(futures)
        results.extend(ray.get(done))
    ray.shutdown()
    return results

def main(model: str = "gpt-4o-mini",
         input_file: str = "data/metaculus_sample_val.json", 
         output_file: str = None,
         breadth: int = 5, 
         parallel: int = 20,
         prompt_type: str = "adam", # og,adam,halawi
         time_chunk: tuple = (1,2,3,4),
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
    global TIME_CHUNK
    print("time_chunk=",time_chunk)
    if type(time_chunk) == int:
        time_chunk = [time_chunk]
    TIME_CHUNK = time_chunk

    examples = load_dataset(input_file)
    examples = examples
    t0 = time()

    results = process_requests_ray(examples, parallel, model=model, breadth=breadth, prompt_type=prompt_type, search_type=search_type)

    if not output_file:
        output_file = input_file.replace(".json", f"_{model}_{breadth}_{prompt_type}_{search_type}_outputs.json")
    
    # Create the full results file
    full_output_file = output_file.replace(".json", "_full.json")
    os.makedirs(os.path.dirname(full_output_file), exist_ok=True)
    with open(full_output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)

    # Create the results file without the "response" key
    compact_results = [{k: v for k, v in item.items() if "response" not in k and k != 'sources'} for item in results]

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(compact_results, f, indent=2)

    overall_brier_scores = []
    crowd_overall_brier_scores = []
    all_preds = []
    all_labels = []
    all_cors = []
    all_cors_crowd = []
    for i, chunk in enumerate(time_chunk):
        preds = [q['predictions'][i] for q in results]
        crowd_preds = [q['crowd_pred'][chunk][-1] for q in results]

        labels = [float(q['resolution']) for q in results]
        brier_score = average_brier_score(preds, labels)
        crowd_brier_score = average_brier_score(crowd_preds, labels)
        print(f"Time {chunk} Brier Score:", brier_score, " | Crowd: ", crowd_brier_score)

        cors = [(pred >= 0.5) == label for pred, label in zip(preds, labels) if pred is not None]
        cors_crowd = [(crowd_pred >= 0.5) == label for crowd_pred, label in zip(crowd_preds, labels)]
        print(f"Time {chunk} Cor:", np.mean(cors), " | Crowd: ", np.mean(cors_crowd))

        overall_brier_scores.append(brier_score)
        crowd_overall_brier_scores.append(crowd_brier_score)
        all_preds.extend(preds)
        all_labels.extend(labels)
        all_cors.extend(cors)
        all_cors_crowd.extend(cors_crowd)

    print("Overall Avg Brier Score:", np.mean(overall_brier_scores), " | Crowd: ", np.mean(crowd_overall_brier_scores))
    print("Overall Avg Cor:", np.mean(all_cors), " | Crowd: ", np.mean(all_cors_crowd))
    t1 = time()
    
    print(f"Processing complete. Results written to {output_file}. Total time: {t1 - t0:.2f}s")

if __name__ == "__main__":
    Fire(main)