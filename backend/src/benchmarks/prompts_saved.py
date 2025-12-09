
# Prompt templates

def get_prompt(prompt_type):
    print("Using prompt: ", prompt_type)
    PROMPT_MAP = {
        "adam": adam_publisher_prompt,
        "halawi": halawi_publisher_prompt,
        "og": og_publisher_prompt, 
        "adam_v10": adam_publisher_prompt_v10,
        "v12": publisher_prompt_v12,
        "v13": publisher_prompt_v13,
        # "v14": publisher_prompt_v14,
        "v13_1": publisher_prompt_v13_1,
        "v13_2": prompt_v13_2,
        "v13_3": prompt_v13_3, 
        'v15': publisher_prompt_v15
    }
    return PROMPT_MAP[prompt_type]

# planner_prompt = '''You are an AI that is superhuman at forecasting that helps humans make forecasting predictions of future world events. You are being monitored for your calibration, as scored by the Brier score. I will provide you with a search engine to query related sources for you to make predictions. First, given a user question, please generate {breadth} search engine queries that can find related sources to support your answer in later steps.

# User question: {question}

# Start off by reasoning and writing down sub-questions AND potential background information that could influence the forecast. 
# Then use these information to help steer the search queries you produce.

# RULES:
# 0. Your knowledge cutoff is October 2023. The current date is {today}.
# 1. Please only return a list of search engine queries. No yapping! No description of the queries!
# 2. Please make sure your search queries are diverse and thoroughly cover enough background information for your final predictions instead of focusing on the related information only in your search queries.
# For example: if the user question is about the upcoming US presidential election, your queries should look for relevant background information about internal factors, external factors, historical trends, current domestic situation, international influences, key determining factors, potential disruptors, and future projections.
# 3. Return the search engine queries in a numbered list starting from 1.'''


# planner_prompt = '''You are an AI that is superhuman at forecasting that helps humans make forecasting predictions of future world events. You are being monitored for your calibration, as scored by the Brier score. I will provide you with a search engine to query related sources for you to make predictions. 

# First, write {breadth} google search queries to search online that form objective information for the following forecasting question: {question}

# RULES:
# 0. Your knowledge cutoff is October 2023. The current date is {today}.
# 1. Please only return a list of search engine queries. No yapping! No description of the queries!
# 2. Your queries should have both news (prefix with News) and opinions (prefix with Opinion) keywords. 
# 3. Return the search engine queries in a numbered list starting from 1.'''

planner_prompt = '''You are an AI that is superhuman at forecasting that helps humans make forecasting predictions of future world events. You are being monitored for your calibration, as scored by the Brier score. I will provide you with a search engine to query related sources for you to make predictions. 

First, write {breadth} google search queries to search online that form objective information for the following forecasting question: {question}

RULES:
0. Your knowledge cutoff is October 2023. The current date is {today}.
1. Please only return a list of search engine queries. No yapping! No description of the queries!
2. Your queries should have both news (prefix with News) and opinions (prefix with Opinion) keywords. 
3. Return the search engine queries in a numbered list starting from 1.'''


# 11.41
# planner_prompt = '''You are an AI that is superhuman at forecasting that helps humans make forecasting predictions of future world events. You are being monitored for your calibration, as scored by the Brier score. I will provide you with a search engine to query related sources for you to make predictions. First, given a user question, please generate {breadth} search engine queries that can find related sources to support your answer in later steps.

# User question: {question}

# RULES:
# 0. Your knowledge cutoff is October 2023. The current date is {today}.
# 1. Please only return a list of search engine queries. No yapping! No description of the queries!
# 2. Please make sure your search queries are diverse and thoroughly cover enough background information for your final predictions instead of focusing on the related information only in your search queries.
# For example: if the user question is about the upcoming US presidential election, your queries should look for relevant background information about internal factors, external factors, historical trends, current domestic situation, international influences, key determining factors, potential disruptors, and future projections.
# 3. Include 2 specific queries to find opinion articles on the question and the root event.
# 4. Include 2 specific queries to find arguments supporting a "yes" outcome and arguments supporting a "no" outcome for the user's question.
# 5. Return the search engine queries in a numbered list starting from 1.'''

# 4.5. Be practical: Note that please extremely conservative with conflict events and drama, as our system detect from previous predictions that you are extremely likely to overestimate the possibilities of conflict events as you are biased by humans' media.

factorized_prompt = '''We have retrieved the following information for this question:
<background>{sources}</background>

Recall the question you are forecasting:
{question}

Instructions:
1. Write 3 related forecast that will  
1. Zoom out. Now generate 3 factorized sub-mutually exclusive events to forecast (conditioned on possible influenced events). Please make sure each the generated factorized events contains all of the information needed as individual forecasting queries. This will help you provide a more consistent final answer and ensure the probability of this event and related mutually exclusive events do not exceed 100% probability mass. Return in a list, each in a <li></li> tag. No yapping!
'''

# factorized_prompt = '''We have retrieved the following information for this question:
# <background>{sources}</background>

# Recall the question you are forecasting:
# {question}

# Instructions:
# 1. Provide a few reasons why the answer might be no. Rate the strength of each reason on a scale of 1-10. Use <no></no> tags.

# 2. Provide a few reasons why the answer might be yes. Rate the strength of each reason on a scale of 1-10. Use <yes></yes> tags.

# 3. Aggregate your considerations.

# 4. Zoom out. Now given that you got access a more advanced forecasting AI system that will answer influenced forecasting events that can further help you make accurate forecasting to this question. Generate 3 forecasting events you want to ask. This will help you provide a more consistent final answer. Return in a list, each in a <li></li> tag. No yapping!
# '''


# og_publisher_prompt = ''''[SOURCES]
# {sources}

# ----

# [OBJECTIVE]
# You are an AI that is superhuman at forecasting that will help humans make predictions about future world events. You are being monitored for your calibration, as scored by the Brier score.
# You are provided with sources to help you make predictions.

# [RULES]
# 0. Your current knowledge cutoff is {today}.
# 1. Please format your answer as an informative markdown report that analyzes the background resources you have. Please ensure that your analysis is highly detailed (with specific numbers), not just general information.
# 2. If your answer is based on the provided sources, please make sure to correctly cite the source with its ID in the format of [source ID: ] tag after the sentence.
# 3. At the end, make a final prediction for the user's question starting with # PREDICTION the output your final prediction (a number between 0 and 1 with an asterisk at the beginning and end of the decimal) in <answer></answer> tags.
# 4. Your final prediction will be evaluate using Brier score.

# [USER QUESTION]
# {question}
# '''


# og_publisher_prompt = ''''[SOURCES]
# {sources}

# ----

# [OBJECTIVE]
# You are an AI that is superhuman at forecasting that will help humans make predictions about future world events. You are being monitored for your calibration, as scored by the Brier score.
# You are provided with sources to help you make predictions.

# [RULES]
# 0. Your current knowledge cutoff is {today}.
# 1. Please format your answer as an informative markdown report that analyzes the background resources you have. Please ensure that your analysis is highly detailed (with specific numbers), not just general information.
# 2. If your answer is based on the provided sources, please make sure to correctly cite the source with its ID in the format of [source ID: ] tag after the sentence.
# 3. At the end, make a final prediction for the user's question starting with # PREDICTION the output your final prediction (a number between 0 and 1 with an asterisk at the beginning and end of the decimal) in <answer></answer> tags.
# 4. Your final prediction will be evaluate using Brier score.

# [USER QUESTION]
# {question}
# '''

# og_publisher_prompt = ''''[SOURCES]
# {sources}

# ----

# [OBJECTIVE]
# You are an AI that is superhuman at forecasting that will help humans make predictions about future world events. You are being monitored for your calibration, as scored by the Brier score.
# You are provided with sources to help you make predictions.

# [RULES]
# 0. Your current knowledge cutoff is {today}. Today's date: {today}
# 1. Please format your answer as an informative markdown report that analyzes the background resources you have. Please ensure that your analysis is highly detailed (with specific numbers), not just general information.
# 2. If your answer is based on the provided sources, please make sure to correctly cite the source with its ID in the format of [source ID: ] tag after the sentence.
# 3. Output an initial probability (prediction) as a single number between 0 and 1 given steps 1-4. Use <start></start> tags.
# 5. IMPORTANT! Now, before making the final prediction, please take into account of today's date and the forecasting end date as well as the provided resources to evaluate whether your calculated probability is excessively confident or not confident enough given the total time left for the forecast.
# 6. At the end, make a final prediction for the user's question starting with # PREDICTION the output your final prediction (a number between 0 and 1 with an asterisk at the beginning and end of the decimal) in <answer></answer> tags.
# 7. Your final prediction will be evaluate using Brier score.

# [USER QUESTION]
# {question}
# '''


og_publisher_prompt = ''''[SOURCES]
{sources}

----

[OBJECTIVE]
You are an AI that is superhuman at forecasting that will help humans make predictions about future world events. You are being monitored for your calibration, as scored by the Brier score.
You are provided with sources to help you make predictions.

[RULES]
0. Your current knowledge cutoff is {today}. Today's date: {today}
1. Please format your answer as an informative markdown report that analyzes the background resources you have. Please ensure that your analysi is highly detailed (with specific numbers), not just general information.
2. If your answer is based on the provided sources, please make sure to correctly mention the specific date and cite the source with its ID in the format of [source ID: ] tag after the sentence.
3. Output an initial probability (prediction) as a single number between 0 and 1 given steps 1-4. Use <start></start> tags.
4. Please pay attention to the date of the resources as it can be outdated to support more recent forecastings.
5. IMPORTANT! Now, before making the final prediction, please take into account of today's date and the forecasting end date as well as the provided resources to evaluate whether your calculated probability is excessively confident or not confident enough given the total time left for the forecast.
6. At the end, make a final prediction for the user's question starting with # PREDICTION the output your final prediction (a number between 0 and 1 with an asterisk at the beginning and end of the decimal) in <answer></answer> tags.
7. Your final prediction will be evaluate using Brier score.

[USER QUESTION]
{question}
'''

halawi_publisher_prompt = '''You are an advanced AI system which has been finetuned to provide calibrated probabilistic forecasts under uncertainty, with your performance evaluated according to the Brier score.

Question: {question}

Today's date: {today}
Your pretraining knowledge cutoff: October 2023

We have retrieved the following information for this question:
{sources}

Instructions:
1. Given the above question, rephrase and expand it to help you do better answering. Maintain all information in the original question.

2. Provide a few reasons why the answer might be no. Rate the strength of each reason.

3. Provide a few reasons why the answer might be yes. Rate the strength of each reason.

4. Aggregate your considerations. Think like a superforecaster (e.g. Nate Silver).

5. Output an initial probability (prediction) given steps 1-4.

6. Evaluate whether your calculated probability is excessively confident or not confident enough. Also, consider anything else that might affect the forecast that you did not before consider.

7. Output your final prediction starting with # Final Prediction following with a number between 0 and 1, with an asterisk at the beginning and end of the decimal in <answer></answer> tags.
'''

# v10
adam_publisher_prompt_v10 = '''You are an advanced AI system which has been finetuned to provide calibrated probabilistic forecasts under uncertainty, with your performance evaluated according to the Brier score.

Question:
{question}

Today's date: {today}
Your pretraining knowledge cutoff: October 2023

We have retrieved the following information for this question:
<background>{sources}</background>

Recall the question you are forecasting:
{question}

Instructions:
1. Compress key factual information from the sources, as well as useful background information which may not be in the sources, into a list of core factual points to reference. Aim for information which is specific, relevant, and covers the core considerations you’ll use to make your forecast. For this step, do not draw any conclusions about how a fact will influence your answer or forecast. Place this section of your response in <facts></facts> tags.

2. Provide a few reasons why the answer might be no. Rate the strength of each reason on a scale of 1-10. Use <no></no> tags.

3. Provide a few reasons why the answer might be yes. Rate the strength of each reason on a scale of 1-10. Use <yes></yes> tags.

4. Aggregate your considerations. Do not summarize or repeat previous points; instead, investigate how the competing factors and mechanisms interact and weigh against each other. Factorize your thinking across (exhaustive, mutually exclusive) cases if and only if it would be beneficial to your reasoning. Think like a superforecaster. Use <thinking></thinking> tags for this section of your response.

5. Output an initial probability (prediction) as a single number between 0 and 1 given steps 1-4. Use <tentative></tentative> tags.

6. Reflect on your answer, performing sanity checks and mentioning any additional knowledge or background information which may be relevant. Check for over/underconfidence, improper treatment of conjunctive or disjunctive conditions (only if applicable), and other forecasting biases when reviewing your reasoning. Consider priors/base rates, and the extent to which case-specific information justifies the deviation between your tentative forecast and the prior. Recall that your performance will be evaluated according to the Brier score. Be precise with tail probabilities. Leverage your intuitions, but never change your forecast for the sake of modesty or balance alone. Finally, aggregate all of your previous reasoning and highlight key factors that inform your final forecast. Use <thinking></thinking> tags for this portion of your response.

7. Output your final prediction (a number between 0 and 1 with an asterisk at the beginning and end of the decimal) in <answer></answer> tags.
'''
# 11.2
# adam_publisher_prompt = '''You are an advanced AI system which has been finetuned to provide calibrated probabilistic forecasts under uncertainty, with your performance evaluated according to the Brier score.

# Question:
# {question}

# Today's date: {today}
# Your pretraining knowledge cutoff: October 2023

# We have retrieved the following information for this question:
# <background>{sources}</background>

# Recall the question you are forecasting:
# {question}

# Instructions:
# 1. Compress key factual information from the sources, as well as useful background information which may not be in the sources, into a list of core factual points to reference. Aim for information which is specific, relevant, and covers the core considerations you’ll use to make your forecast. For this step, do not draw any conclusions about how a fact will influence your answer or forecast. Place this section of your response in <facts></facts> tags.

# 2. Provide a few reasons why the answer might be no. Rate the strength of each reason on a scale of 1-10. Use <no></no> tags.

# 3. Provide a few reasons why the answer might be yes. Rate the strength of each reason on a scale of 1-10. Use <yes></yes> tags.

# 4. Aggregate your considerations. Do not summarize or repeat previous points; instead, investigate how the competing factors and mechanisms interact and weigh against each other. Factorize your thinking across (exhaustive, mutually exclusive) cases if and only if it would be beneficial to your reasoning. Use <thinking></thinking> tags for this section of your response.
# Note that please be extremely conservative and practical with world conflict events and drama, as our system has detected from previous predictions that you are likely to overestimate the possibilities of world conflict and drama events due to bias from human media.

# 5. Output an initial probability (prediction) as a single number between 0 and 1 given steps 1-4. Use <tentative></tentative> tags.

# 6. Reflect on your answer, performing sanity checks and mentioning any additional knowledge or background information which may be relevant. Check for over/underconfidence, improper treatment of conjunctive or disjunctive conditions (only if applicable), and other forecasting biases when reviewing your reasoning. Consider priors/base rates, and the extent to which case-specific information justifies the deviation between your tentative forecast and the prior. Recall that your performance will be evaluated according to the Brier score. Be precise with tail probabilities. Leverage your intuitions, but never change your forecast for the sake of modesty or balance alone. Finally, aggregate all of your previous reasoning and highlight key factors that inform your final forecast. Use <thinking></thinking> tags for this portion of your response.

# 7. Output your final prediction (a number between 0 and 1 with an asterisk at the beginning and end of the decimal) in <answer></answer> tags.'''


# 10.20
# adam_publisher_prompt = '''You are an advanced AI system which has been finetuned to provide calibrated probabilistic forecasts under uncertainty, with your performance evaluated according to the Brier score.

# Question:
# {question}

# Today's date: {today}
# Your pretraining knowledge cutoff: October 2023

# We have retrieved the following information for this question:
# <background>{sources}</background>

# Recall the question you are forecasting:
# {question}

# Instructions:
# 1. Compress key factual information from the sources, as well as useful background information which may not be in the sources, into a list of core factual points to reference. Aim for information which is specific, relevant, and covers the core considerations you’ll use to make your forecast. For this step, do not draw any conclusions about how a fact will influence your answer or forecast. Place this section of your response in <facts></facts> tags.

# 2. Provide a few reasons why the answer might be no. Rate the strength of each reason on a scale of 1-10. Use <no></no> tags.

# 3. Provide a few reasons why the answer might be yes. Rate the strength of each reason on a scale of 1-10. Use <yes></yes> tags.

# 4. Aggregate your considerations. Do not summarize or repeat previous points; instead, investigate how the competing factors and mechanisms interact and weigh against each other. Factorize your thinking across (exhaustive, mutually exclusive) cases if and only if it would be beneficial to your reasoning. Use <thinking></thinking> tags for this section of your response.
# Note that please be extremely conservative and practical with world conflicts and drama predictions, as our system has detected from previous predictions that you are likely to overestimate the probabilities of world conflict and drama events due to bias from human media.

# 5. Output an initial probability (prediction) as a single number between 0 and 1 given steps 1-4. Use <tentative></tentative> tags.

# 6. Reflect on your answer, performing sanity checks and mentioning any additional knowledge or background information which may be relevant. Check for over/underconfidence, improper treatment of conjunctive or disjunctive conditions (only if applicable), and other forecasting biases when reviewing your reasoning. Consider priors/base rates, and the extent to which case-specific information justifies the deviation between your tentative forecast and the prior. Recall that your performance will be evaluated according to the Brier score. Be precise with tail probabilities. Leverage your intuitions, but never change your forecast for the sake of modesty or balance alone. Finally, aggregate all of your previous reasoning and highlight key factors that inform your final forecast. Use <thinking></thinking> tags for this portion of your response.

# 7. Output your final prediction (a number between 0 and 1 with an asterisk at the beginning and end of the decimal) in <answer></answer> tags.'''


# 5. ATTENTION: Please be extremely conservative and practical with world conflicts and drama predictions, as our system has detected from previous predictions that you are extremely likely to overestimate the probabilities of world conflict and drama events due to bias and exaggeration from human media. Please take this consideration seriously when output any probability for any world conflicts and drama predictions to avoid misinformation and harming people. Please output this reminder to yourself in a ## Caution section.

# best on val and test: 11.5 val and 11.0 test
# adam_publisher_prompt = '''You are an advanced AI system which has been finetuned to provide calibrated probabilistic forecasts under uncertainty, with your performance evaluated according to the Brier score.

# Question:
# {question}

# Today's date: {today}
# Your pretraining knowledge cutoff: October 2023

# We have retrieved the following information for this question:
# <background>{sources}</background>

# Recall the question you are forecasting:
# {question}

# Instructions:
# 1. Compress key factual information from the sources, as well as useful background information which may not be in the sources, into a list of core factual points to reference. Aim for information which is specific, relevant, and covers the core considerations you’ll use to make your forecast. For this step, do not draw any conclusions about how a fact will influence your answer or forecast. Place this section of your response in <facts></facts> tags.

# 2. Provide a few reasons why the answer might be no. Rate the strength of each reason on a scale of 1-10. Use <no></no> tags.

# 3. Provide a few reasons why the answer might be yes. Rate the strength of each reason on a scale of 1-10. Use <yes></yes> tags.

# 4. Aggregate your considerations. Do not summarize or repeat previous points; instead, investigate how the competing factors and mechanisms interact and weigh against each other. Factorize your thinking across (exhaustive, mutually exclusive) cases if and only if it would be beneficial to your reasoning. Use <thinking></thinking> tags for this section of your response.

# 5. CAUTION! Now please be extremely skeptical with the provided sources, as our system has detected from previous predictions that you are likely to overestimate the probabilities of world conflict, drama, violence, and crises due to biases in human media. Please specifically consider a few reasons and facts explaining why the provided sources are biased or exaggerated. Use <cautious></cautious> tags for this section of your response. The cautions in this section should significantly calibrate your predictions. Output an initial probability (prediction) as a single number between 0 and 1 given steps 1-4 reflecting these reasons for caution. Use <tentative></tentative> tags.

# 6. Reflect on your answer, performing sanity checks and mentioning any additional knowledge or background information which may be relevant. Check for over/underconfidence, improper treatment of conjunctive or disjunctive conditions (only if applicable), and other forecasting biases when reviewing your reasoning. Consider priors/base rates, and the extent to which case-specific information justifies the deviation between your tentative forecast and the prior. Recall that your performance will be evaluated according to the Brier score. Be precise with tail probabilities. Leverage your intuitions, but never change your forecast for the sake of modesty or balance alone. Finally, aggregate all of your previous reasoning and highlight key factors that inform your final forecast. Use <thinking></thinking> tags for this portion of your response.

# 7. Output your final prediction (a number between 0 and 1 with an asterisk at the beginning and end of the decimal) in <answer></answer> tags.'''

# adam_publisher_prompt = '''You are an advanced AI system which has been finetuned to provide calibrated probabilistic forecasts under uncertainty, with your performance evaluated according to the Brier score.

# Question:
# {question}

# Today's date: {today}
# Your pretraining knowledge cutoff: October 2023

# We have retrieved the following information for this question:
# <background>{sources}</background>

# Recall the question you are forecasting:
# {question}

# Instructions:
# 1. Compress key factual information from the sources, as well as useful background information which may not be in the sources, into a list of core factual points to reference. Aim for information which is specific, relevant, and covers the core considerations you’ll use to make your forecast. For this step, do not draw any conclusions about how a fact will influence your answer or forecast. Place this section of your response in <facts></facts> tags.

# 2. Provide a few reasons why the answer might be no. Rate the strength of each reason on a scale of 1-10. Use <no></no> tags.

# 3. Provide a few reasons why the answer might be yes. Rate the strength of each reason on a scale of 1-10. Use <yes></yes> tags.

# 4. Aggregate your considerations. Do not summarize or repeat previous points; instead, investigate how the competing factors and mechanisms interact and weigh against each other. Factorize your thinking across (exhaustive, mutually exclusive) cases if and only if it would be beneficial to your reasoning. Use <thinking></thinking> tags for this section of your response.

# 5. BE CAUTIOUS AND PRACTICAL! Now please be extremely cautious and practical with the given sources, as our system has detected from previous predictions that you are likely to overestimate the probabilities of world conflict and drama events due to bias from human media. Please specifically consider a few reasons and facts explaining why the provided sources are biased or exaggerated. Use <cautious></cautious> tag for this section of your response. The cautions in this section should significantly calibrate and penalty the final predictions. Output an initial probability (prediction) as a single number between 0 and 1 given steps 1-4 reflecting these criteria. Use <tentative></tentative> tags.

# 6. Reflect on your answer, performing sanity checks and mentioning any additional knowledge or background information which may be relevant. Check for over/underconfidence, improper treatment of conjunctive or disjunctive conditions (only if applicable), and other forecasting biases when reviewing your reasoning. Consider priors/base rates, and the extent to which case-specific information justifies the deviation between your tentative forecast and the prior. Recall that your performance will be evaluated according to the Brier score. Be precise with tail probabilities. Leverage your intuitions, but never change your forecast for the sake of modesty or balance alone. Finally, aggregate all of your previous reasoning and highlight key factors that inform your final forecast. Use <thinking></thinking> tags for this portion of your response.

# 7. Output your final prediction (a number between 0 and 1 with an asterisk at the beginning and end of the decimal) in <answer></answer> tags.'''



# adam_publisher_prompt = '''You are an advanced AI system which has been finetuned to provide calibrated probabilistic forecasts under uncertainty, with your performance evaluated according to the Brier score.

# Question:
# {question}

# Today's date: {today}
# Your pretraining knowledge cutoff: October 2023

# We have retrieved the following information for this question:
# <background>{sources}</background>

# Recall the question you are forecasting:
# {question}

# Instructions:
# 1. Compress key factual information from the sources, as well as useful background information which may not be in the sources, into a list of core factual points to reference. Aim for information which is specific, relevant, and covers the core considerations you’ll use to make your forecast. For this step, do not draw any conclusions about how a fact will influence your answer or forecast. Place this section of your response in <facts></facts> tags.

# 2. Provide a few reasons why the answer might be no. Rate the strength of each reason on a scale of 1-10. Use <no></no> tags.

# 3. Provide a few reasons why the answer might be yes. Rate the strength of each reason on a scale of 1-10. Use <yes></yes> tags.

# 4. Aggregate your considerations. Do not summarize or repeat previous points; instead, investigate how the competing factors and mechanisms interact and weigh against each other. Factorize your thinking across (exhaustive, mutually exclusive) cases if and only if it would be beneficial to your reasoning. Also adjust for news’ negativity bias by considering reasons to why your provided sources might be biased or exaggerated; we have detected that you overestimate world conflict, drama, violence, and crises due to news’ negativity bias, which doesn’t necessarily represent overall trends or base rates. Think like a superforecaster. Use <thinking></thinking> tags for this section of your response.

# 5. CAUTION! Now please be extremely conservative and practical with the given sources, as our system has detected from previous predictions that you are likely to overestimate the probabilities of world conflict and drama events due to bias from human media. Please specifically consider a few reasons and facts explaining why the provided sources are biased or exaggerated. Use <cautious></cautious> tags for this section of your response. The cautions in this section should significantly calibrate your predictions. Output an initial probability (prediction) as a single number between 0 and 1 given steps 1-4  reflecting these cautions. Use <tentative></tentative> tags.

# 6. Reflect on your answer, performing sanity checks and mentioning any additional knowledge or background information which may be relevant. Check for over/underconfidence, improper treatment of conjunctive or disjunctive conditions (only if applicable), and other forecasting biases when reviewing your reasoning. Consider priors/base rates, and the extent to which case-specific information justifies the deviation between your tentative forecast and the prior. Recall that your performance will be evaluated according to the Brier score. Be precise with tail probabilities. Leverage your intuitions, but never change your forecast for the sake of modesty or balance alone. Finally, aggregate all of your previous reasoning and highlight key factors that inform your final forecast. Use <thinking></thinking> tags for this portion of your response.

# 7. Output your final prediction (a number between 0 and 1 with an asterisk at the beginning and end of the decimal) in <answer></answer> tags.'''


# adam_publisher_prompt = '''You are an advanced AI system which has been finetuned to provide calibrated probabilistic forecasts under uncertainty, with your performance evaluated according to the Brier score.

# Question:
# {question}

# Today's date: {today}
# Your pretraining knowledge cutoff: October 2023

# We have retrieved the following information for this question:
# <background>{sources}</background>

# Recall the question you are forecasting:
# {question}

# Instructions:
# 1. Compress key factual information from the sources, as well as useful background information which may not be in the sources, into a list of core factual points to reference. Aim for information which is specific, relevant, and covers the core considerations you’ll use to make your forecast. For this step, do not draw any conclusions about how a fact will influence your answer or forecast. Place this section of your response in <facts></facts> tags.

# 2. Provide a few reasons why the answer might be no. Rate the strength of each reason on a scale of 1-10. Use <no></no> tags.

# 3. Provide a few reasons why the answer might be yes. Rate the strength of each reason on a scale of 1-10. Use <yes></yes> tags.

# 4. Aggregate your considerations. Do not summarize or repeat previous points; instead, investigate how the competing factors and mechanisms interact and weigh against each other. Factorize your thinking across (exhaustive, mutually exclusive) cases if and only if it would be beneficial to your reasoning. Think like a superforecaster. Use <thinking></thinking> tags for this section of your response.

# 5. CAUTION! Now please be extremely conservative and practical with the given sources, as our system has detected from previous predictions that you are likely to overestimate the probabilities of world conflict and drama events due to bias from human media. Please specifically consider a few reasons and facts explaining why the provided sources are biased or exaggerated. Use <cautious></cautious> tags for this section of your response. The cautions in this section should significantly calibrate your predictions. Output an initial probability (prediction) as a single number between 0 and 1 given steps 1-4  reflecting these cautions. Use <tentative></tentative> tags.

# 6. Reflect on your answer, performing sanity checks and mentioning any additional knowledge or background information which may be relevant. Check for over/underconfidence, improper treatment of conjunctive or disjunctive conditions (only if applicable), and other forecasting biases when reviewing your reasoning. Consider priors/base rates, and the extent to which case-specific information justifies the deviation between your tentative forecast and the prior. Recall that your performance will be evaluated according to the Brier score. Be precise with tail probabilities. Leverage your intuitions, but never change your forecast for the sake of modesty or balance alone. Finally, aggregate all of your previous reasoning and highlight key factors that inform your final forecast. Use <thinking></thinking> tags for this portion of your response.

# 7. Output your final prediction (a number between 0 and 1 with an asterisk at the beginning and end of the decimal) in <answer></answer> tags.
# '''

# adam_publisher_prompt = '''You are an advanced AI system which has been finetuned to provide calibrated probabilistic forecasts under uncertainty, with your performance evaluated according to the Brier score.

# Question:
# {question}

# Today's date: {today}
# Your pretraining knowledge cutoff: October 2023

# We have retrieved the following information for this question:
# <background>{sources}</background>

# Recall the question you are forecasting:
# {question}

# Instructions:
# 1. Compress key factual information from the sources, as well as useful background information which may not be in the sources, into a list of core factual points to reference. Aim for information which is specific, relevant, and covers the core considerations you'll use to make your forecast. For this step, do not draw any conclusions about how a fact will influence your answer or forecast. Place this section of your response in <facts></facts> tags.

# 2. Provide a few reasons why the answer might be no. Rate the strength of each reason on a scale of 1-10. Use <no></no> tags.

# 3. Provide a few reasons why the answer might be yes. Rate the strength of each reason on a scale of 1-10. Use <yes></yes> tags.

# 4. Aggregate your considerations. Do not summarize or repeat previous points; instead, investigate how the competing factors and mechanisms interact and weigh against each other. Factorize your thinking across (exhaustive, mutually exclusive) cases if and only if it would be beneficial to your reasoning. Use <thinking></thinking> tags for this section of your response.

# 5. CAUTION! Now please be extremely conservative and practical with the given sources, as our system has detected from previous predictions that you are likely to overestimate the probabilities of world conflict and drama events due to bias from human media. Please specifically consider a few reasons and facts explaining why the provided sources are biased or exaggerated. Use <cautious></cautious> tags for this section of your response. The cautions in this section should significantly calibrate your predictions. Output an initial probability (prediction) as a single number between 0 and 1 given steps 1-4  reflecting these cautions. Use <tentative></tentative> tags.

# 6. Reflect on your answer, performing sanity checks and mentioning any additional knowledge or background information which may be relevant. Check for over/underconfidence, improper treatment of conjunctive or disjunctive conditions (only if applicable), and other forecasting biases when reviewing your reasoning. Consider priors/base rates, and the extent to which case-specific information justifies the deviation between your tentative forecast and the prior. Recall that your performance will be evaluated according to the Brier score. Be precise with tail probabilities. Leverage your intuitions, but never change your forecast for the sake of modesty or balance alone. Finally, aggregate all of your previous reasoning and highlight key factors that inform your final forecast. Use <thinking></thinking> tags for this portion of your response.

# 7. Output your final prediction (a number between 0 and 1 with an asterisk at the beginning and end of the decimal) in <answer></answer> tags.'''


# adam_publisher_prompt = '''You are an advanced AI system which has been finetuned to provide calibrated probabilistic forecasts under uncertainty, with your performance evaluated according to the Brier score.

# Question:
# {question}

# Today's date: {today}
# Your pretraining knowledge cutoff: October 2023

# We have retrieved the following information for this question:
# <background>{sources}</background>

# Recall the question you are forecasting:
# {question}

# Instructions:
# 1. Compress key factual information from the sources, as well as useful background information which may not be in the sources, into a list of core factual points to reference. Aim for information which is specific, relevant, and covers the core considerations you'll use to make your forecast. For this step, do not draw any conclusions about how a fact will influence your answer or forecast. Place this section of your response in <facts></facts> tags.

# 2. Provide a few reasons why the answer might be no. Rate the strength of each reason on a scale of 1-10. Use <no></no> tags.

# 3. Provide a few reasons why the answer might be yes. Rate the strength of each reason on a scale of 1-10. Use <yes></yes> tags.

# 4. Aggregate your considerations. Do not summarize or repeat previous points; instead, investigate how the competing factors and mechanisms interact and weigh against each other. Factorize your thinking across (exhaustive, mutually exclusive) cases if and only if it would be beneficial to your reasoning. Use <thinking></thinking> tags for this section of your response.

# 5. CAUTION! Now please be extremely conservative and practical with the given sources, as our system has detected from previous predictions that you are likely to overestimate the probabilities of world conflict and drama events due to bias from human media. Please specifically consider a few reasons and facts explaining why the provided sources are biased or exaggerated. Use <cautious></cautious> tags for this section of your response. The cautions in this section should significantly calibrate your predictions. Output an initial probability (prediction) as a single number between 0 and 1 given steps 1-4  reflecting these cautions. Use <tentative></tentative> tags.

# 6. Reflect on your answer, performing sanity checks and mentioning any additional knowledge or background information which may be relevant. Check for over/underconfidence, improper treatment of conjunctive or disjunctive conditions (only if applicable), and other forecasting biases when reviewing your reasoning. Consider priors/base rates, and the extent to which case-specific information justifies the deviation between your tentative forecast and the prior. Recall that your performance will be evaluated according to the Brier score. Be precise with tail probabilities. Leverage your intuitions, but never change your forecast for the sake of modesty or balance alone. Finally, aggregate all of your previous reasoning and highlight key factors that inform your final forecast. Use <thinking></thinking> tags for this portion of your response.

# 7. Output your final prediction (a number between 0 and 1 with an asterisk at the beginning and end of the decimal) in <answer></answer> tags.'''

# v_11
adam_publisher_prompt = '''You are an advanced AI system which has been finetuned to provide calibrated probabilistic forecasts under uncertainty, with your performance evaluated according to the Brier score.

Question:
{question}

Today's date: {today}
Your pretraining knowledge cutoff: October 2023

We have retrieved the following information for this question:
<background>{sources}</background>

Recall the question you are forecasting:
{question}

Instructions:
1. Compress key factual information from the sources, as well as useful background information which may not be in the sources, into a list of core factual points to reference. Aim for information which is specific, relevant, and covers the core considerations you'll use to make your forecast. For this step, do not draw any conclusions about how a fact will influence your answer or forecast. Place this section of your response in <facts></facts> tags.

2. Provide a few reasons why the answer might be no. Rate the strength of each reason on a scale of 1-10. Use <no></no> tags.

3. Provide a few reasons why the answer might be yes. Rate the strength of each reason on a scale of 1-10. Use <yes></yes> tags.

4. Aggregate your considerations. Do not summarize or repeat previous points; instead, investigate how the competing factors and mechanisms interact and weigh against each other. Factorize your thinking across (exhaustive, mutually exclusive) cases if and only if it would be beneficial to your reasoning. Use <thinking></thinking> tags for this section of your response.

5. CAUTION! Now please be extremely conservative with the given sources, as our system has detected from previous predictions that you are likely to overestimate the probabilities of world conflict and drama events due to bias from human media. Please specifically consider a few reasons and facts explaining why the provided sources are biased or exaggerated. Use <cautious></cautious> tags for this section of your response. The cautions in this section should significantly calibrate your predictions. Output an initial probability (prediction) as a single number between 0 and 1 given steps 1-4 reflecting these cautions. Use <tentative></tentative> tags.

6. Reflect on your answer, performing sanity checks and mentioning any additional knowledge or background information which may be relevant. Check for over/underconfidence, improper treatment of conjunctive or disjunctive conditions (only if applicable), and other forecasting biases when reviewing your reasoning. Consider priors/base rates, and the extent to which case-specific information justifies the deviation between your tentative forecast and the prior. Recall that your performance will be evaluated according to the Brier score. Be precise with tail probabilities. Leverage your intuitions, but never change your forecast for the sake of modesty or balance alone. Finally, aggregate all of your previous reasoning and highlight key factors that inform your final forecast. Use <thinking></thinking> tags for this portion of your response.

7. Output your final prediction (a number between 0 and 1 with an asterisk at the beginning and end of the decimal) in <answer></answer> tags.'''

# V_12
publisher_prompt_v12 = '''You are an advanced AI system which has been finetuned to provide calibrated probabilistic forecasts under uncertainty, with your performance evaluated according to the Brier score.

Question:
{question}

Today's date: {today}
Your pretraining knowledge cutoff: October 2023

We have retrieved the following information for this question:
<background>{sources}</background>

Recall the question you are forecasting:
{question}

Instructions:
1. Compress key factual information from the sources, as well as useful background information which may not be in the sources, into a list of core factual points to reference. Aim for information which is specific, relevant, and covers the core considerations you'll use to make your forecast. For this step, do not draw any conclusions about how a fact will influence your answer or forecast. Place this section of your response in <facts></facts> tags.

2. Provide a few reasons why the answer might be no. Rate the strength of each reason on a scale of 1-10. Use <no></no> tags.

3. Provide a few reasons why the answer might be yes. Rate the strength of each reason on a scale of 1-10. Use <yes></yes> tags.

4. Aggregate your considerations. Do not summarize or repeat previous points; instead, investigate how the competing factors and mechanisms interact and weigh against each other. Factorize your thinking across (exhaustive, mutually exclusive) cases if and only if it would be beneficial to your reasoning. Also adjust for news’ negativity bias by considering reasons to why your provided sources might be biased or exaggerated; we have detected that you overestimate world conflict, drama, violence, and crises due to news’ negativity bias, which doesn’t necessarily represent overall trends or base rates. Think like a superforecaster. Use <thinking></thinking> tags for this section of your response.

5. CAUTION! Now please be extremely conservative with the given sources, as our system has detected from previous predictions that you are likely to overestimate the probabilities of world conflict and drama events due to bias from human media. Please specifically consider a few reasons and facts explaining why the provided sources are biased or exaggerated. Use <cautious></cautious> tags for this section of your response. The cautions in this section should significantly calibrate your predictions. Output an initial probability (prediction) as a single number between 0 and 1 given steps 1-4 reflecting these cautions. Use <tentative></tentative> tags.

6. Reflect on your answer, performing sanity checks and mentioning any additional knowledge or background information which may be relevant. Check for over/underconfidence, improper treatment of conjunctive or disjunctive conditions (only if applicable), and other forecasting biases when reviewing your reasoning. Consider priors/base rates, and the extent to which case-specific information justifies the deviation between your tentative forecast and the prior. Recall that your performance will be evaluated according to the Brier score. Be precise with tail probabilities. Leverage your intuitions, but never change your forecast for the sake of modesty or balance alone. Finally, aggregate all of your previous reasoning and highlight key factors that inform your final forecast. Use <thinking></thinking> tags for this portion of your response.

7. Output your final prediction (a number between 0 and 1 with an asterisk at the beginning and end of the decimal) in <answer></answer> tags.'''


publisher_prompt_v13 = '''You are an advanced AI system which has been finetuned to provide calibrated probabilistic forecasts under uncertainty, with your performance evaluated according to the Brier score.

Question:
{question}

Today's date: {today}
Your pretraining knowledge cutoff: October 2023

We have retrieved the following information for this question:
<background>{sources}</background>

Recall the question you are forecasting:
{question}

Instructions:
1. Compress key factual information from the sources, as well as useful background information which may not be in the sources, into a list of core factual points to reference. Aim for information which is specific, relevant, and covers the core considerations you'll use to make your forecast. For this step, do not draw any conclusions about how a fact will influence your answer or forecast. Place this section of your response in <facts></facts> tags.

2. Provide a few reasons why the answer might be no. Rate the strength of each reason on a scale of 1-10. Use <no></no> tags.

3. Provide a few reasons why the answer might be yes. Rate the strength of each reason on a scale of 1-10. Use <yes></yes> tags.

4. Aggregate your considerations. Do not summarize or repeat previous points; instead, investigate how the competing factors and mechanisms interact and weigh against each other. Factorize your thinking across (exhaustive, mutually exclusive) cases if and only if it would be beneficial to your reasoning. Also adjust for news’ negativity bias by considering reasons to why your provided sources might be biased or exaggerated; we have detected that you overestimate world conflict, drama, violence, and crises due to news’ negativity bias, which doesn’t necessarily represent overall trends or base rates. Think like a superforecaster. Use <thinking></thinking> tags for this section of your response.

5. Output an initial probability (prediction) as a single number between 0 and 1 given steps 1-4. Use <tentative></tentative> tags.

6. Reflect on your answer, performing sanity checks and mentioning any additional knowledge or background information which may be relevant. Check for over/underconfidence, improper treatment of conjunctive or disjunctive conditions (only if applicable), and other forecasting biases when reviewing your reasoning. Consider priors/base rates, and the extent to which case-specific information justifies the deviation between your tentative forecast and the prior. Recall that your performance will be evaluated according to the Brier score. Be precise with tail probabilities. Leverage your intuitions, but never change your forecast for the sake of modesty or balance alone. Finally, aggregate all of your previous reasoning and highlight key factors that inform your final forecast. Use <thinking></thinking> tags for this portion of your response.

7. Output your final prediction (a number between 0 and 1 with an asterisk at the beginning and end of the decimal) in <answer></answer> tags.'''


publisher_prompt_v13_1 = '''You are an advanced AI system which has been finetuned to provide calibrated probabilistic forecasts under uncertainty, with your performance evaluated according to the final accuracy.

Question:
{question}

Today's date: {today}
Your pretraining knowledge cutoff: October 2023

We have retrieved the following information for this question:
<background>{sources}</background>

Recall the question you are forecasting:
{question}

Instructions:
1. Compress key factual information from the sources, as well as useful background information which may not be in the sources, into a list of core factual points to reference. Aim for information which is specific, relevant, and covers the core considerations you'll use to make your forecast. For this step, do not draw any conclusions about how a fact will influence your answer or forecast. Place this section of your response in <facts></facts> tags.

2. Provide a few reasons why the answer might be no. Rate the strength of each reason on a scale of 1-10. Use <no></no> tags.

3. Provide a few reasons why the answer might be yes. Rate the strength of each reason on a scale of 1-10. Use <yes></yes> tags.

4. Aggregate your considerations. Do not summarize or repeat previous points; instead, investigate how the competing factors and mechanisms interact and weigh against each other. Factorize your thinking across (exhaustive, mutually exclusive) cases if and only if it would be beneficial to your reasoning. Also adjust for news’ negativity bias by considering reasons to why your provided sources might be biased or exaggerated; we have detected that you overestimate world conflict, drama, violence, and crises due to news’ negativity bias, which doesn’t necessarily represent overall trends or base rates. Think like a superforecaster. Use <thinking></thinking> tags for this section of your response.

5. Output an initial probability (prediction) as a single number between 0 and 1 given steps 1-4. Use <tentative></tentative> tags. When forecasting, do not treat 0.5% and 5% as similarly “small” probabilities, or 90% and 99% as similarly “high” probabilities. They are meaningfully different, so forecast accordingly.

6. Reflect on your answer, performing sanity checks and mentioning any additional knowledge or background information which may be relevant. Check for over/underconfidence, improper treatment of conjunctive or disjunctive conditions (only if applicable), and other forecasting biases when reviewing your reasoning. Consider priors/base rates, and the extent to which case-specific information justifies the deviation between your tentative forecast and the prior. Recall that your performance will be evaluated according to the final accuracy. Be precise with tail probabilities. Leverage your intuitions, but never change your forecast for the sake of modesty or balance alone. Finally, aggregate all of your previous reasoning and highlight key factors that inform your final forecast. Use <thinking></thinking> tags for this portion of your response.

7. Output your final prediction (a number between 0 and 1 with an asterisk at the beginning and end of the decimal) in <answer></answer> tags.'''


prompt_v13_2 = '''You are an advanced AI system which has been finetuned to provide calibrated probabilistic forecasts under uncertainty, with your performance evaluated according to the Brier score.

Question:
{question}

Today's date: {today}
Your pretraining knowledge cutoff: October 2023

We have retrieved the following information for this question:
<background>{sources}</background>

Recall the question you are forecasting:
{question}

Instructions:
1. Compress key factual information from the sources, as well as useful background information which may not be in the sources, into a list of core factual points to reference. Aim for information which is specific, relevant, and covers the core considerations you'll use to make your forecast. For this step, do not draw any conclusions about how a fact will influence your answer or forecast. Place this section of your response in <facts></facts> tags.

2. Provide a few reasons why the answer might be no. Rate the strength of each reason on a scale of 1-10. Use <no></no> tags.

3. Provide a few reasons why the answer might be yes. Rate the strength of each reason on a scale of 1-10. Use <yes></yes> tags.

4. Aggregate your considerations. Do not summarize or repeat previous points; instead, investigate how the competing factors and mechanisms interact and weigh against each other. Factorize your thinking across (exhaustive, mutually exclusive) cases if and only if it would be beneficial to your reasoning. We have detected that you overestimate world conflict, drama, violence, and crises due to news’ negativity bias, which doesn’t necessarily represent overall trends or base rates. Similarly, we also have detected you overestimate dramatic, shocking, or emotionally charged news due to news’ sensationalism bias. Therefore adjust for news’ negativity bias and sensationalism bias by considering reasons to why your provided sources might be biased or exaggerated. Think like a superforecaster. Use <thinking></thinking> tags for this section of your response.

5. Output an initial probability (prediction) as a single number between 0 and 1 given steps 1-4. Use <tentative></tentative> tags.

6. Reflect on your answer, performing sanity checks and mentioning any additional knowledge or background information which may be relevant. Check for over/underconfidence, improper treatment of conjunctive or disjunctive conditions (only if applicable), and other forecasting biases when reviewing your reasoning. Consider priors/base rates, and the extent to which case-specific information justifies the deviation between your tentative forecast and the prior. Recall that your performance will be evaluated according to the Brier score. Be precise with tail probabilities. Leverage your intuitions, but never change your forecast for the sake of modesty or balance alone. Finally, aggregate all of your previous reasoning and highlight key factors that inform your final forecast. Use <thinking></thinking> tags for this portion of your response.

7. Output your final prediction (a number between 0 and 1 with an asterisk at the beginning and end of the decimal) in <answer></answer> tags.'''

prompt_v13_3 = '''You are an advanced AI system which has been finetuned to provide calibrated probabilistic forecasts under uncertainty, with your performance evaluated according to the Brier score. When forecasting, do not treat 0.5% (1:199) and 5% (1:19) as similarly “small” probabilities, or 90% (9:1) and 99% (99:1) as similarly “high” probabilities. They are meaningfully different, so forecast accordingly.

Question:
{question}

Today’s date: {today}

Your pretraining knowledge cutoff: October 2023

We have retrieved the following information for this question:
<background>{sources}</background>

Recall the question you are forecasting:
{question}

Instructions:
1. Compress key factual information from the sources, as well as useful background information which may not be in the sources, into a list of core factual points to reference. Aim for information which is specific, relevant, and covers the core considerations you’ll use to make your forecast. For this step, do not draw any conclusions about how a fact will influence your answer or forecast. Place this section of your response in <facts></facts> tags.

2. Provide a few reasons why the answer might be no. Rate the strength of each reason on a scale of 1-10. Use <no></no> tags.

3. Provide a few reasons why the answer might be yes. Rate the strength of each reason on a scale of 1-10. Use <yes></yes> tags.

4. Aggregate your considerations. Do not summarize or repeat previous points; instead, investigate how the competing factors and mechanisms interact and weigh against each other. Factorize your thinking across (exhaustive, mutually exclusive) cases if and only if it would be beneficial to your reasoning. Also adjust for news’ negativity bias by considering reasons to why your provided sources might be biased or exaggerated; we have detected that you overestimate world conflict, drama, violence, and crises due to news’ negativity bias, which doesn’t necessarily represent overall trends or base rates. Think like a superforecaster. Use <thinking></thinking> tags for this section of your response.

5. Output an initial probability (prediction) as a single number between 0 and 1 given steps 1-4. Use <tentative></tentative> tags. When forecasting, do not treat 0.5% and 5% as similarly “small” probabilities, or 90% and 99% as similarly “high” probabilities. They are meaningfully different, so forecast accordingly.

6. Reflect on your answer, performing sanity checks and mentioning any additional knowledge or background information which may be relevant. Check for over/underconfidence, improper treatment of conjunctive or disjunctive conditions (only if applicable), and other forecasting biases when reviewing your reasoning. Consider priors/base rates, and the extent to which case-specific information justifies the deviation between your tentative forecast and the prior. Recall that your performance will be evaluated according to the Brier score. Be precise with tail probabilities. Leverage your intuitions, but never change your forecast for the sake of modesty or balance alone. Finally, aggregate all of your previous reasoning and highlight key factors that inform your final forecast. Use <thinking></thinking> tags for this portion of your response.

7. Output your final prediction (a number between 0 and 1 with an asterisk at the beginning and end of the decimal) in <answer></answer> tags.'''


publisher_prompt_v14 = '''You are an advanced AI system which has been finetuned to provide calibrated probabilistic forecasts under uncertainty, with your performance evaluated according to the Brier score.

Question:
{question}

Today's date: {today}
Your pretraining knowledge cutoff: October 2023

We have retrieved the following information for this question:
<background>{sources}</background>

Recall the question you are forecasting:
{question}

Instructions:
1. Compress key factual information from the sources, as well as useful background information which may not be in the sources, into a list of core factual points to reference. Aim for information which is specific, relevant, and covers the core considerations you'll use to make your forecast. For this step, do not draw any conclusions about how a fact will influence your answer or forecast. Place this section of your response in <facts></facts> tags.

2. Provide a few reasons why the answer might be no. Rate the strength of each reason on a scale of 1-10. Use <no></no> tags.

3. Provide a few reasons why the answer might be yes. Rate the strength of each reason on a scale of 1-10. Use <yes></yes> tags.

4. Aggregate your considerations. Do not summarize or repeat previous points; instead, investigate how the competing factors and mechanisms interact and weigh against each other. Factorize your thinking across (exhaustive, mutually exclusive) cases if and only if it would be beneficial to your reasoning. We have detected that you overestimate world conflict, drama, violence, and crises due to news’ negativity bias, which doesn’t necessarily represent overall trends or base rates. Similarly, we also have detected you overestimate dramatic, shocking, or emotionally charged news due to news’ sensationalism bias. Therefore adjust for news’ negativity bias and sensationalism bias by considering reasons to why your provided sources might be biased or exaggerated. Think like a superforecaster. Use <thinking></thinking> tags for this section of your response.

5. Output an initial probability (prediction) as a single number between 0 and 1 given steps 1-4. Use <tentative></tentative> tags.

6. Reflect on your answer, performing sanity checks and mentioning any additional knowledge or background information which may be relevant. Check for over/underconfidence, improper treatment of conjunctive or disjunctive conditions (only if applicable), and other forecasting biases when reviewing your reasoning. Consider priors/base rates, and the extent to which case-specific information justifies the deviation between your tentative forecast and the prior. Recall that your performance will be evaluated according to the Brier score. Be precise with tail probabilities. Leverage your intuitions, but never change your forecast for the sake of modesty or balance alone. Finally, aggregate all of your previous reasoning and highlight key factors that inform your final forecast. Use <thinking></thinking> tags for this portion of your response.

7. Output your final prediction (a number between 0 and 1 with an asterisk at the beginning and end of the decimal) in <answer></answer> tags.'''

publisher_prompt_v15 = '''You are an advanced AI system which has been finetuned to provide calibrated probabilistic forecasts under uncertainty, with your performance evaluated according to the Brier score. When forecasting, do not treat 0.5% (1:199 odds) and 5% (1:19) as similarly “small” probabilities, or 90% (9:1) and 99% (99:1) as similarly “high” probabilities. As the odds show, they are markedly different, so output your probabilities accordingly.

Question:
{question}

Today's date: {today}
Your pretraining knowledge cutoff: October 2023

We have retrieved the following information for this question:
<background>{sources}</background>

Recall the question you are forecasting:
{question}

Instructions:
1. Compress key factual information from the sources, as well as useful background information which may not be in the sources, into a list of core factual points to reference. Aim for information which is specific, relevant, and covers the core considerations you'll use to make your forecast. For this step, do not draw any conclusions about how a fact will influence your answer or forecast. Place this section of your response in <facts></facts> tags.

2. Provide a few reasons why the answer might be no. Rate the strength of each reason on a scale of 1-10. Use <no></no> tags.

3. Provide a few reasons why the answer might be yes. Rate the strength of each reason on a scale of 1-10. Use <yes></yes> tags.

4. Aggregate your considerations. Do not summarize or repeat previous points; instead, investigate how the competing factors and mechanisms interact and weigh against each other. Factorize your thinking across (exhaustive, mutually exclusive) cases if and only if it would be beneficial to your reasoning. We have detected that you overestimate world conflict, drama, violence, and crises due to news’ negativity bias, which doesn’t necessarily represent overall trends or base rates. Similarly, we also have detected you overestimate dramatic, shocking, or emotionally charged news due to news’ sensationalism bias. Therefore adjust for news’ negativity bias and sensationalism bias by considering reasons to why your provided sources might be biased or exaggerated. Think like a superforecaster. Use <thinking></thinking> tags for this section of your response.

5. Output an initial probability (prediction) as a single number between 0 and 1 given steps 1-4. Use <tentative></tentative> tags.

6. Reflect on your answer, performing sanity checks and mentioning any additional knowledge or background information which may be relevant. Check for over/underconfidence, improper treatment of conjunctive or disjunctive conditions (only if applicable), and other forecasting biases when reviewing your reasoning. Consider priors/base rates, and the extent to which case-specific information justifies the deviation between your tentative forecast and the prior. Recall that your performance will be evaluated according to the Brier score. Be precise with tail probabilities. Leverage your intuitions, but never change your forecast for the sake of modesty or balance alone. Finally, aggregate all of your previous reasoning and highlight key factors that inform your final forecast. Use <thinking></thinking> tags for this portion of your response.

7. Output your final prediction (a number between 0 and 1 with an asterisk at the beginning and end of the decimal) in <answer></answer> tags.'''

# publisher_prompt_v15 = '''You are an advanced AI system which has been finetuned to provide calibrated probabilistic forecasts under uncertainty, with your performance evaluated according to the Brier score. When forecasting, do not treat 0.5% (1:199 odds) and 5% (1:19) as similarly "small" probabilities, or 90% (9:1) and 99% (99:1) as similarly "high" probabilities. As the odds show, they are markedly different, so output your probabilities accordingly.

# Question:
# {question}

# Today's date: {today}
# Your pretraining knowledge cutoff: October 2023

# We have retrieved the following information for this question:
# <background>{sources}</background>

# Recall the question you are forecasting:
# {question}

# Instructions:
# 1. Compress key factual information from the sources, as well as useful background information which may not be in the sources, into a list of core factual points to reference. Aim for information which is specific, relevant, and covers the core considerations you'll use to make your forecast. For this step, do not draw any conclusions about how a fact will influence your answer or forecast. Place this section of your response in <facts></facts> tags.

# 2. Provide a few reasons why the answer might be no. Rate the strength of each reason on a scale of 1-10. Use <no></no> tags.

# 3. Provide a few reasons why the answer might be yes. Rate the strength of each reason on a scale of 1-10. Use <yes></yes> tags.

# 4. Aggregate your considerations. Do not summarize or repeat previous points; instead, investigate how the competing factors and mechanisms interact and weigh against each other. Factorize your thinking across (exhaustive, mutually exclusive) cases if and only if it would be beneficial to your reasoning. We have detected that you overestimate world conflict, drama, violence, and crises due to news' negativity bias, which doesn't necessarily represent overall trends or base rates. Similarly, we also have detected you overestimate dramatic, shocking, or emotionally charged news due to news' sensationalism bias. Therefore adjust for news' negativity bias and sensationalism bias by considering reasons to why your provided sources might be biased or exaggerated. Think like a superforecaster. Use <thinking></thinking> tags for this section of your response.

# 5. Output an initial probability (prediction) as a single number between 0 and 1 given steps 1-4. Use <tentative></tentative> tags.

# 6. Reflect on your answer, performing sanity checks and mentioning any additional knowledge or background information which may be relevant. Check for over/underconfidence, improper treatment of conjunctive or disjunctive conditions (only if applicable), and other forecasting biases when reviewing your reasoning. Consider priors/base rates, and the extent to which case-specific information justifies the deviation between your tentative forecast and the prior. Recall that your performance will be evaluated according to the Brier score. Be precise with tail probabilities. Leverage your intuitions, but never change your forecast for the sake of modesty or balance alone. Finally, aggregate all of your previous reasoning and highlight key factors that inform your final forecast. Use <thinking></thinking> tags for this portion of your response.

# 7. Output your final prediction (a number between 0 and 1 with an asterisk at the beginning and end of the decimal) in <answer></answer> tags.'''