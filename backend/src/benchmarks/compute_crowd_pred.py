import requests
import json
from tqdm import tqdm
from fire import Fire
from scoring import average_brier_score

# def main(input_file: str = "data/manifold_03012024_small.json"):

#     with open(input_file, 'r') as file:
#         data = json.load(file)

#     data = data
#     preds = []
#     labels = []
#     for market in tqdm(data):
#         preds.append(market['crowd_pred'])
#         labels.append(market['resolution'] == "YES")
    
#     brier_score = average_brier_score(preds, labels)

#     print("Brier Score:", brier_score)


def main(input_file: str = "output/test_adam.json"):

    with open(input_file, 'r') as file:
        data = json.load(file)

    data = data
    for i in range(0,4):
        crowd_preds = []
        model_preds = []
        labels = []
        for market in tqdm(data):
            crowd_preds.append(market['crowd_pred'][i][-1])
            model_preds.append(market['predictions'][i])
            labels.append(market['resolution'])
    
        crowd_brier_score = average_brier_score(crowd_preds, labels)
        model_brier_score = average_brier_score(model_preds, labels)

        print(f"{i} Crowd Brier Score:", crowd_brier_score)
        print(f"{i} Model Brier Score:", model_brier_score)
        print("====")

if __name__ == "__main__":
    Fire(main)