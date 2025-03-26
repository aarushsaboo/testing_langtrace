
# IMPORTANT: Import Langtrace SDK first
from langtrace_python_sdk import langtrace, trace

# Initialize Langtrace SDK
# Replace with your actual Langtrace API key
LANGTRACE_API_KEY = "039c704c3cad6e22aea5baa386aae84d32147635e8115664394056994dbea42b"
langtrace.init(
    api_key=LANGTRACE_API_KEY,
    service_name="langtrace_demo_app",
    write_spans_to_console=True
)

import os
import sys
import time
# Import the LLM library (in this case, we'll use Google's Gemini)
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

GOOGLE_API_KEY = "AIzaSyC5zEinq8gaFKWr33_Mjusxbm-fyYS0YZA"  # Replace with your key
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

class LangtraceDemo:
    def __init__(self):
        # Initialize the LLM
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.7,
            max_output_tokens=1024
        )
    
    @trace("generate_response")
    def generate_response(self, query):
        """
        Generate a response using the LLM with Langtrace tracing
        
        Args:
            query (str): User's input query
        
        Returns:
            str: LLM's generated response
        """
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

    @trace("explain_topic")
    def explain_topic(self, topic):
        """
        Provide a detailed explanation of a given topic
        
        Args:
            topic (str): Topic to explain
        
        Returns:
            str: Detailed explanation
        """
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
    # Ensure Google API key is set
    if "GOOGLE_API_KEY" not in os.environ:
        print("Please set the GOOGLE_API_KEY environment variable.")
        sys.exit(1)
    
    # Run the main application
    main()

# Quick usage instructions
print("\n--- Langtrace Demo Setup ---")
print("1. Install required packages:")
print("   pip install langtrace-python-sdk langchain-google-genai")
print("2. Set your Google API key:")
print("   export GOOGLE_API_KEY='your_google_api_key'")
print("3. Set your Langtrace API key in the script")
print("4. Run the script and explore!")