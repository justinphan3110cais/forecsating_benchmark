import re
from typing import List
from chat_forecasting.llm_agent import get_llm_agent_class
from chat_forecasting.research_agent import ResearchAgent
from chat_forecasting.prompts import PLANNER_PROMPT, PUBLISHER_PROMPT
from chat_forecasting.parse_date import GOOGLE_SEARCH_DATE_FORMAT
import asyncio
import os
import json
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

class ForecastingMultiAgents:
    def __init__(self, model: str ="gpt-4o-mini", 
                 breadth: int =5, 
                 planner_prompt: str =None, 
                 publisher_prompt: str =None, 
                 search_type: str='news', 
                 before_timestamp: int = None):
        serper_api_key = os.getenv("SERPER_API_KEY")
        
        # query -> plannerAgent -> search queries -> researchAgent based on search queries -> concatenated markdown text -> publisherAgnet
        self.plannerAgent = get_llm_agent_class(model)(model=model, temperature=0.0, max_tokens=512)
        self.researchAgent = ResearchAgent(serper_api_key=serper_api_key, search_type=search_type, before_timestamp=before_timestamp)
        self.publisherAgent = get_llm_agent_class(model)(model=model, temperature=0.0, max_tokens=2048)

        self.planner_prompt = planner_prompt or PLANNER_PROMPT
        self.publisher_prompt = publisher_prompt or PUBLISHER_PROMPT
        self.breadth = breadth

        if self.researchAgent.before_date_str:
            self.today_string = self.researchAgent.before_date_str
        else: 
            self.today_string = datetime.now().strftime(GOOGLE_SEARCH_DATE_FORMAT)


    
    def extract_queries(self, str: str) -> List[str]:
        # Use regex to find numbered lines
        pattern = r'^\d+\.\s*(.+)$'
        queries = re.findall(pattern, str, re.MULTILINE)
        cleaned_queries = [re.sub(r'[\'"`]', '', query).strip() for query in queries]
        cleaned_queries = [c for c in cleaned_queries if c]
        
        return cleaned_queries
    
    def format_research_results(self, research_results):
        template = "ID: {id}\nQuery: {query}\nTitle: {title}\nDate: {date}\nContent:\n[start content]{content}\n[end content]"
        contents = []
        for id, res in enumerate(research_results, start=1):
            content = template.format(id=id, query=res['query'], title=res['title'], date=res['date'], content=res['content'])
            contents.append(content)
        return "\n\n----\n\n".join(contents)
    
    async def completions(self, messages):
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
            search_queries = self.extract_queries(planner_response)
            
            # Step 2 calling researchAgent to generate research content from search queries
            search_queries = [s for s in search_queries]

            research_results = await self.researchAgent.research(search_queries)

        # return result schema
        research_results_str = [dict(id=i, **{k: v for k, v in r.items()}) 
                                for i, r in enumerate(research_results, start=1)] 
        research_results_str = json.dumps(research_results_str)
        yield research_results_str + '[SEP_SOURCE]'

        # Step 3 publishing results
        formated_research_results = self.format_research_results(research_results)
        publishing_query = self.publisher_prompt.format(sources=formated_research_results, today=self.today_string, question=question)
        publishing_input = [dict(role="user", content=publishing_query)]
        input = planner_input + [dict(role="assistant", content=planner_response)] + publishing_input
        response = await self.publisherAgent.completions_stream([dict(role="user", content=publishing_query)])
        
        async for chunk in response:
            yield chunk

async def forecasting_search_completions(messages: List, model: str):
    multi_agents = ForecastingMultiAgents(model)
    response = multi_agents.completions(messages)
    async for chunk in response:
        yield chunk

async def main():
    # Initialize forecastingMultiAgents
    serper_api_key = "00cad34a3001b5d34b9a74a00f9cf06a6a42d891"
    multi_agents = ForecastingMultiAgents(serper_api_key)

    # results = await multi_agents.completions(question)

    # print(results)



if __name__ == "__main__":
    asyncio.run(main())