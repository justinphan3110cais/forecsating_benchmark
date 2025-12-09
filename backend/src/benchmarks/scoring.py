import re

def extract_prediction(prediction_str):
    # Find the first number (integer or float) in the string
    match = re.search(r'(\d+(\.\d+)?)', prediction_str)
    if match:
        return float(match.group(1))
    return None

def brier_score(prediction, actual):
    """
    Calculate the Brier score for a single prediction.
    
    :param prediction: float, the predicted probability (between 0 and 1)
    :param actual: int, the actual outcome (0 or 1)
    :return: float, the Brier score
    """
    if not 0 <= prediction <= 1:
        raise ValueError("Prediction must be between 0 and 1")
    if actual not in [0, 1]:
        raise ValueError("Actual outcome must be 0 or 1")
    
    return (prediction - actual) ** 2

def average_brier_score(predictions, actuals):
    """
    Calculate the average Brier score for multiple predictions, skipping None values.
    
    :param predictions: list of float or None, predicted probabilities
    :param actuals: list of int, actual outcomes (0 or 1)
    :return: float, the average Brier score
    """
    if len(predictions) != len(actuals):
        raise ValueError("The number of predictions and actuals must be the same")
    
    valid_pairs = []
    for pred, act in zip(predictions, actuals):
        if pred is None or pred < 0 or pred > 1:
            print("Invalid pred: ", pred)
        else:
            valid_pairs.append((pred,act))
    
    if not valid_pairs:
        return None  # Return None if there are no valid predictions
    
    individual_scores = [brier_score(pred, act) for pred, act in valid_pairs]
    return sum(individual_scores) / len(individual_scores)