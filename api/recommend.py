from http.server import BaseHTTPRequestHandler
import json
import random
import os
import urllib.request
import urllib.error
from urllib.parse import quote_plus, urlparse


# Gemini API Configuration
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"


# Affiliate program IDs (set in Vercel env). Any unset key -> raw URL.
# - Amazon Associates India: e.g. "yourname-21"
# - Cuelinks (aggregator: Flipkart, Myntra, Croma, Ajio, ShoppersStop, Meesho)
AMAZON_AFFILIATE_TAG = os.environ.get('AMAZON_AFFILIATE_TAG', '')
CUELINKS_CID         = os.environ.get('CUELINKS_CID', '')

# Merchants that have no public affiliate program -> always pass-through.
_NO_AFFILIATE_MERCHANTS = {'blinkit', 'zepto', 'instamart', 'swiggy'}

# Server-side input caps -- protect against prompt-injection-via-bloat
# and runaway token spend. Match or exceed the client-side maxlength.
_LIMITS = {
    'relationship': 50,
    'occasion':     50,
    'age_group':    50,
    'vibe':         50,
    'gender':       30,
    'notes':        300,
    'city':         50,
}


def _add_amazon_tag(url: str) -> str:
    """Append Associates tag only to genuine amazon.in URLs."""
    if not AMAZON_AFFILIATE_TAG or not isinstance(url, str):
        return url
    try:
        host = urlparse(url).netloc.lower()
    except (ValueError, AttributeError):
        return url
    # Match amazon.in and its subdomains; reject lookalikes (myamazonshop.in, amazonaws.com)
    if host != 'amazon.in' and not host.endswith('.amazon.in'):
        return url
    sep = '&' if '?' in url else '?'
    return f"{url}{sep}tag={quote_plus(AMAZON_AFFILIATE_TAG)}"


def _wrap_cuelinks(url: str) -> str:
    """Wrap a merchant URL through the Cuelinks aggregator redirect."""
    if not CUELINKS_CID or not isinstance(url, str):
        return url
    return (
        "https://linksredirect.com/?cid="
        f"{quote_plus(CUELINKS_CID)}&source=linkkit&url={quote_plus(url)}"
    )


def add_affiliate_tags(links: dict) -> dict:
    """Apply affiliate wrapping to outbound links where we have programs.

    Order of preference:
    - Amazon  -> direct tag append (preserves recognizable URL).
    - Other supported merchants -> Cuelinks if configured.
    - Quick commerce -> untouched (no affiliate programs exist).
    """
    if not links:
        return links

    out: dict = {}
    for merchant, url in links.items():
        if not url or not isinstance(url, str):
            out[merchant] = url
            continue
        merchant_key = merchant.lower()
        if merchant_key in _NO_AFFILIATE_MERCHANTS:
            out[merchant] = url
        elif merchant_key == 'amazon':
            out[merchant] = _add_amazon_tag(url)
        elif CUELINKS_CID:
            out[merchant] = _wrap_cuelinks(url)
        else:
            out[merchant] = url
    return out


def _sanitize_inputs(data: dict) -> dict:
    """Coerce + truncate user-submitted fields before they hit the prompt.

    Defends against prompt injection via bloat and runaway Gemini token spend.
    """
    out = {}
    for key, cap in _LIMITS.items():
        val = data.get(key, '')
        if not isinstance(val, str):
            val = str(val) if val is not None else ''
        out[key] = val.strip()[:cap]

    # Budget: must be a positive int within sane bounds
    raw_budget = data.get('budget', 2000)
    try:
        b = int(raw_budget)
    except (TypeError, ValueError):
        b = 2000
    out['budget'] = max(100, min(b, 10_000_000))

    # gift_types: list[str] of known tags only
    valid_tags = {"Formal", "Funky", "Romantic", "Practical", "Traditional", "Luxury"}
    raw_types = data.get('gift_types')
    if isinstance(raw_types, list):
        out['gift_types'] = [t for t in raw_types if isinstance(t, str) and t in valid_tags] or None
    else:
        out['gift_types'] = None
    return out


def call_gemini(prompt, max_tokens=2048):
    """Call Gemini API and return the response text."""
    if not GEMINI_API_KEY:
        return None

    try:
        url = f"{GEMINI_API_URL}?key={GEMINI_API_KEY}"
        data = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": max_tokens,
            }
        }

        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
            method='POST'
        )

        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            if 'candidates' in result and len(result['candidates']) > 0:
                return result['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        print(f"Gemini API error: {e}")
    return None


def get_ai_recommendations(relationship, occasion, age_group, vibe, budget, gender, notes, gift_types, city=""):
    """LLM-1: Generate gift recommendations using Gemini."""

    gender_text = f", gender: {gender}" if gender else ""
    notes_text = f"\nSpecial notes from user: {notes}" if notes else ""
    city_text = f"\nBuyer's city: {city} (suggest same-day delivery options from Blinkit/Zepto where relevant)" if city else ""

    # Build preference hints from gift_types but don't restrict
    style_hints = ""
    if gift_types and len(gift_types) < 6:
        style_hints = f"\nUser prefers these styles: {', '.join(gift_types)} (but feel free to suggest others if they fit better)"

    prompt = f"""You are a creative Indian gift consultant who stays updated with the latest trends, viral products, and what's popular right now in {occasion} gifting.

Context:
- Recipient: {relationship}
- Occasion: {occasion}
- Age Group: {age_group}{gender_text}
- Style/Vibe they like: {vibe}
- Budget: Rs.{budget:,} INR{notes_text}{city_text}{style_hints}

Generate exactly 10 UNIQUE and CREATIVE gift recommendations. Think about:
- What's trending right now in India for this occasion
- Popular brands and products that are currently in demand
- Unique experiential gifts (subscriptions, experiences, classes)
- Personalized/customizable options
- Tech gadgets that are currently popular
- Artisanal and handcrafted items from Indian brands
- Wellness and self-care products that are trending
- What would genuinely surprise and delight this person

IMPORTANT:
- Be CREATIVE and SPECIFIC - don't suggest generic items like "Watch" or "Perfume", suggest specific types like "Noise ColorFit Pro 4 Smartwatch" or "Forest Essentials Sandalwood Gift Set"
- Mix different categories - don't repeat similar items
- Consider what's actually popular and available in India RIGHT NOW
- Each gift should feel thoughtful and personalized to this specific person

For each gift, provide in this EXACT JSON format (no markdown, just pure JSON array):
[
  {{
    "title": "Specific Gift Name",
    "gift_type": "Formal|Funky|Romantic|Practical|Traditional|Luxury",
    "description": "Why this specific gift is perfect for them - be personal and specific",
    "price": 1500,
    "icon": "emoji"
  }}
]

Requirements:
- All gifts must be easily purchasable in India
- Prices should be realistic and within budget range (60%-120% of budget)
- Make each suggestion UNIQUE - no two gifts should be from the same category
- Be specific with product names/types, not generic

Return ONLY the JSON array, no other text."""

    response = call_gemini(prompt, max_tokens=2048)
    if response:
        try:
            # Clean up response - remove markdown code blocks if present
            cleaned = response.strip()
            if cleaned.startswith('```'):
                cleaned = cleaned.split('\n', 1)[1] if '\n' in cleaned else cleaned[3:]
            if cleaned.endswith('```'):
                cleaned = cleaned.rsplit('```', 1)[0]
            cleaned = cleaned.strip()
            if cleaned.startswith('json'):
                cleaned = cleaned[4:].strip()

            gifts = json.loads(cleaned)
            if isinstance(gifts, list) and len(gifts) > 0:
                return gifts
        except json.JSONDecodeError as e:
            print(f"JSON parse error: {e}")
    return None


def get_ai_personalization(gifts, relationship, occasion, age_group, gender, notes):
    """LLM-2: Add personalized reasoning for each gift using Gemini."""

    gift_titles = [g.get('title', '') for g in gifts[:10]]
    gender_text = f", {gender}" if gender else ""
    notes_text = f"\nUser's note about them: {notes}" if notes else ""

    prompt = f"""You are a thoughtful gift advisor. For each gift below, write a SHORT, PERSONAL reason why it's perfect for this specific person. Make it feel like advice from a friend, not a sales pitch.

Recipient: {relationship} ({age_group}{gender_text})
Occasion: {occasion}{notes_text}

Gifts:
{json.dumps(gift_titles, indent=2)}

For each gift, write 2-3 short, punchy reasons joined with " • ". Be specific to their situation:
- Reference their relationship naturally ("Your {relationship.lower()} will love...")
- Mention something specific about the occasion
- If notes provided, connect to their interests/personality
- Keep it warm and personal, not generic

Return as JSON object with gift titles as keys:
{{
  "Gift Name 1": "Reason 1 • Reason 2 • Reason 3",
  "Gift Name 2": "Reason 1 • Reason 2"
}}

Return ONLY the JSON object, no other text."""

    response = call_gemini(prompt, max_tokens=1500)
    if response:
        try:
            cleaned = response.strip()
            if cleaned.startswith('```'):
                cleaned = cleaned.split('\n', 1)[1] if '\n' in cleaned else cleaned[3:]
            if cleaned.endswith('```'):
                cleaned = cleaned.rsplit('```', 1)[0]
            cleaned = cleaned.strip()
            if cleaned.startswith('json'):
                cleaned = cleaned[4:].strip()

            reasons = json.loads(cleaned)
            if isinstance(reasons, dict):
                return reasons
        except json.JSONDecodeError as e:
            print(f"JSON parse error in personalization: {e}")
    return None


# Fallback data for when API is unavailable
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


def get_fallback_recommendations(relationship, occasion, age_group, vibe, budget, gender="", notes="", gift_types=None):
    """Fallback to rule-based recommendations when AI is unavailable."""
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
            else:
                why_reasons.append(f"Ideal for celebrating {occasion}")

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
                "purchase_links": add_affiliate_tags({
                    "amazon": f"https://www.amazon.in/s?k={encoded_item}",
                    "flipkart": f"https://www.flipkart.com/search?q={encoded_item}",
                    "myntra": f"https://www.myntra.com/{encoded_item}",
                    "shoppersstop": f"https://www.shoppersstop.com/search?q={encoded_item}",
                    "blinkit": f"https://blinkit.com/s/?q={encoded_item}",
                    "meesho": f"https://www.meesho.com/search?q={encoded_item}"
                })
            })
        attempt += 1

    return recommendations


def get_recommendations(relationship, occasion, age_group, vibe, budget, gender="", notes="", gift_types=None, city=""):
    """Main function that uses dual-LLM approach with fallback."""
    if gift_types is None:
        gift_types = ["Formal", "Funky", "Romantic", "Practical", "Traditional", "Luxury"]

    rel_type = RELATIONSHIPS.get(relationship.lower(), "general")
    occ_type = OCCASIONS.get(occasion.lower(), "celebration")

    ai_powered = False
    recommendations = []

    # Try AI-powered recommendations if API key is available
    if GEMINI_API_KEY:
        # LLM-1: Generate gift ideas
        ai_gifts = get_ai_recommendations(relationship, occasion, age_group, vibe, budget, gender, notes, gift_types, city)

        if ai_gifts:
            # LLM-2: Add personalized reasoning
            personalization = get_ai_personalization(ai_gifts, relationship, occasion, age_group, gender, notes)

            for i, gift in enumerate(ai_gifts[:10]):
                title = gift.get('title', 'Gift')
                encoded_item = quote_plus(title)

                # Get personalized reason from LLM-2, or use LLM-1's description
                why_applicable = gift.get('description', '')
                if personalization and title in personalization:
                    why_applicable = personalization[title]

                recommendations.append({
                    "id": i + 1,
                    "title": title,
                    "icon": gift.get('icon', '🎁'),
                    "gift_type": gift.get('gift_type', 'Practical'),
                    "description": gift.get('description', f"Perfect gift for {relationship}"),
                    "why_applicable": why_applicable,
                    "approx_price_inr": f"Rs.{gift.get('price', budget):,}",
                    "purchase_links": add_affiliate_tags({
                        "amazon": f"https://www.amazon.in/s?k={encoded_item}",
                        "flipkart": f"https://www.flipkart.com/search?q={encoded_item}",
                        "myntra": f"https://www.myntra.com/{encoded_item}",
                        "shoppersstop": f"https://www.shoppersstop.com/search?q={encoded_item}",
                        "blinkit": f"https://blinkit.com/s/?q={encoded_item}",
                        "meesho": f"https://www.meesho.com/search?q={encoded_item}"
                    })
                })
            ai_powered = True

    # Fallback to rule-based if AI failed or no API key
    if not recommendations:
        recommendations = get_fallback_recommendations(
            relationship, occasion, age_group, vibe, budget, gender, notes, gift_types
        )

    pro_tip = PRO_TIPS.get(occasion.lower(), PRO_TIPS.get("professional" if rel_type == "professional" else "default", PRO_TIPS["default"]))

    gender_text = f", {gender} gender" if gender else ""
    notes_text = f", with special note: '{notes[:30]}...'" if notes and len(notes) > 30 else (f", with note: '{notes}'" if notes else "")
    types_text = f", filtering by: {', '.join(gift_types)}" if len(gift_types) < 6 else ""
    ai_text = " [AI-Powered by Gemini]" if ai_powered else " [Smart Recommendations]"

    return {
        "thinking_trace": f"Analyzing gift for {relationship} on {occasion}. Considering {rel_type} relationship type, {occ_type} occasion, {age_group} age group{gender_text}, {vibe} style preference, and Rs.{budget:,} budget{notes_text}{types_text}.{ai_text}",
        "recommendations": recommendations,
        "pro_tip": pro_tip,
        "ai_powered": ai_powered
    }


_MAX_REQUEST_BYTES = 8 * 1024  # 8KB is more than enough for our payload


class handler(BaseHTTPRequestHandler):
    def _send_json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0) or 0)
        except (TypeError, ValueError):
            self._send_json(400, {"error": "invalid content-length"})
            return

        if content_length <= 0 or content_length > _MAX_REQUEST_BYTES:
            self._send_json(413, {"error": "request too large"})
            return

        try:
            body = self.rfile.read(content_length)
            data = json.loads(body)
            if not isinstance(data, dict):
                raise ValueError("body is not an object")
        except (json.JSONDecodeError, ValueError, UnicodeDecodeError):
            self._send_json(400, {"error": "invalid request body"})
            return

        clean = _sanitize_inputs(data)

        try:
            result = get_recommendations(
                clean['relationship'] or 'Friend',
                clean['occasion'] or 'Birthday',
                clean['age_group'] or 'Adult',
                clean['vibe'] or 'Traditional',
                clean['budget'],
                clean['gender'],
                clean['notes'],
                clean['gift_types'],
                clean.get('city', ''),
            )
        except Exception as exc:
            # Last-resort guard. Log to Vercel function logs but don't leak details.
            print(f"recommend error: {type(exc).__name__}: {exc}")
            self._send_json(500, {"error": "internal error"})
            return

        self._send_json(200, result)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Access-Control-Max-Age', '86400')
        self.end_headers()
