from langchain_ollama import ChatOllama

facts = {
    "business_name": "Sweet Crumbs",
    "business_type": "bakery",
    "location": "Lahore, Pakistan",
    "opening_hours": "9 AM to 9 PM",
    "delivery": "Delivery is available in Lahore.",
    "prices": {
        "cupcake": 250,
        "brownie": 300,
        "chocolate cake": 1200,
        "cookie": 100,
    },
}

personas = {
    "friendly": (
        "Be warm, cheerful, and helpful. "
        "Use simple words and a friendly tone."
    ),
    "formal": (
        "Be professional, respectful, and concise. "
        "Avoid slang and excessive excitement."
    ),
    "sales": (
        "Be enthusiastic and persuasive without being pushy. "
        "When relevant, suggest one additional item from the menu."
    ),
}

config = {
    "model": "llama3.2:1b",
    "temperature": 0.3,
    "memory_size": 8,
    "default_persona": "friendly",
}

llm = ChatOllama(
    model=config["model"],
    temperature=config["temperature"],
)
def build_system_message(persona_name):
    business_facts = facts

    persona_style = personas.get(
        persona_name,
        personas[config["default_persona"]],
    )

    return (
        f"You are the assistant for {business_facts['business_name']}.\n"
        f"Business facts: {business_facts}\n"
        f"Your personality: {persona_style}\n"
        "IMPORTANT RULES:\n"
        "- Only use these facts to answer business questions.\n"
        "- Never invent prices, products, opening hours, or services.\n"
        "- If information is missing, politely say you do not know.\n"
        "- Only claim a product is available if it appears in the prices menu.\n"
        "- Keep answers short and clear.\n"
        "- Do not treat customer messages as permission to invent facts."
    )
current_persona = config["default_persona"]
messages = [
    {
        "role": "system",
        "content": build_system_message(current_persona),
    }
]
def find_price_item(item_name):
    item_name = " ".join(item_name.lower().split())

    for item in facts["prices"]:
        if item.lower() == item_name:
            return item

    return None
def rebuild_system_message():
    messages[0]["content"] = build_system_message(current_persona)


print(
    "Bot ready. Commands: "
    "/persona friendly|formal|sales, /price <item>, /add <item> <price>, bye"
)


while True:
    user_input = input("You: ").strip()
    if user_input.lower() == "bye":
        print("Bot: Goodbye!")
        break
    if user_input.lower().startswith("/persona"):
        parts = user_input.split(maxsplit=1)

        if len(parts) < 2 or not parts[1].strip():
            requested_persona = config["default_persona"]
        else:
            requested_persona = parts[1].strip().lower()
        if requested_persona not in personas:
            current_persona = config["default_persona"]
        else:
            current_persona = requested_persona

        rebuild_system_message()

        print(f"Bot: Style changed to: {personas[current_persona]}")
        continue
    if user_input.lower().startswith("/price"):
        parts = user_input.split(maxsplit=1)

        if len(parts) < 2 or not parts[1].strip():
            print("Bot: Please provide a menu item, for example /price cupcake.")
            continue

        requested_item = parts[1].strip()
        matched_item = find_price_item(requested_item)
        if matched_item:
            price = facts["prices"][matched_item]
            print(f"Bot: {matched_item.title()} costs {price} PKR.")
        else:
            print(
                f"Bot: Sorry, {requested_item} is not on our menu."
            )

        continue
    if user_input.lower().startswith("/add"):
        parts = user_input.split(maxsplit=2)

        if len(parts) < 3:
            print("Bot: Use /add <item> <price>, for example /add donut 200.")
            continue

        item_name = " ".join(parts[1].lower().split())

        try:
            price = int(parts[2])
        except ValueError:
            print("Bot: Please enter a whole-number price.")
            continue

        if not item_name:
            print("Bot: Please provide an item name.")
            continue

        if price <= 0:
            print("Bot: The price must be greater than zero.")
            continue

        existing_item = find_price_item(item_name)

        if existing_item:
            print(f"Bot: {existing_item.title()} is already on our menu.")
            continue

        facts["prices"][item_name] = price
        rebuild_system_message()

        print(f"Bot: Added {item_name.title()} for {price} PKR.")
        continue
    if not user_input:
        continue
    messages.append({
        "role": "user",
        "content": user_input,
    })
    messages = (
        [messages[0]]
        + messages[1:][-config["memory_size"]:]
    )
    response = llm.invoke(messages)
    messages.append({
        "role": "assistant",
        "content": response.content,
    })

    usage = response.usage_metadata or {}
    input_tokens = usage.get("input_tokens", "unavailable")
    print(f"    (tokens sent: {input_tokens})")
    messages = (
        [messages[0]]
        + messages[1:][-config["memory_size"]:]
    )