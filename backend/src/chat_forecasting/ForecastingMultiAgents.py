import re
from typing import List
from chat_forecasting.llm_agent import get_llm_agent_class, O1OpenAIAgent
from chat_forecasting.research_agent import ResearchAgent
from chat_forecasting.related_forecast_agent import RelatedForecastAgent

from chat_forecasting.prompts import PLANNER_PROMPT, PUBLISHER_PROMPT
from chat_forecasting.parse_date import GOOGLE_SEARCH_DATE_FORMAT
import asyncio
import os
import json
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
ENV_TYPE = os.getenv('ENV_TYPE')

class ForecastingMultiAgents:
    def __init__(self, model: str ="gpt-4o-mini", 
                 summarize_model: str="grok-3-mini-beta",
                 breadth: int =5, 
                 planner_prompt: str =None, 
                 publisher_prompt: str =None, 
                 search_type: str='news', 
                 before_timestamp: int = None,
                 factorize_prompt: str=None):
        serper_api_key = os.getenv("SERPER_API_KEY")
        
        # query -> plannerAgent -> search queries -> researchAgent based on search queries -> concatenated markdown text -> publisherAgnet
        if "o1" not in model and "o3" not in model:
            self.plannerAgent = get_llm_agent_class(model)(model=model, temperature=0.0, max_tokens=512)
        else:
            self.plannerAgent = get_llm_agent_class("gpt-4o")(model="gpt-4o", temperature=0.0, max_tokens=512)
            
        self.researchAgent = ResearchAgent(serper_api_key=serper_api_key, summarize_model=summarize_model, search_type=search_type, breadth=breadth, before_timestamp=before_timestamp)
        self.factorizeAgent = get_llm_agent_class(model)(model=model, temperature=0.0, max_tokens=2048)
        self.publisherAgent = get_llm_agent_class(model)(model=model, temperature=0.0, max_tokens=2048)

        self.planner_prompt = planner_prompt or PLANNER_PROMPT
        self.publisher_prompt = publisher_prompt or PUBLISHER_PROMPT
        self.factorize_prompt = factorize_prompt 
        self.breadth = breadth

        if self.researchAgent.before_date_str:
            self.today_string = self.researchAgent.before_date_str
        else: 
            self.today_string = datetime.now().strftime(GOOGLE_SEARCH_DATE_FORMAT)

        if ENV_TYPE == "prod":
            self.related_forecast_agent = RelatedForecastAgent(model="gpt-4o-mini")
        else:
            self.related_forecast_agent = None

    def extract_queries(self, input_str: str, use_xml: bool = False) -> List[str]:
        if not use_xml:
            # Pattern for numbered lines
            pattern = r'^\d+\.\s*(.+)$'
            queries = re.findall(pattern, input_str, re.MULTILINE)
        else:
            # Pattern for <sub_forecast> tags
            pattern = r'<query>(.+?)</query>'
            queries = re.findall(pattern, input_str)
        
        cleaned_queries = [re.sub(r'[\'"`]', '', query).strip() for query in queries]
        cleaned_queries = [c for c in cleaned_queries if c][-self.breadth:]

        return cleaned_queries
        
    def format_research_results(self, research_results):
        template = "ID: {id}\nQuery: {query}\nTitle: {title}\nDate: {date}\nContent:\n[start content]{content}\n[end content]"

        contents = []
        for id, res in enumerate(research_results, start=1):
            content = template.format(id=id, query=res['query'], title=res['title'], date=res['date'], content=res['summarized_content'])
            contents.append(content)
        return "\n\n----\n\n".join(contents)
    
    def format_factorized_results(self, factorized_results):
        template = "Question {id}: {query}\nForecasting: {forecast}"
        contents = []
        for id, res in enumerate(factorized_results, start=1):
            content = template.format(id=id, query=res['query'], forecast=res['forecast'])
            contents.append(content)
        return "\n\n----\n\n".join(contents)

    def extract_prediction(self, prediction_str):
        # Find the first number (integer or float) in the string
        match = re.search(r'(\d+(\.\d+)?)', prediction_str)
        if match:
            return float(match.group(1))
        return None
    
    async def completions(self, messages, depth=0):
        # Step 1 calling plannerAgent to generate search queries
        question = messages[-1]['content']
        if self.breadth < 1:
            research_results = []
        else:
            planner_query = self.planner_prompt.format(question=question, breadth=self.breadth, today=self.today_string)
            planner_input = [dict(role="user", content=planner_query)]
            planner_response = self.plannerAgent.completions(planner_input)   
                     
            if planner_response == self.plannerAgent.default_outputs:
                yield planner_response
            search_queries = self.extract_queries(planner_response, use_xml=True) 

            # Step 2 calling researchAgent to generate research content from search queries
            research_results = []
            async for result in self.researchAgent.research(search_queries, question=question):
                research_results = result  # Get the last yielded result
            yield json.dumps(research_results) + '[SEP_SOURCE]'
            
            if not research_results:
                print("planner_response=", planner_response)

        formated_research_results = self.format_research_results(research_results)
        # yield json.dumps(research_results_dicts) + '[SEP_SOURCE]'

        # Step 3 publishing results
        publishing_query = self.publisher_prompt.format(sources=formated_research_results, today=self.today_string, question=question)
        publishing_input = [dict(role="user", content=publishing_query)]
        # input = planner_input + [dict(role="assistant", content=planner_response)] + publishing_input
        input = publishing_input
    
        if not isinstance(self.publisherAgent, O1OpenAIAgent):
            response = await self.publisherAgent.completions_stream(input)
            async for chunk in response:
                yield chunk
        else:
            response = self.publisherAgent.completions(input)
            yield response

async def forecasting_search_completions(messages: List, model: str):
    multi_agents = ForecastingMultiAgents(model)
    response = multi_agents.completions(messages)
    async for chunk in response:
        yield chunk

async def main():
    # Initialize forecastingMultiAgents
    serper_api_key = os.getenv("SERPER_API_KEY")
    multi_agents = ForecastingMultiAgents(serper_api_key)

    # results = await multi_agents.completions(question)

    # print(results)



if __name__ == "__main__":
    asyncio.run(main())