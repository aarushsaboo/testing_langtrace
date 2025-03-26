import logging
from config.logging_config import setup_logging
from utils.performance_logger import PerformanceLogger
from models.ai_assistant import AIResearchAssistant

def main():
    log_dir = setup_logging()
    performance_logger = PerformanceLogger(log_dir)
    assistant = AIResearchAssistant(performance_logger)
    
    try:
        while True:
            topic = input("\nEnter a research topic (or 'quit' to exit, 'report' for performance): ")
            
            if topic.lower() == 'quit':
                break
            
            if topic.lower() == 'report':
                log_file = performance_logger.save_performance_log()
                print(f"\nPerformance log saved to: {log_file}")
                continue
            
            print(f"\n===== Researching: {topic} =====")
            research_result = assistant.research_workflow(topic)
            
            print("\n----- Final Research Report -----")
            print(research_result['final_report'])
    
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        print(f"An error occurred: {e}")
    finally:
        performance_logger.save_performance_log()

if __name__ == "__main__":
    main()