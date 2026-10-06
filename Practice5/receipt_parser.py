import re
import json
from pathlib import Path


# Find raw.txt in the same folder as this Python file
file_path = Path(__file__).parent / "raw.txt"

with open(file_path, "r", encoding="utf-8") as file:
    text = file.read()


# Convert a receipt price such as "18 009,00" to 18009.0
def convert_price(price):
    return float(price.replace(" ", "").replace(",", "."))


# 1. Extract all prices
# This does not include quantities such as 1,000 or 2,000
prices = re.findall(
    r"(?<![\d,])\d+(?: \d{3})*,\d{2}(?!\d)",
    text
)


# 2. Extract product information
product_pattern = (
    r"^\d+\.\s*\n"                 # Product number
    r"(.+)\n"                      # Product name
    r"(\d+,\d{3})\s*x\s*"          # Quantity
    r"([\d ]+,\d{2})\s*\n"         # Unit price
    r"([\d ]+,\d{2})"              # Product total
)

product_matches = re.findall(
    product_pattern,
    text,
    re.MULTILINE
)

products = []

for name, quantity, unit_price, product_total in product_matches:
    product = {
        "name": name.strip(),
        "quantity": float(quantity.replace(",", ".")),
        "unit_price": convert_price(unit_price),
        "total": convert_price(product_total)
    }

    products.append(product)


# 3. Calculate the total using product totals
calculated_total = sum(product["total"] for product in products)


# Extract the total written on the receipt
total_match = re.search(
    r"ИТОГО:\s*\n([\d ]+,\d{2})",
    text
)

if total_match:
    receipt_total = convert_price(total_match.group(1))
else:
    receipt_total = None


# 4. Extract date and time
date_time_match = re.search(
    r"Время:\s*(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2}:\d{2})",
    text
)

if date_time_match:
    date = date_time_match.group(1)
    time = date_time_match.group(2)
else:
    date = None
    time = None


# 5. Extract payment method and payment amount
payment_match = re.search(
    r"(Банковская карта):\s*\n([\d ]+,\d{2})",
    text
)

if payment_match:
    payment_method = payment_match.group(1)
    payment_amount = convert_price(payment_match.group(2))
else:
    payment_method = None
    payment_amount = None


# 6. Create structured output
result = {
    "prices": prices,
    "products": products,
    "number_of_products": len(products),
    "calculated_total": calculated_total,
    "receipt_total": receipt_total,
    "payment": {
        "method": payment_method,
        "amount": payment_amount
    },
    "date": date,
    "time": time
}


# Display JSON with Russian characters
print(json.dumps(result, ensure_ascii=False, indent=4))