from langchain_ollama import ChatOllama

llm = ChatOllama(model="llama3.2:1b")

system_message = {
    "role": "system",
    "content": (
        "You are a friendly personal tutor for students. "
        "Remember details from the conversation. "
        "Give clear, simple, short answers in 2-4 sentences. "
        "If the conversation does not contain the answer, "
        "say you do not know instead of guessing."
    ),
}
messages = [system_message]

questions = []


print("Tutor: Ask me anything. Commands: /reset, /count, bye")


while True:
    user_input = input("You: ").strip()

    if user_input.lower() == "bye":
        print("Tutor: Goodbye!")
        print(f"Tutor: You asked {len(questions)} questions.")

        if questions:
            print(f"Tutor: First question: {questions[0]}")
            print(f"Tutor: Last question: {questions[-1]}")

        break
    if user_input.lower() == "/reset":
        messages = [messages[0]]
        print("Tutor: Memory cleared.")
        continue
    if user_input.lower() == "/count":
        print(f"Tutor: {len(messages)} messages in memory.")
        continue
    if not user_input:
        continue
    messages.append({
        "role": "user",
        "content": user_input,
    })
    questions.append(user_input)
    messages = [messages[0]] + messages[1:][-8:]
    response = llm.invoke(messages)

    messages.append({
        "role": "assistant",
        "content": response.content,
    })
    print(f"Tutor: {response.content}")
    usage = response.usage_metadata or {}
    input_tokens = usage.get("input_tokens", "unavailable")
    print(f"       (tokens sent: {input_tokens})")

    messages = [messages[0]] + messages[1:][-8:]