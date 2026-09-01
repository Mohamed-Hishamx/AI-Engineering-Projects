"""
Display helpers — all terminal output lives here, keeping it separate from logic.
Uses only stdlib (no rich dependency) for simplicity.
"""

from src.models import ResearchResponse

# ANSI colour codes
RESET  = "\033[0m"
BOLD   = "\033[1m"
CYAN   = "\033[96m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
DIM    = "\033[2m"
BLUE   = "\033[94m"

CONFIDENCE_COLOUR = {
    "high":   GREEN,
    "medium": YELLOW,
    "low":    RED,
}


def print_banner():
    banner = f"""
{CYAN}{BOLD}
╔══════════════════════════════════════════╗
║      🧠  Research Assistant CLI          ║
║      Powered by GROQ + Pydantic          ║
╚══════════════════════════════════════════╝{RESET}
"""
    print(banner)


def print_result(result: ResearchResponse):
    conf_colour = CONFIDENCE_COLOUR.get(result.confidence, RESET)

    # Summary
    print(f"{BOLD}{CYAN}━━━ Summary ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
    print(f"{result.summary}")
    print()

    # Key points
    print(f"{BOLD}{GREEN}━━━ Key Points ━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
    for i, point in enumerate(result.key_points, 1):
        print(f"  {GREEN}{i}.{RESET} {point}")
    print()

    # Follow-up questions
    print(f"{BOLD}{BLUE}━━━ Follow-up Questions ━━━━━━━━━━━━━━━━━━━{RESET}")
    for q in result.follow_up_questions:
        print(f"  {BLUE}→{RESET} {q}")
    print()

    # Metadata row
    print(
        f"{DIM}Confidence: {conf_colour}{result.confidence.upper()}{RESET}{DIM}  |  "
        f"Sources: {result.sources_note}{RESET}"
    )
    print(f"{DIM}{'─' * 44}{RESET}")


def print_error(message: str):
    print(f"\n{RED}{BOLD}Error:{RESET} {message}")
    print(f"{DIM}Check logs/assistant.log for details.{RESET}\n")
