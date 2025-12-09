# Standard library imports
import concurrent.futures
import logging
import re

# Local application/library-specific imports
# from prompts.prompts import PROMPT_DICT
# from utils import db_utils, time_utils, string_utils

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_formatted_data(
    s3_path,
    retrieval_index=0,
    num_retrievals=5,
    questions_after="2015",
    return_raw_question_data=False,
    data=None,
):
    """
    Retrieve and process training data from an S3 path.

    This function reads data from S3, processes it, and structures it for training purposes.
    It calculates retrieval dates and filters out data based on these dates. The function can
    optionally return raw question data.
    
    Also, the function can optionally take in the |data| directly.

    Parameters:
    s3_path (str): Path to the data file in S3.
    retrieval_index (int, optional): Index for calculating the retrieval date. Defaults to 0.
    num_retrievals (int, optional): Total number of retrievals to consider. Defaults to 5.
    return_raw_question_data (bool, optional): Flag to return raw question data. Defaults to False.
    data (list): List of forecasting questions.

    Returns:
    dict or tuple: A dictionary containing structured training data, or a tuple with the dictionary
    and raw data if return_raw_question_data is True.

    Note:
    This function expects specific keys in the data (e.g., 'date_close', 'date_resolve_at', etc.),
    and logs an error if reading from S3 fails.
    """
    if not data:
        try:
            data = db_utils.read_pickle_from_s3(S3, S3_BUCKET_NAME, s3_path)
        except Exception as e:
            logger.error(f"Error reading data from S3: {e}")
            return {}

    question_dict = {
        "question_list": [],
        "background_list": [],
        "resolution_criteria_list": [],
        "question_dates_list": [],
        "resolve_dates_list": [],
        "retrieval_dates_list": [],
        "answer_list": [],
        "data_source_list": [],
        "community_pred_at_retrieval_list": [],
        "urls_in_background_list": [],
        "category_list": [],
    }
    raw_data = []
    for q in data:
        q["date_close"] = q["date_close"] or q["date_resolve_at"]
        retrieval_date = time_utils.get_retrieval_date(
            retrieval_index,
            num_retrievals,
            q["date_begin"],
            q["date_close"],
            q["date_resolve_at"],
        )

        if retrieval_date is None:
            continue
        elif retrieval_date == q["date_resolve_at"]:
            continue
        elif not time_utils.is_more_recent(
            f"{questions_after}-01-01", q["date_begin"], or_equal_to=True
        ):
            continue

        raw_data.append(q)
        for key, value in {
            "question_list": q["question"],
            "background_list": q["background"],
            "resolution_criteria_list": q["resolution_criteria"],
            "question_dates_list": (
                time_utils.extract_date(q["date_begin"]),
                time_utils.extract_date(q["date_close"]),
            ),
            "resolve_dates_list": q["date_resolve_at"],
            "retrieval_dates_list": (
                time_utils.extract_date(q["date_begin"]),
                retrieval_date,
            ),
            "answer_list": int(q["resolution"]),
            "data_source_list": q["data_source"],
            "community_pred_at_retrieval_list": time_utils.find_pred_with_closest_date(
                retrieval_date, q["community_predictions"]
            )[1],
            "urls_in_background_list": q["urls_in_background"],
            "category_list": q["gpt_3p5_category"],
        }.items():
            question_dict[key].append(value)

    return (question_dict, raw_data) if return_raw_question_data else question_dict


def format_single_question(data_dict, index):
    """
    Format a single question, located by |index|, from a dictionary of all
    questions.

    Args:
        data_dict (dict): Dictionary containing all question data.
        index (int): Index of question.

    Returns:
        dict: Formatted question
    """
    return {
        "question": data_dict["question_list"][index],
        "background": data_dict["background_list"][index],
        "resolution_criteria": data_dict["resolution_criteria_list"][index],
        "answer": data_dict["answer_list"][index],
        "question_dates": data_dict["question_dates_list"][index],
        "retrieval_dates": data_dict["retrieval_dates_list"][index],
        "data_source": data_dict["data_source_list"][index],
        "resolve_date": data_dict["resolve_dates_list"][index],
        "community_pred_at_retrieval": data_dict["community_pred_at_retrieval_list"][
            index
        ],
        "urls_in_background": data_dict["urls_in_background_list"][index],
        "category": data_dict["category_list"][index],
    }


# def reformat_metaculus_questions(
#     data,
#     model_name="gpt-3.5-turbo-1106",
#     prompt=PROMPT_DICT["data_wrangling"]["reformat"],
# ):
#     """
#     Reformat questions from Metaculus to be more readable.

#     In particular, some questions have a title that ends with a parenthesis,
#     containing the actual subject.
#     This function rephrases it to be a Yes/No question.

#     For example,
#     >>> "Who will win the 2020 US presidential election? (Biden)"
#     will be reformatted by the langauge model to
#     >>> "Will Biden win the 2020 US presidential election?"

#     Args:
#         data (list of dict): List of questions in dictionary format.
#         model_name (str, optional): Language model name, default is
#             "gpt-3.5-turbo-1106".
#         prompt (tuple of str, optional): Prompt to use for model evaluation.
#             Default is PROMPT_DICT["data_cleaning"]["reformat"].

#     Returns:
#         Modifies the input data in-place, and returns None.
#     """

#     def find_text_between_stars(text):
#         match = re.search(r"\*([^*]+)\*", text)
#         return match.group(1) if match else None

#     for d in data:
#         if "? (" in d["title"]:
#             prompt = string_utils.get_prompt(
#                 prompt[0],
#                 prompt[1],
#                 question=d["title"],
#             )
#             response = model_eval.get_response_from_model(
#                 model_name=model_name, prompt=prompt
#             )
#             transformed_title = find_text_between_stars(response)
#             if transformed_title:
#                 d["title"] = transformed_title

#     return None