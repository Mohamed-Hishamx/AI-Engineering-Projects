"""
Research Assistant CLI
Entry point — run with: python -m src.main
"""

import sys
from src.assistant import ResearchAssistant
from src.display import print_banner, print_result, print_error
import logging

logger = logging.getLogger(__name__)


def main():
    print_banner()
    assistant = ResearchAssistant()

    print("Type your question and press Enter. Type 'quit' or 'exit' to stop.\n")

    while True:
        try:
            question = input("🔍 Your question: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\nGoodbye!")
            sys.exit(0)

        if not question:
            continue

        if question.lower() in ("quit", "exit", "q"):
            print("\nGoodbye!")
            sys.exit(0)

        try:
            print("\n⏳ Researching...\n")
            result = assistant.ask(question)
            print_result(result)
        except Exception as e:
            logger.error("Error processing question: %s", e)
            print_error(str(e))

        print()


if __name__ == "__main__":
    main()
