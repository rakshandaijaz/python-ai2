import time
from langchain_ollama import ChatOllama

products = {
    "Chocolate Cake": 1500,
    "Cupcake": 250,
    "Brownie": 300,
    "Donut": 200,
    "Cookie": 100,
    "Old Stock": 0,
}

llm = ChatOllama(model="llama3.2:1b", temperature=0.3)

results = []
total_tokens = 0
total_seconds = 0

start_time = time.time()

for name, price in products.items():

    if price == 0:
        print(f"Skipping {name.lower()} (no price)")
        continue
    prompt = (
        f"Write one short, attractive sentence describing {name} "
        f"for a bakery menu. The price is {price} PKR. "
        "Return only the description."
    )

    item_start = time.time()
    response = llm.invoke(prompt)
    item_seconds = time.time() - item_start

    description = response.content.strip()

    usage = response.usage_metadata or {}
    tokens = usage.get("total_tokens", 0)

    total_tokens += tokens
    total_seconds += item_seconds
    results.append({
        "item": name,
        "price": price,
        "text": description,
    })
print("=" * 50)

for number, product in enumerate(results, start=1):
    print(f"{number}. {product['item']} ({product['price']} PKR)")
    print(f"   {product['text']}")

print("=" * 50)

print(
    f"{len(results)} descriptions, "
    f"{total_tokens} tokens, "
    f"{total_seconds:.1f} seconds"
)