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
    "kids_boys": ["Remote Control Car", "Building Blocks Set", "Gaming Accessories", "Story Books Set", "Cricket Kit", "Football"],
    "kids_girls": ["Art and Craft Kit", "Doll House Set", "Story Books Set", "Educational Toys", "Dance Costume Set", "Jewelry Making Kit"],
}

# Gift type classification (formal, funky, romantic, practical, traditional, luxury)
GIFT_TYPE_TAGS = {
    "Silver Pooja Items": "Traditional", "Brass Diya Set": "Traditional", "Traditional Silk Saree": "Traditional",
    "Kurta Pajama Set": "Formal", "Handcrafted Jewelry": "Traditional", "Silver Coins": "Formal",
    "Copper Water Bottle": "Practical", "Traditional Sweet Box": "Traditional", "Smart Watch": "Practical",
    "Bluetooth Speaker": "Funky", "Power Bank": "Practical", "Wireless Earbuds": "Practical",
    "Coffee Maker": "Practical", "Air Purifier": "Practical", "Electric Kettle": "Practical", "Grooming Kit": "Practical",
    "Customized Photo Frame": "Romantic", "Engraved Pen Set": "Formal", "Personalized Cushion": "Funky",
    "Photo Coffee Mug": "Funky", "Custom Name Plate": "Formal", "Customized Diary": "Formal",
    "Designer Perfume": "Luxury", "Premium Watch": "Luxury", "Leather Wallet": "Formal",
    "Designer Sunglasses": "Luxury", "Branded Handbag": "Luxury", "Premium Tea Gift Set": "Formal",
    "Luxury Chocolate Box": "Luxury", "Yoga Mat": "Practical", "Essential Oil Diffuser": "Practical",
    "Spa Gift Hamper": "Luxury", "Fitness Tracker": "Practical", "Organic Skincare Set": "Luxury",
    "Meditation Kit": "Practical", "Decorative Diya Set": "Traditional", "Rangoli Kit": "Traditional",
    "Festival Sweet Hamper": "Traditional", "Pooja Thali Set": "Traditional", "Festive Dry Fruit Box": "Formal",
    "Decorative Toran": "Traditional", "Couple Watches": "Romantic", "Heart-shaped Jewelry": "Romantic",
    "Perfume Gift Set": "Romantic", "Love Letter Kit": "Romantic", "Couple Keychains": "Romantic",
    "Wall Clock": "Practical", "Decorative Showpiece": "Formal", "Table Lamp": "Practical",
    "Bedsheet Set": "Practical", "Dinner Set": "Formal", "Indoor Plant with Planter": "Practical",
    "Tablet": "Practical", "Kindle E-reader": "Practical", "Smart Home Device": "Practical",
    "Gaming Accessories": "Funky", "Portable Projector": "Practical", "Educational Toys": "Practical",
    "Building Blocks Set": "Funky", "Art and Craft Kit": "Funky", "Remote Control Car": "Funky",
    "Story Books Set": "Practical", "Cricket Kit": "Funky", "Football": "Funky",
    "Doll House Set": "Funky", "Dance Costume Set": "Funky", "Jewelry Making Kit": "Funky"
}

GIFT_ICONS = {
    "Silver Pooja Items": "🪔", "Brass Diya Set": "🪔", "Traditional Silk Saree": "👗",
    "Kurta Pajama Set": "👔", "Handcrafted Jewelry": "💍", "Silver Coins": "🪙",
    "Copper Water Bottle": "🍶", "Traditional Sweet Box": "🍬", "Smart Watch": "⌚",
    "Bluetooth Speaker": "🔊", "Power Bank": "🔋", "Wireless Earbuds": "🎧",
    "Coffee Maker": "☕", "Air Purifier": "💨", "Electric Kettle": "🫖", "Grooming Kit": "💈",
    "Customized Photo Frame": "🖼️", "Engraved Pen Set": "🖊️", "Personalized Cushion": "🛋️",
    "Photo Coffee Mug": "☕", "Custom Name Plate": "🏷️", "Customized Diary": "📔",
    "Designer Perfume": "🧴", "Premium Watch": "⌚", "Leather Wallet": "👛",
    "Designer Sunglasses": "🕶️", "Branded Handbag": "👜", "Premium Tea Gift Set": "🍵",
    "Luxury Chocolate Box": "🍫", "Yoga Mat": "🧘", "Essential Oil Diffuser": "🌸",
    "Spa Gift Hamper": "🧖", "Fitness Tracker": "📱", "Organic Skincare Set": "🧴",
    "Meditation Kit": "🧘", "Decorative Diya Set": "🪔", "Rangoli Kit": "🎨",
    "Festival Sweet Hamper": "🍬", "Pooja Thali Set": "🪔", "Festive Dry Fruit Box": "🥜",
    "Decorative Toran": "🎊", "Couple Watches": "⌚", "Heart-shaped Jewelry": "💝",
    "Perfume Gift Set": "🧴", "Love Letter Kit": "💌", "Couple Keychains": "🔑",
    "Wall Clock": "🕐", "Decorative Showpiece": "🏺", "Table Lamp": "💡",
    "Bedsheet Set": "🛏️", "Dinner Set": "🍽️", "Indoor Plant with Planter": "🪴",
    "Tablet": "📱", "Kindle E-reader": "📚", "Smart Home Device": "🏠",
    "Gaming Accessories": "🎮", "Portable Projector": "📽️", "Educational Toys": "🧩",
    "Building Blocks Set": "🧱", "Art and Craft Kit": "🎨", "Remote Control Car": "🚗",
    "Story Books Set": "📚", "Cricket Kit": "🏏", "Football": "⚽",
    "Doll House Set": "🏠", "Dance Costume Set": "💃", "Jewelry Making Kit": "💎"
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


def get_recommendations(relationship, occasion, age_group, vibe, budget, gender="", notes="", gift_types=None):
    if gift_types is None:
        gift_types = ["Formal", "Funky", "Romantic", "Practical", "Traditional", "Luxury"]

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

    # Handle children with gender-specific gifts
    if age_group and age_group.lower() == "child":
        if gender and gender.lower() == "male":
            categories = ["kids_boys", "kids", "personalized"] + categories
        elif gender and gender.lower() == "female":
            categories = ["kids_girls", "kids", "personalized"] + categories
        else:
            categories = ["kids", "personalized"] + categories

    recommendations = []
    used = set()
    attempt = 0

    while len(recommendations) < 10 and attempt < 50:
        cat = categories[attempt % len(categories)]
        # Filter items by selected gift types
        items = [x for x in GIFT_DATABASE.get(cat, GIFT_DATABASE["modern"])
                 if x not in used and GIFT_TYPE_TAGS.get(x, "Practical") in gift_types]
        if not items:
            items = [x for v in GIFT_DATABASE.values() for x in v
                     if x not in used and GIFT_TYPE_TAGS.get(x, "Practical") in gift_types]
        if items:
            random.seed(hash(f"{relationship}{occasion}{vibe}{gender}{attempt}"))
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

            # Generate personalized reason for this gift
            why_reasons = []
            if rel_type == "immediate_family":
                why_reasons.append(f"Your {relationship} deserves something special that shows deep appreciation")
            elif rel_type == "romantic":
                why_reasons.append(f"Perfect for expressing love and affection to your {relationship}")
            elif rel_type == "professional":
                why_reasons.append(f"Maintains appropriate professional boundaries while showing respect")
            else:
                why_reasons.append(f"Thoughtful choice that strengthens your bond with your {relationship}")

            if occ_type == "festival":
                why_reasons.append(f"Aligns beautifully with the spirit and traditions of {occasion}")
            elif occ_type == "milestone":
                why_reasons.append(f"Commemorates this important {occasion} milestone meaningfully")
            elif occ_type == "romantic":
                why_reasons.append(f"Captures the romantic essence of {occasion}")
            else:
                why_reasons.append(f"Ideal for celebrating {occasion}")

            if age_group and age_group.lower() == "child":
                gender_text = " boy" if gender and gender.lower() == "male" else (" girl" if gender and gender.lower() == "female" else "")
                why_reasons.append(f"Age-appropriate and engaging for children{gender_text}")
            elif age_group and age_group.lower() == "senior":
                why_reasons.append("Practical and valued by seniors")
            elif age_group and age_group.lower() == "teenager":
                why_reasons.append("Trendy and appealing for teenagers")

            if "traditional" in vibe_lower:
                why_reasons.append("Honors traditional values and cultural heritage")
            elif "tech" in vibe_lower:
                why_reasons.append("Modern tech gift for the gadget enthusiast")
            elif "luxury" in vibe_lower:
                why_reasons.append("Premium quality that makes a lasting impression")
            elif "wellness" in vibe_lower:
                why_reasons.append("Promotes health and well-being")

            # Add personalized note if provided
            if notes and notes.strip():
                why_reasons.append(f"Considering your note: {notes.strip()[:50]}")

            why_applicable = " • ".join(why_reasons[:3])
            gift_type_tag = GIFT_TYPE_TAGS.get(item, "Practical")

            icon = GIFT_ICONS.get(item, "🎁")
            encoded_item = quote_plus(item)

            recommendations.append({
                "id": len(recommendations) + 1,
                "title": item,
                "icon": icon,
                "gift_type": gift_type_tag,
                "description": descriptions[len(recommendations) % len(descriptions)],
                "why_applicable": why_applicable,
                "approx_price_inr": f"Rs.{price:,}",
                "purchase_links": {
                    "amazon": f"https://www.amazon.in/s?k={encoded_item}",
                    "flipkart": f"https://www.flipkart.com/search?q={encoded_item}",
                    "myntra": f"https://www.myntra.com/{encoded_item}",
                    "shoppersstop": f"https://www.shoppersstop.com/search?q={encoded_item}",
                    "blinkit": f"https://blinkit.com/s/?q={encoded_item}",
                    "meesho": f"https://www.meesho.com/search?q={encoded_item}"
                }
            })
        attempt += 1

    pro_tip = PRO_TIPS.get(occasion.lower(), PRO_TIPS.get("professional" if rel_type == "professional" else "default", PRO_TIPS["default"]))

    gender_text = f", {gender} gender" if gender else ""
    notes_text = f", with special note: '{notes[:30]}...'" if notes and len(notes) > 30 else (f", with note: '{notes}'" if notes else "")
    types_text = f", filtering by: {', '.join(gift_types)}" if len(gift_types) < 6 else ""

    return {
        "thinking_trace": f"Analyzing gift for {relationship} on {occasion}. Considering {rel_type} relationship type, {occ_type} occasion, {age_group} age group{gender_text}, {vibe} style preference, and Rs.{budget:,} budget{notes_text}{types_text}.",
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
            data.get('budget', 2000),
            data.get('gender', ''),
            data.get('notes', ''),
            data.get('gift_types', None)
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
