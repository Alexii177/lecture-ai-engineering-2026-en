"""Lecture 01: single questions and a chat with conversation history."""

import argparse

from google import genai
from google.genai import errors

from app.config import MODEL, api_error_message, get_api_key

DEFAULT_QUESTION = "What are the 3 homework levels in the AIE2026 course?"


def display_response(response) -> str:
    """Display token usage and return the response text."""
    usage = response.usage_metadata
    if usage is not None:
        print(
            f"[tokens] input={usage.prompt_token_count}, "
            f"output={usage.candidates_token_count}"
        )
    return response.text or ""


def ask(question: str) -> str:
    """Ask one question without keeping history."""
    with genai.Client(api_key=get_api_key()) as client:
        response = client.models.generate_content(
            model=MODEL,
            contents=question,
        )
        return display_response(response)


def chat() -> None:
    """Keep conversation history for the current chat session."""
    with genai.Client(api_key=get_api_key()) as client:
        session = client.chats.create(model=MODEL)
        print("Chat started. Type /exit to quit or /reset to clear history.")

        while True:
            try:
                question = input("\nYou: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nChat ended.")
                break

            if question.lower() == "/exit":
                print("Chat ended.")
                break

            if question.lower() == "/reset":
                session = client.chats.create(model=MODEL)
                print("Conversation history cleared.")
                continue

            if not question:
                continue

            try:
                response = session.send_message(question)
                print(f"\nAssistant: {display_response(response)}")
            except errors.APIError as error:
                print(api_error_message(error.code, error.message))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Ask one question or start a chat with history."
    )
    parser.add_argument("question", nargs="?", default=DEFAULT_QUESTION)
    parser.add_argument(
        "--chat",
        action="store_true",
        help="Start an interactive conversation with history.",
    )
    args = parser.parse_args()

    print(f"[model] {MODEL}")

    try:
        if args.chat:
            chat()
        else:
            print(f"[question] {args.question}\n")
            print(ask(args.question))
    except errors.APIError as error:
        print(api_error_message(error.code, error.message))
        raise SystemExit(1)


if __name__ == "__main__":
    main()