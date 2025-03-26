import os
import sys
import time
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import Langtrace
from langtrace_python_sdk import langtrace

# Initialize Langtrace with comprehensive settings
langtrace.init(
    api_key=os.getenv('LANGTRACE_API_KEY'),
    service_name="ai_research_assistant",
    write_spans_to_console=True
)

# Import required libraries
import json
from opentelemetry import trace
from typing import Dict, Any, List

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('ai_assistant_log.txt')
    ]
)

# Import LLM and related libraries
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

class AIResearchAssistant:
    def __init__(self):
        # Get tracer for detailed tracing
        self.tracer = trace.get_tracer(__name__)
        
        # Initialize the LLM with detailed configuration
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.7,
            max_output_tokens=2048
        )
        
        # Performance and usage tracking
        self.total_api_calls = 0
        self.total_tokens_used = 0
        self.api_call_times = []
    
    def track_api_performance(self, start_time: float, input_tokens: int, output_tokens: int):
        """
        Track detailed performance metrics for each API call
        
        Args:
            start_time (float): Start time of the API call
            input_tokens (int): Number of input tokens
            output_tokens (int): Number of output tokens
        """
        end_time = time.time()
        call_duration = end_time - start_time
        
        # Record performance metrics
        self.total_api_calls += 1
        self.total_tokens_used += (input_tokens + output_tokens)
        self.api_call_times.append(call_duration)
        
        # Log performance details
        logging.info(f"API Call Performance:")
        logging.info(f"  Duration: {call_duration:.4f} seconds")
        logging.info(f"  Input Tokens: {input_tokens}")
        logging.info(f"  Output Tokens: {output_tokens}")
    
    def generate_response(self, query: str, context: Dict[str, Any] = None) -> str:
        """
        Generate a response with comprehensive tracing and performance monitoring
        
        Args:
            query (str): User's input query
            context (dict, optional): Additional context for the query
        
        Returns:
            str: Generated response
        """
        # Start a detailed trace span
        with self.tracer.start_as_current_span("generate_response") as span:
            try:
                # Add context attributes to the span
                if context:
                    for key, value in context.items():
                        span.set_attribute(f"context.{key}", str(value))
                
                # Prepare detailed messages
                messages = [
                    SystemMessage(content="You are an advanced research assistant. Provide comprehensive, well-structured responses."),
                    HumanMessage(content=query)
                ]
                
                # Track input tokens (simulated)
                input_tokens = len(' '.join([msg.content for msg in messages]).split())
                
                # Measure API call time
                start_time = time.time()
                
                # Invoke LLM with tracing
                response = self.llm.invoke(messages)
                
                # Track output tokens (simulated)
                output_tokens = len(response.content.split())
                
                # Track performance
                self.track_api_performance(start_time, input_tokens, output_tokens)
                
                # Add span attributes for debugging
                span.set_attribute("input.query", query)
                span.set_attribute("output.length", len(response.content))
                span.set_attribute("input_tokens", input_tokens)
                span.set_attribute("output_tokens", output_tokens)
                
                return response.content
            
            except Exception as e:
                # Detailed error tracking
                span.record_exception(e)
                logging.error(f"API Call Error: {e}")
                raise
    
    def research_workflow(self, topic: str) -> Dict[str, Any]:
        """
        Comprehensive research workflow with multiple traced steps
        
        Args:
            topic (str): Research topic
        
        Returns:
            dict: Comprehensive research results
        """
        with self.tracer.start_as_current_span("research_workflow"):
            try:
                # Define research steps
                research_steps = [
                    f"Generate a comprehensive overview of {topic}",
                    f"List key subtopics and important aspects of {topic}",
                    f"Provide historical context for {topic}",
                    f"Discuss current trends and future implications of {topic}"
                ]
                
                # Trace each research step
                research_results = {}
                for step in research_steps:
                    with self.tracer.start_as_current_span(f"research_step_{step}"):
                        result = self.generate_response(step)
                        research_results[step] = result
                
                # Synthesize final research report
                synthesis_prompt = f"Synthesize a comprehensive research report on {topic} using these key sections: {json.dumps(list(research_results.keys()))}"
                final_report = self.generate_response(synthesis_prompt)
                
                return {
                    "detailed_sections": research_results,
                    "final_report": final_report
                }
            
            except Exception as e:
                logging.error(f"Research Workflow Error: {e}")
                raise
    
    def generate_performance_report(self) -> str:
        """
        Generate a detailed performance and usage report
        
        Returns:
            str: Formatted performance report
        """
        avg_call_time = sum(self.api_call_times) / len(self.api_call_times) if self.api_call_times else 0
        
        report = f"""
        === AI Assistant Performance Report ===
        Total API Calls: {self.total_api_calls}
        Total Tokens Used: {self.total_tokens_used}
        Average API Call Duration: {avg_call_time:.4f} seconds
        Fastest API Call: {min(self.api_call_times):.4f} seconds
        Slowest API Call: {max(self.api_call_times):.4f} seconds
        """
        
        return report

def main():
    # Create AI Research Assistant
    assistant = AIResearchAssistant()
    
    while True:
        try:
            # User interaction
            topic = input("\nEnter a research topic (or 'quit' to exit, 'report' for performance): ")
            
            if topic.lower() == 'quit':
                break
            
            if topic.lower() == 'report':
                print(assistant.generate_performance_report())
                continue
            
            # Perform research with comprehensive tracing
            print(f"\n===== Researching: {topic} =====")
            research_result = assistant.research_workflow(topic)
            
            # Display research results
            print("\n----- Final Research Report -----")
            print(research_result['final_report'])
        
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            break
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()