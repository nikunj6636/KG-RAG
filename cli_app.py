import os
import subprocess
import sys
from datetime import datetime
from typing import List, Tuple

class QATerminal:
    def __init__(self):
        self.history: List[Tuple[str, str]] = []
        self.title = '''ResearchNexus (our proposal) Session on "Attention is All You Need"'''
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def display_title(self):
        width = 60
        print("=" * width)
        print(self.title.center(width))
        print(f"Session started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}".center(width))
        print("=" * width)
        print()

    def display_history(self):
        if not self.history:
            print("No questions asked yet.\n")
            return
            
        print("\nPrevious Questions and Answers:")
        print("-" * 60)
        for i, (q, a) in enumerate(self.history, 1):
            print(f"\nQ{i}: {q}")
            print(f"A{i}: {a}")
        print("\n" + "-" * 60 + "\n")

    def get_answer(self, question: str) -> str:
        try:
            result = subprocess.run(
                [
                   "./graphragvenv/bin/python3", "-m", "graphrag.query", "--root", ".", "--method", "local", question
                ],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            return f"Error getting answer: {e.stderr}"
        except Exception as e:
            return f"Unexpected error: {str(e)}"

    def run(self):
        try:
            while True:
                self.clear_screen()
                self.display_title()
                self.display_history()
                
                question = input("Enter your question (or 'quit' to exit): ").strip()
                
                if question.lower() in ['quit', 'exit', 'q']:
                    print("\nThank you for using the Q&A Terminal. Goodbye!")
                    break
                    
                if not question:
                    continue
                
                print("\nGetting answer...\n")
                answer = self.get_answer(question)
                self.history.append((question, answer))
                
                input("\nPress Enter to continue...")
                
        except KeyboardInterrupt:
            print("\n\nExiting due to user interruption. Goodbye!")
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
            print("The application will now exit.")
            
if __name__ == "__main__":
    app = QATerminal()
    app.run()