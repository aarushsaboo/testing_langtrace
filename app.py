import os
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

# Import Langtrace SDK
from langtrace_python_sdk import langtrace

# Initialize Langtrace with environment variables
langtrace.init(
    api_key=os.getenv('LANGTRACE_API_KEY'),
    service_name="langtrace_demo_app"
)

# Import other required libraries
import sys
import time
from opentelemetry import trace
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

class LangtraceDemo:
    def __init__(self):
        # Get tracer
        self.tracer = trace.get_tracer(__name__)
        
        # Initialize the LLM
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.7,
            max_output_tokens=1024
        )
    
    def generate_response(self, query):
        """
        Generate a response using the LLM with OpenTelemetry tracing
        
        Args:
            query (str): User's input query
        
        Returns:
            str: LLM's generated response
        """
        # Use context manager for tracing
        with self.tracer.start_as_current_span("generate_response"):
            try:
                # Prepare messages
                messages = [
                    SystemMessage(content="You are a helpful assistant designed to make complex topics simple."),
                    HumanMessage(content=query)
                ]
                
                # Invoke the LLM and trace the interaction
                start_time = time.time()
                response = self.llm.invoke(messages)
                
                # Calculate processing time
                processing_time = time.time() - start_time
                
                print(f"Response generated in {processing_time:.2f} seconds")
                return response.content
            
            except Exception as e:
                print(f"Error generating response: {e}")
                return "I'm sorry, but I couldn't generate a response."

    def explain_topic(self, topic):
        """
        Provide a detailed explanation of a given topic
        
        Args:
            topic (str): Topic to explain
        
        Returns:
            str: Detailed explanation
        """
        # Use context manager for tracing
        with self.tracer.start_as_current_span("explain_topic"):
            query = f"Provide a comprehensive, beginner-friendly explanation of {topic}. Break down complex concepts into simple terms."
            return self.generate_response(query)

def main():
    # Create an instance of the demo
    demo = LangtraceDemo()
    
    # Interactive loop
    while True:
        try:
            # Get user input
            topic = input("\nEnter a topic to explain (or 'quit' to exit): ")
            
            # Check for exit
            if topic.lower() in ['quit', 'exit', 'q']:
                print("Exiting the Langtrace demo. Goodbye!")
                break
            
            # Generate and print explanation
            explanation = demo.explain_topic(topic)
            print("\n----- Explanation -----")
            print(explanation)
        
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Ensure API keys are set
    if not os.getenv('GOOGLE_API_KEY'):
        print("Please set the GOOGLE_API_KEY in your .env file.")
        sys.exit(1)
    
    if not os.getenv('LANGTRACE_API_KEY'):
        print("Please set the LANGTRACE_API_KEY in your .env file.")
        sys.exit(1)
    
    # Run the main application
    main()

# Installation instructions
print("\n--- Langtrace Demo Setup ---")
print("1. Additional packages required:")
print("   pip install python-dotenv opentelemetry-api langtrace-python-sdk")
print("2. Ensure your .env file contains:")
print("   GOOGLE_API_KEY=your_google_api_key")
print("   LANGTRACE_API_KEY=your_langtrace_api_key")
print("3. Run the script and explore!")