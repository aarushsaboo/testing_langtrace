import os
import json
import logging
from datetime import datetime

class PerformanceLogger:
    def __init__(self, log_dir):
        self.log_dir = log_dir
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.performance_txt_log = os.path.join(log_dir, f'performance_log_{timestamp}.txt')
        self.performance_json_log = os.path.join(log_dir, f'performance_log_{timestamp}.json')
        
        self.total_api_calls = 0
        self.total_tokens_used = 0
        self.api_call_times = []
        self.detailed_tracking = []
    
    def log_api_call(self, query, input_tokens, output_tokens, duration, success=True, error=None):
        call_record = {
            'timestamp': datetime.now().isoformat(),
            'query': query[:200],
            'input_tokens': input_tokens,
            'output_tokens': output_tokens,
            'total_tokens': input_tokens + output_tokens,
            'duration_seconds': round(duration, 4),
            'success': success,
            'error': error
        }
        
        self.detailed_tracking.append(call_record)
        self.total_api_calls += 1
        self.total_tokens_used += (input_tokens + output_tokens)
        self.api_call_times.append(duration)
        
        log_message = (
            f"API Call: {query[:50]}... | "
            f"Tokens: {input_tokens}/{output_tokens} | "
            f"Duration: {duration:.4f}s | "
            f"Success: {success}"
        )
        logging.info(log_message)
    
    def save_performance_log(self):
        performance_summary = {
            'timestamp': datetime.now().isoformat(),
            'total_api_calls': self.total_api_calls,
            'total_tokens_used': self.total_tokens_used,
            'avg_call_time': round(sum(self.api_call_times) / len(self.api_call_times), 4) if self.api_call_times else 0,
            'min_call_time': round(min(self.api_call_times), 4) if self.api_call_times else 0,
            'max_call_time': round(max(self.api_call_times), 4) if self.api_call_times else 0,
        }
        
        try:
            with open(self.performance_txt_log, 'w') as f:
                f.write("=== Performance Summary ===\n")
                for key, value in performance_summary.items():
                    f.write(f"{key}: {value}\n")
                
                f.write("\n=== Detailed API Calls ===\n")
                for call in self.detailed_tracking:
                    f.write(json.dumps(call) + "\n")
            
            with open(self.performance_json_log, 'w') as f:
                json.dump({
                    'summary': performance_summary,
                    'detailed_calls': self.detailed_tracking
                }, f, indent=2)
            
            print(f"Performance logs saved:")
            print(f"- Text log: {self.performance_txt_log}")
            print(f"- JSON log: {self.performance_json_log}")
            
            return self.performance_txt_log
        except Exception as e:
            print(f"Error saving log files: {e}")
            return None