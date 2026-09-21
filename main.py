from agent import run_agent


def main():
    print("Portfolio risk agent. Type 'quit' to exit.\n")

    while True:
        question = input("> ")
        if question.strip().lower() in ("quit", "exit"):
            break
        if not question.strip():
            continue

        answer = run_agent(question)
        print(f"\n{answer}\n")


if __name__ == "__main__":
    main()
