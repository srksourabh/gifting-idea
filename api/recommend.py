from http.server import BaseHTTPRequestHandler
import json
import random
from urllib.parse import quote_plus


GIFT_DATABASE = {
    "traditional": ["Silver Pooja Items", "Brass Diya Set", "Traditional Silk Saree", "Kurta Pajama Set", "Handcrafted Jewelry", "Silver Coins"],
    "modern": ["Smart Watch", "Bluetooth Speaker", "Power Bank", "Wireless Earbuds", "Coffee Maker", "Air Purifier"],
    "personalized": ["Customized Photo Frame", "Engraved Pen Set", "Personalized Cushion", "Photo Coffee Mug"],
    "luxury": ["Designer Perfume", "Premium Watch", "Leather Wallet", "Designer Sunglasses", "Branded Handbag"],
    "wellness": ["Yoga Mat", "Essential Oil Diffuser", "Spa Gift Hamper", "Fitness Tracker"],
    "festive": ["Decorative Diya Set", "Rangoli Kit", "Festival Sweet Hamper", "Pooja Thali Set"],
    "romantic": ["Couple Watches", "Heart-shaped Jewelry", "Perfume Gift Set", "Love Letter Kit"],
    "home": ["Wall Clock", "Decorative Showpiece", "Table Lamp", "Bedsheet Set", "Dinner Set"],
}

RELATIONSHIPS = {
    "mother": "immediate_family", "father": "immediate_family", "brother": "immediate_family",
    "sister": "immediate_family", "wife": "immediate_family", "husband": "immediate_family",
    "boss": "professional", "colleague": "professional", "friend": "social",
    "boyfriend": "romantic", "girlfriend": "romantic", "saali": "family"
}


def get_recommendations(relationship, occasion, budget):
    rel_type = RELATIONSHIPS.get(relationship.lower(), "general")

    if rel_type == "immediate_family":
        categories = ["personalized", "luxury", "wellness"]
    elif rel_type == "professional":
        categories = ["modern", "luxury"]
    elif rel_type == "romantic":
        categories = ["romantic", "personalized", "luxury"]
    else:
        categories = ["traditional", "modern", "personalized"]

    if occasion.lower() in ["diwali", "holi", "raksha bandhan"]:
        categories.insert(0, "festive")

    recommendations = []
    used = set()

    for i in range(5):
        cat = categories[i % len(categories)]
        items = [x for x in GIFT_DATABASE.get(cat, GIFT_DATABASE["modern"]) if x not in used]
        if not items:
            items = [x for v in GIFT_DATABASE.values() for x in v if x not in used]
        if items:
            random.seed(hash(f"{relationship}{occasion}{i}"))
            item = random.choice(items)
            used.add(item)
            price = round(budget * random.uniform(0.7, 1.1) / 50) * 50
            recommendations.append({
                "id": i + 1,
                "title": item,
                "description": f"Perfect for {relationship} on {occasion}",
                "approx_price_inr": f"Rs.{price:,}",
                "purchase_links": {
                    "amazon_in": f"https://www.amazon.in/s?k={quote_plus(item)}",
                    "flipkart": f"https://www.flipkart.com/search?q={quote_plus(item)}"
                }
            })

    return {
        "thinking_trace": f"Analyzing gift for {relationship} on {occasion} with Rs.{budget} budget.",
        "recommendations": recommendations,
        "pro_tip": "Present with both hands as a sign of respect."
    }


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        data = json.loads(body)

        result = get_recommendations(
            data.get('relationship', 'Friend'),
            data.get('occasion', 'Birthday'),
            data.get('budget', 2000)
        )

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(result).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
