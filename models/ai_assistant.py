import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
import time
import json
import logging

class AIResearchAssistant:
    def __init__(self, performance_logger):
        # Load environment variables
        load_dotenv()
        
        # Get API key from environment
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("No Google API key found. Please set GOOGLE_API_KEY in .env")

        # Initialize the LLM with detailed configuration
        self.llm = ChatGoogleGenerativeAI(
            google_api_key=api_key,
            model="gemini-1.5-flash",
            temperature=0.7,
            max_output_tokens=2048
        )
        
        self.performance_logger = performance_logger
    
    def generate_response(self, query):
        try:
            messages = [
                SystemMessage(content="You are an advanced research assistant. Provide comprehensive, well-structured responses."),
                HumanMessage(content=query)
            ]
            
            input_tokens = len(' '.join([msg.content for msg in messages]).split())
            start_time = time.time()
            
            response = self.llm.invoke(messages)
            
            duration = time.time() - start_time
            output_tokens = len(response.content.split())
            
            self.performance_logger.log_api_call(
                query=query, 
                input_tokens=input_tokens, 
                output_tokens=output_tokens, 
                duration=duration
            )
            
            return response.content
            
        except Exception as e:
            self.performance_logger.log_api_call(
                query=query, 
                input_tokens=0, 
                output_tokens=0, 
                duration=0,
                success=False,
                error=str(e)
            )
            logging.error(f"API Call Error: {e}")
            raise
    
    def research_workflow(self, topic):
        try:
            research_steps = [
                f"Generate a comprehensive overview of {topic}",
                f"List key subtopics and important aspects of {topic}",
                f"Provide historical context for {topic}",
                f"Discuss current trends and future implications of {topic}"
            ]
            
            research_results = {}
            for step in research_steps:
                result = self.generate_response(step)
                research_results[step] = result
            
            synthesis_prompt = f"Synthesize a comprehensive research report on {topic} using these key sections: {json.dumps(list(research_results.keys()))}"
            final_report = self.generate_response(synthesis_prompt)
            
            return {
                "detailed_sections": research_results,
                "final_report": final_report
            }
            
        except Exception as e:
            logging.error(f"Research Workflow Error: {e}")
            raise