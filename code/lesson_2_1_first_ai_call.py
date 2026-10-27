from langchain.chat_models import init_chat_model


# Ask the user for a topic and remove unnecessary spaces.
topic = input("Topic:   ").strip()

# Ask the user for a level and clean the input.
level = input("Level (beginner or expert): ").strip().lower()

# Why: Validation prevents an unsupported level from being used.
if level not in ["beginner", "expert"]:
    print("Invalid level. Please enter beginner or expert.")
    raise SystemExit(1)

# Tell the AI its role, the student's level, and the answer length.
system_message = f"""
You are a helpful AI tutor.

Explain the topic at the {level} level.

For beginner students, use simple words and a short explanation.
For expert students, use technical details and a more detailed explanation.

Keep your answer focused on the requested topic.
"""

# Why: A low temperature encourages more consistent answers.
model = init_chat_model(
    "ollama:llama3.2:1b",
    temperature=0.2,
)

# Send the instructions and topic to the AI.
response = model.invoke(
    [
        ("system", system_message),
        ("human", topic),
    ]
)

# Print the answer between separator lines.
print("=" * 40)
print(response.text)
print("=" * 40)

# Read the total number of tokens reported by the model.
total_tokens = response.usage_metadata["total_tokens"]

# Get the model's processing duration in nanoseconds.
total_duration = response.response_metadata.get("total_duration", 0)

# Convert nanoseconds to seconds.
seconds = total_duration / 1_000_000_000

# Print the token count and time to one decimal place.
print(f"{total_tokens} tokens in {seconds:.1f} seconds")