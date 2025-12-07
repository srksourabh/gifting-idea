from http.server import BaseHTTPRequestHandler
import json
import random
from urllib.parse import quote_plus


GIFT_DATABASE = {
    "traditional": ["Silver Pooja Items", "Brass Diya Set", "Traditional Silk Saree", "Kurta Pajama Set", "Handcrafted Jewelry", "Silver Coins", "Copper Water Bottle", "Traditional Sweet Box"],
    "modern": ["Smart Watch", "Bluetooth Speaker", "Power Bank", "Wireless Earbuds", "Coffee Maker", "Air Purifier", "Electric Kettle", "Grooming Kit"],
    "personalized": ["Customized Photo Frame", "Engraved Pen Set", "Personalized Cushion", "Photo Coffee Mug", "Custom Name Plate", "Customized Diary"],
    "luxury": ["Designer Perfume", "Premium Watch", "Leather Wallet", "Designer Sunglasses", "Branded Handbag", "Premium Tea Gift Set", "Luxury Chocolate Box"],
    "wellness": ["Yoga Mat", "Essential Oil Diffuser", "Spa Gift Hamper", "Fitness Tracker", "Organic Skincare Set", "Meditation Kit"],
    "festive": ["Decorative Diya Set", "Rangoli Kit", "Festival Sweet Hamper", "Pooja Thali Set", "Festive Dry Fruit Box", "Decorative Toran"],
    "romantic": ["Couple Watches", "Heart-shaped Jewelry", "Perfume Gift Set", "Love Letter Kit", "Couple Keychains"],
    "home": ["Wall Clock", "Decorative Showpiece", "Table Lamp", "Bedsheet Set", "Dinner Set", "Indoor Plant with Planter"],
    "tech": ["Tablet", "Kindle E-reader", "Smart Home Device", "Gaming Accessories", "Portable Projector"],
    "kids": ["Educational Toys", "Building Blocks Set", "Art and Craft Kit", "Remote Control Car", "Story Books Set"],
}

RELATIONSHIPS = {
    "mother": "immediate_family", "father": "immediate_family", "brother": "immediate_family",
    "sister": "immediate_family", "wife": "immediate_family", "husband": "immediate_family",
    "son": "immediate_family", "daughter": "immediate_family", "grandparent": "immediate_family",
    "grandchild": "immediate_family", "uncle": "extended_family", "aunt": "extended_family",
    "cousin": "extended_family", "nephew": "extended_family", "niece": "extended_family",
    "boss": "professional", "colleague": "professional", "friend": "social",
    "boyfriend": "romantic", "girlfriend": "romantic", "saali": "family"
}

OCCASIONS = {
    "diwali": "festival", "holi": "festival", "raksha bandhan": "festival",
    "durga puja": "festival", "ganesh chaturthi": "festival", "navratri": "festival",
    "eid": "festival", "christmas": "festival", "pongal": "festival", "onam": "festival",
    "new year": "celebration", "birthday": "celebration", "anniversary": "milestone",
    "wedding": "milestone", "graduation": "milestone", "promotion": "milestone",
    "baby shower": "milestone", "house warming": "milestone", "retirement": "milestone",
    "valentine's day": "romantic", "karva chauth": "festival", "mother's day": "celebration",
    "father's day": "celebration"
}

PRO_TIPS = {
    "diwali": "Always include a handwritten card with Diwali wishes. Avoid black colored gifts.",
    "raksha bandhan": "Present the gift after the rakhi ceremony. Include sweets for tradition.",
    "wedding": "Gifts in odd numbers are considered auspicious. Include shagun envelope.",
    "birthday": "Personalized gifts show extra thought. Consider their hobbies and interests.",
    "anniversary": "Gifts symbolizing togetherness work best. Avoid sharp objects like knives.",
    "professional": "Keep professional gifts neutral and practical. Avoid overly personal items.",
    "default": "Present with both hands as a sign of respect. Include a personalized message."
}


def get_recommendations(relationship, occasion, age_group, vibe, budget):
    rel_type = RELATIONSHIPS.get(relationship.lower(), "general")
    occ_type = OCCASIONS.get(occasion.lower(), "celebration")

    if rel_type == "immediate_family":
        categories = ["personalized", "luxury", "wellness"]
    elif rel_type == "professional":
        categories = ["modern", "luxury"]
    elif rel_type == "romantic":
        categories = ["romantic", "personalized", "luxury"]
    else:
        categories = ["traditional", "modern", "personalized"]

    vibe_lower = vibe.lower() if vibe else ""
    if "traditional" in vibe_lower:
        categories.insert(0, "traditional")
    if "tech" in vibe_lower:
        categories.insert(0, "tech")
    if "wellness" in vibe_lower:
        categories.insert(0, "wellness")
    if "luxury" in vibe_lower:
        categories.insert(0, "luxury")

    if occ_type == "festival":
        categories.insert(0, "festive")

    if age_group and age_group.lower() == "child":
        categories = ["kids", "personalized"] + categories

    recommendations = []
    used = set()

    for i in range(5):
        cat = categories[i % len(categories)]
        items = [x for x in GIFT_DATABASE.get(cat, GIFT_DATABASE["modern"]) if x not in used]
        if not items:
            items = [x for v in GIFT_DATABASE.values() for x in v if x not in used]
        if items:
            random.seed(hash(f"{relationship}{occasion}{vibe}{i}"))
            item = random.choice(items)
            used.add(item)
            price = round(budget * random.uniform(0.7, 1.1) / 50) * 50

            descriptions = [
                f"Perfect for {relationship} on {occasion}, combines thoughtfulness with utility",
                f"Culturally appropriate choice that honors the {occasion} celebration",
                f"Shows respect and affection, ideal for {relationship}",
                f"Meaningful gift that celebrates {occasion} with traditional values",
                f"Thoughtful present that strengthens your bond"
            ]

            recommendations.append({
                "id": i + 1,
                "title": item,
                "description": descriptions[i % len(descriptions)],
                "approx_price_inr": f"Rs.{price:,}",
                "purchase_links": {
                    "amazon_in": f"https://www.amazon.in/s?k={quote_plus(item)}",
                    "flipkart": f"https://www.flipkart.com/search?q={quote_plus(item)}"
                }
            })

    pro_tip = PRO_TIPS.get(occasion.lower(), PRO_TIPS.get("professional" if rel_type == "professional" else "default", PRO_TIPS["default"]))

    return {
        "thinking_trace": f"Analyzing gift for {relationship} on {occasion}. Considering {rel_type} relationship type, {occ_type} occasion, {age_group} age group, {vibe} style preference, and Rs.{budget:,} budget.",
        "recommendations": recommendations,
        "pro_tip": pro_tip
    }


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        data = json.loads(body)

        result = get_recommendations(
            data.get('relationship', 'Friend'),
            data.get('occasion', 'Birthday'),
            data.get('age_group', 'Adult'),
            data.get('vibe', 'Traditional'),
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
