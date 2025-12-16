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

# Gift type classification
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

# Emoji icons for each gift type
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
    "Story Books Set": "📚", "Healthy Snack Box": "🥗", "Cricket Kit": "🏏", "Football": "⚽",
    "Doll House Set": "🏠", "Dance Costume Set": "💃", "Jewelry Making Kit": "💎"
}

# Fashion/lifestyle items that work on Myntra
FASHION_ITEMS = ["saree", "kurta", "jewelry", "watch", "sunglasses", "handbag", "wallet", "perfume", "grooming", "skincare"]

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


def get_purchase_links(item, budget):
    """Generate working e-commerce links with price filters"""
    encoded_item = quote_plus(item)
    min_price = int(budget * 0.5)
    max_price = int(budget * 1.2)
    
    links = {}
    
    # Amazon India - with price filter
    links["amazon"] = f"https://www.amazon.in/s?k={encoded_item}&rh=p_36%3A{min_price}00-{max_price}00"
    
    # Flipkart - with price filter  
    links["flipkart"] = f"https://www.flipkart.com/search?q={encoded_item}&p%5B%5D=facets.price_range.from%3D{min_price}&p%5B%5D=facets.price_range.to%3D{max_price}"
    
    # Myntra - ONLY for fashion/lifestyle items
    item_lower = item.lower()
    if any(f in item_lower for f in FASHION_ITEMS):
        links["myntra"] = f"https://www.myntra.com/{encoded_item.replace('+', '-').lower()}"
    
    # Meesho - works for most items
    links["meesho"] = f"https://www.meesho.com/search?q={encoded_item}"
    
    return links


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

            if notes and notes.strip():
                why_reasons.append(f"Considering your note: {notes.strip()[:50]}")

            why_applicable = " • ".join(why_reasons[:3])
            gift_type_tag = GIFT_TYPE_TAGS.get(item, "Practical")
            icon = GIFT_ICONS.get(item, "🎁")
            purchase_links = get_purchase_links(item, budget)

            recommendations.append({
                "id": len(recommendations) + 1,
                "title": item,
                "icon": icon,
                "gift_type": gift_type_tag,
                "description": descriptions[len(recommendations) % len(descriptions)],
                "why_applicable": why_applicable,
                "approx_price_inr": f"₹{price:,}",
                "purchase_links": purchase_links
            })
        attempt += 1

    pro_tip = PRO_TIPS.get(occasion.lower(), PRO_TIPS.get("professional" if rel_type == "professional" else "default", PRO_TIPS["default"]))

    gender_text = f", {gender} gender" if gender else ""
    notes_text = f", with special note: '{notes[:30]}...'" if notes and len(notes) > 30 else (f", with note: '{notes}'" if notes else "")
    types_text = f", filtering by: {', '.join(gift_types)}" if len(gift_types) < 6 else ""

    return {
        "thinking_trace": f"Analyzing gift for {relationship} on {occasion}. Considering {rel_type} relationship type, {occ_type} occasion, {age_group} age group{gender_text}, {vibe} style preference, and ₹{budget:,} budget{notes_text}{types_text}.",
        "recommendations": recommendations,
        "pro_tip": pro_tip
    }


HTML_PAGE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GiftingGenie - Your Personal Gifting Concierge</title>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🎁</text></svg>">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-primary: #ffffff;
            --bg-secondary: #f8fafc;
            --bg-card: rgba(255, 255, 255, 0.95);
            --text-primary: #1e293b;
            --text-secondary: #64748b;
            --text-muted: #94a3b8;
            --border-color: #e2e8f0;
            --accent-primary: #0d9488;
            --accent-secondary: #0891b2;
            --accent-gradient: linear-gradient(135deg, #0d9488 0%, #0891b2 100%);
            --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
            --shadow-md: 0 4px 6px rgba(0,0,0,0.07);
            --shadow-lg: 0 25px 50px rgba(0,0,0,0.15);
            --glass-bg: rgba(255, 255, 255, 0.85);
            --glass-border: rgba(255, 255, 255, 0.3);
        }
        
        [data-theme="dark"] {
            --bg-primary: #0f172a;
            --bg-secondary: #1e293b;
            --bg-card: rgba(30, 41, 59, 0.95);
            --text-primary: #f1f5f9;
            --text-secondary: #94a3b8;
            --text-muted: #64748b;
            --border-color: #334155;
            --accent-primary: #14b8a6;
            --accent-secondary: #22d3ee;
            --accent-gradient: linear-gradient(135deg, #14b8a6 0%, #22d3ee 100%);
            --shadow-lg: 0 25px 50px rgba(0,0,0,0.5);
            --glass-bg: rgba(30, 41, 59, 0.85);
            --glass-border: rgba(71, 85, 105, 0.5);
        }
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body { 
            font-family: 'Inter', sans-serif; 
            background: linear-gradient(-45deg, #0d9488, #0891b2, #6366f1, #8b5cf6);
            background-size: 400% 400%;
            animation: gradientShift 15s ease infinite;
            min-height: 100vh; 
            padding: 20px; 
            color: var(--text-primary);
            transition: all 0.3s ease;
        }
        
        [data-theme="dark"] body {
            background: linear-gradient(-45deg, #0f172a, #1e293b, #312e81, #4c1d95);
        }
        
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        .container { max-width: 1200px; margin: 0 auto; }
        
        /* Theme Toggle */
        .theme-toggle {
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 1000;
            background: var(--glass-bg);
            backdrop-filter: blur(10px);
            border: 1px solid var(--glass-border);
            border-radius: 50px;
            padding: 8px;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 8px;
            transition: all 0.3s ease;
            box-shadow: var(--shadow-md);
        }
        .theme-toggle:hover {
            transform: scale(1.05);
            box-shadow: var(--shadow-lg);
        }
        .theme-toggle .icon {
            font-size: 1.2rem;
            transition: transform 0.3s ease;
        }
        .theme-toggle:hover .icon {
            transform: rotate(20deg);
        }
        
        .header { text-align: center; color: white; margin-bottom: 40px; animation: fadeInDown 0.8s ease-out; }
        .header h1 { font-size: 3rem; font-weight: 700; margin-bottom: 10px; text-shadow: 2px 2px 4px rgba(0,0,0,0.2); }
        .header .subtitle { font-size: 1.2rem; font-weight: 300; opacity: 0.95; }
        .header .emoji { font-size: 3.5rem; display: inline-block; animation: bounce 2s infinite; }
        
        .main-card { 
            background: var(--glass-bg);
            backdrop-filter: blur(20px);
            border-radius: 24px; 
            padding: 40px; 
            box-shadow: var(--shadow-lg);
            animation: fadeInUp 0.8s ease-out;
            border: 1px solid var(--glass-border);
        }
        
        .form-title { 
            font-size: 1.8rem; 
            color: var(--accent-primary); 
            margin-bottom: 30px; 
            text-align: center; 
            font-weight: 600; 
        }
        
        /* Step Progress Indicator */
        .step-progress {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-bottom: 35px;
            gap: 8px;
        }
        .step-dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: var(--border-color);
            transition: all 0.3s ease;
        }
        .step-dot.active {
            background: var(--accent-gradient);
            transform: scale(1.3);
            box-shadow: 0 0 10px rgba(13, 148, 136, 0.5);
        }
        .step-dot.completed {
            background: var(--accent-primary);
        }
        .step-line {
            width: 40px;
            height: 3px;
            background: var(--border-color);
            border-radius: 2px;
            transition: all 0.3s ease;
        }
        .step-line.completed {
            background: var(--accent-primary);
        }
        
        /* Form Steps */
        .form-step {
            display: none;
            animation: fadeIn 0.4s ease;
        }
        .form-step.active {
            display: block;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .step-title {
            font-size: 1.3rem;
            color: var(--text-primary);
            margin-bottom: 20px;
            text-align: center;
            font-weight: 500;
        }
        .step-subtitle {
            color: var(--text-secondary);
            text-align: center;
            margin-bottom: 25px;
            font-size: 0.95rem;
        }
        
        /* Category Cards for Step 1 */
        .category-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-bottom: 25px;
        }
        .category-card {
            background: var(--bg-secondary);
            border: 2px solid var(--border-color);
            border-radius: 16px;
            padding: 20px 15px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }
        .category-card:hover {
            transform: translateY(-5px);
            border-color: var(--accent-primary);
            box-shadow: 0 10px 30px rgba(13, 148, 136, 0.15);
        }
        .category-card.selected {
            background: var(--accent-gradient);
            border-color: transparent;
            color: white;
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(13, 148, 136, 0.3);
        }
        .category-card .icon {
            font-size: 2.5rem;
            margin-bottom: 10px;
            display: block;
        }
        .category-card .label {
            font-weight: 600;
            font-size: 0.95rem;
        }
        
        /* Occasion Pills for Step 2 */
        .occasion-pills {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            justify-content: center;
            margin-bottom: 25px;
        }
        .occasion-pill {
            padding: 12px 20px;
            border: 2px solid var(--border-color);
            border-radius: 50px;
            background: var(--bg-secondary);
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 500;
            font-size: 0.9rem;
            color: var(--text-primary);
        }
        .occasion-pill:hover {
            border-color: var(--accent-primary);
            background: rgba(13, 148, 136, 0.1);
        }
        .occasion-pill.selected {
            background: var(--accent-gradient);
            border-color: transparent;
            color: white;
            box-shadow: 0 4px 15px rgba(13, 148, 136, 0.3);
        }
        
        /* Relationship Cards */
        .relationship-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 12px;
            margin-bottom: 25px;
        }
        .relationship-card {
            background: var(--bg-secondary);
            border: 2px solid var(--border-color);
            border-radius: 12px;
            padding: 15px 10px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .relationship-card:hover {
            border-color: var(--accent-primary);
            transform: translateY(-3px);
        }
        .relationship-card.selected {
            background: var(--accent-gradient);
            border-color: transparent;
            color: white;
        }
        .relationship-card.suggested {
            border-color: var(--accent-primary);
            background: rgba(13, 148, 136, 0.1);
        }
        .relationship-card.suggested::after {
            content: '★';
            position: absolute;
            top: -5px;
            right: -5px;
            background: #fbbf24;
            color: white;
            font-size: 0.6rem;
            width: 16px;
            height: 16px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .relationship-card {
            position: relative;
        }
        .relationship-card .emoji {
            font-size: 1.5rem;
            display: block;
            margin-bottom: 5px;
        }
        .relationship-card .name {
            font-size: 0.8rem;
            font-weight: 500;
        }
        
        .form-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 20px; margin-bottom: 30px; }
        
        .form-group { display: flex; flex-direction: column; }
        .form-group label { font-weight: 600; margin-bottom: 8px; color: var(--text-secondary); font-size: 0.9rem; }
        .form-group select, .form-group input { 
            padding: 14px 16px; 
            border: 2px solid var(--border-color); 
            border-radius: 12px; 
            font-size: 1rem; 
            font-family: 'Inter', sans-serif; 
            transition: all 0.3s ease; 
            background: var(--bg-secondary);
            color: var(--text-primary);
        }
        .form-group select:focus, .form-group input:focus { 
            outline: none; 
            border-color: var(--accent-primary); 
            background: var(--bg-primary); 
            box-shadow: 0 0 0 4px rgba(13, 148, 136, 0.15); 
        }
        
        .form-group.gender-auto-set select {
            background: linear-gradient(135deg, rgba(13, 148, 136, 0.1) 0%, rgba(8, 145, 178, 0.1) 100%);
            border-color: var(--accent-primary);
        }
        .form-group.gender-auto-set::after {
            content: '✓ Auto-detected';
            font-size: 0.75rem;
            color: var(--accent-primary);
            margin-top: 4px;
            font-weight: 500;
        }
        
        .form-group textarea { 
            padding: 14px 16px; 
            border: 2px solid var(--border-color); 
            border-radius: 12px; 
            font-size: 1rem; 
            font-family: 'Inter', sans-serif; 
            transition: all 0.3s ease; 
            background: var(--bg-secondary);
            color: var(--text-primary);
            resize: vertical; 
            min-height: 80px; 
        }
        .form-group textarea:focus { 
            outline: none; 
            border-color: var(--accent-primary); 
            background: var(--bg-primary); 
            box-shadow: 0 0 0 4px rgba(13, 148, 136, 0.15); 
        }
        
        .full-width { grid-column: 1 / -1; }
        
        /* Navigation Buttons */
        .nav-buttons {
            display: flex;
            gap: 15px;
            justify-content: center;
            margin-top: 25px;
        }
        .nav-btn {
            padding: 14px 35px;
            border-radius: 12px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 1rem;
            font-family: 'Inter', sans-serif;
        }
        .nav-btn.secondary {
            background: var(--bg-secondary);
            color: var(--text-primary);
            border: 2px solid var(--border-color);
        }
        .nav-btn.secondary:hover {
            border-color: var(--accent-primary);
            background: rgba(13, 148, 136, 0.1);
        }
        .nav-btn.primary {
            background: var(--accent-gradient);
            color: white;
            border: none;
            box-shadow: 0 4px 15px rgba(13, 148, 136, 0.3);
        }
        .nav-btn.primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(13, 148, 136, 0.4);
        }
        .nav-btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            transform: none !important;
        }
        
        .submit-btn { 
            width: 100%; 
            padding: 18px; 
            background: var(--accent-gradient);
            color: white; 
            border: none; 
            border-radius: 12px; 
            font-size: 1.2rem; 
            font-weight: 600; 
            cursor: pointer; 
            transition: all 0.3s ease; 
            box-shadow: 0 4px 20px rgba(13, 148, 136, 0.4); 
        }
        .submit-btn:hover { 
            transform: translateY(-3px) scale(1.01); 
            box-shadow: 0 8px 30px rgba(13, 148, 136, 0.5); 
        }
        
        .gift-types-section { margin-bottom: 25px; }
        .gift-types-label { font-weight: 600; margin-bottom: 12px; color: var(--text-secondary); font-size: 0.9rem; display: block; }
        .gift-types-grid { display: flex; flex-wrap: wrap; gap: 10px; }
        .gift-type-checkbox { display: none; }
        .gift-type-label { 
            padding: 10px 18px; 
            border: 2px solid var(--border-color); 
            border-radius: 25px; 
            cursor: pointer; 
            transition: all 0.3s ease; 
            font-size: 0.9rem; 
            font-weight: 500; 
            background: var(--bg-secondary);
            color: var(--text-secondary);
        }
        .gift-type-checkbox:checked + .gift-type-label { 
            background: var(--accent-gradient);
            color: white; 
            border-color: transparent; 
            box-shadow: 0 4px 15px rgba(13, 148, 136, 0.3); 
        }
        .gift-type-label:hover { 
            border-color: var(--accent-primary); 
        }
        
        .loading { display: none; text-align: center; padding: 50px; }
        .spinner { border: 4px solid var(--border-color); border-top: 4px solid var(--accent-primary); border-radius: 50%; width: 50px; height: 50px; animation: spin 1s linear infinite; margin: 0 auto 20px; }
        
        .results-section { display: none; margin-top: 40px; }
        .results-header { text-align: center; margin-bottom: 25px; }
        .results-header h2 { font-size: 2rem; color: var(--accent-primary); }
        
        .thinking-trace { 
            background: linear-gradient(135deg, rgba(13, 148, 136, 0.1) 0%, rgba(8, 145, 178, 0.1) 100%); 
            padding: 20px; 
            border-radius: 12px; 
            margin-bottom: 25px; 
            border-left: 4px solid var(--accent-primary); 
        }
        .thinking-trace h3 { color: var(--accent-primary); font-size: 1rem; margin-bottom: 8px; }
        .thinking-trace p { color: var(--text-secondary); line-height: 1.6; font-size: 0.95rem; }
        
        .gifts-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(340px, 1fr)); gap: 24px; margin-bottom: 25px; }
        
        .gift-card { 
            background: var(--bg-card);
            border-radius: 20px; 
            padding: 28px; 
            box-shadow: var(--shadow-md);
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); 
            border: 2px solid transparent; 
            position: relative;
        }
        .gift-card:hover { 
            transform: translateY(-8px) scale(1.02); 
            box-shadow: 0 20px 60px rgba(13, 148, 136, 0.2); 
            border-color: var(--accent-primary); 
        }
        
        .gift-header { display: flex; align-items: center; gap: 15px; margin-bottom: 15px; }
        .gift-icon { 
            font-size: 3rem; 
            background: linear-gradient(135deg, rgba(13, 148, 136, 0.15) 0%, rgba(8, 145, 178, 0.15) 100%); 
            width: 75px; 
            height: 75px; 
            display: flex; 
            align-items: center; 
            justify-content: center; 
            border-radius: 18px; 
            box-shadow: 0 6px 20px rgba(13, 148, 136, 0.15); 
        }
        .gift-info { flex: 1; }
        .gift-number { 
            display: inline-flex; 
            align-items: center; 
            justify-content: center; 
            background: var(--accent-gradient);
            color: white; 
            width: 26px; 
            height: 26px; 
            border-radius: 50%; 
            font-weight: 600; 
            font-size: 0.8rem; 
            margin-bottom: 5px; 
        }
        .gift-title { font-size: 1.2rem; color: var(--text-primary); font-weight: 600; line-height: 1.3; }
        
        .gift-description { color: var(--text-secondary); margin-bottom: 12px; line-height: 1.5; font-size: 0.9rem; }
        
        .gift-why { 
            background: linear-gradient(135deg, rgba(13, 148, 136, 0.08) 0%, rgba(8, 145, 178, 0.08) 100%); 
            padding: 14px; 
            border-radius: 10px; 
            margin-bottom: 14px; 
            border-left: 3px solid var(--accent-primary); 
        }
        .gift-why-label { font-weight: 600; color: var(--accent-primary); font-size: 0.8rem; margin-bottom: 4px; }
        .gift-why-text { color: var(--text-secondary); font-size: 0.85rem; line-height: 1.5; }
        
        .gift-price { font-size: 1.6rem; color: var(--accent-primary); font-weight: 700; margin-bottom: 16px; }
        
        .purchase-links { display: flex; flex-wrap: wrap; gap: 8px; }
        .purchase-btn { 
            padding: 10px 16px; 
            border-radius: 8px; 
            text-decoration: none; 
            text-align: center; 
            font-weight: 600; 
            transition: all 0.3s ease; 
            font-size: 0.8rem; 
            color: white; 
            flex: 1;
            min-width: 80px;
        }
        .amazon-btn { background: linear-gradient(135deg, #FF9900 0%, #FF6600 100%); }
        .flipkart-btn { background: linear-gradient(135deg, #2874F0 0%, #1a5dc8 100%); }
        .myntra-btn { background: linear-gradient(135deg, #ff3e6c 0%, #e8304f 100%); }
        .meesho-btn { background: linear-gradient(135deg, #570741 0%, #3d0530 100%); }
        .shoppersstop-btn { background: linear-gradient(135deg, #000000 0%, #333333 100%); }
        .blinkit-btn { background: linear-gradient(135deg, #f8cb46 0%, #e5b93d 100%); color: #000; }
        .purchase-btn:hover { opacity: 0.9; transform: scale(1.03); box-shadow: 0 4px 12px rgba(0,0,0,0.2); }
        
        .pro-tip { 
            background: linear-gradient(135deg, rgba(251, 191, 36, 0.2) 0%, rgba(16, 185, 129, 0.2) 100%); 
            padding: 20px; 
            border-radius: 12px; 
            text-align: center; 
            margin-bottom: 20px; 
        }
        .pro-tip h3 { color: var(--accent-primary); font-size: 1.1rem; margin-bottom: 8px; }
        .pro-tip p { color: var(--text-secondary); line-height: 1.6; }
        
        .button-group { display: flex; gap: 15px; justify-content: center; flex-wrap: wrap; }
        .back-btn { 
            padding: 14px 45px; 
            background: var(--bg-secondary); 
            color: var(--accent-primary); 
            border: 2px solid var(--accent-primary); 
            border-radius: 12px; 
            font-weight: 600; 
            cursor: pointer; 
            transition: all 0.3s ease; 
            font-size: 1rem; 
        }
        .back-btn:hover { 
            background: var(--accent-primary); 
            color: white; 
            transform: translateY(-2px); 
        }
        .edit-btn { 
            padding: 14px 45px; 
            background: var(--accent-gradient);
            color: white; 
            border: none; 
            border-radius: 12px; 
            font-weight: 600; 
            cursor: pointer; 
            transition: all 0.3s ease; 
            font-size: 1rem; 
            box-shadow: 0 4px 15px rgba(13, 148, 136, 0.3); 
        }
        .edit-btn:hover { 
            transform: translateY(-2px); 
            box-shadow: 0 6px 20px rgba(13, 148, 136, 0.5); 
        }
        
        .error { background: rgba(239, 68, 68, 0.1); color: #ef4444; padding: 15px; border-radius: 10px; margin-top: 15px; display: none; text-align: center; }
        
        .gift-type-tag { 
            position: absolute; 
            top: 14px; 
            right: 14px; 
            padding: 5px 14px; 
            border-radius: 20px; 
            font-size: 0.7rem; 
            font-weight: 600; 
            text-transform: uppercase; 
            letter-spacing: 0.5px; 
        }
        .tag-formal { background: linear-gradient(135deg, #1e40af, #1d4ed8); color: white; }
        .tag-funky { background: linear-gradient(135deg, #dc2626, #ef4444); color: white; }
        .tag-romantic { background: linear-gradient(135deg, #db2777, #ec4899); color: white; }
        .tag-practical { background: linear-gradient(135deg, #059669, #10b981); color: white; }
        .tag-traditional { background: linear-gradient(135deg, #d97706, #f59e0b); color: white; }
        .tag-luxury { background: linear-gradient(135deg, #7c3aed, #8b5cf6); color: white; }
        
        /* Confetti Animation */
        .confetti {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 9999;
            overflow: hidden;
        }
        .confetti-piece {
            position: absolute;
            width: 10px;
            height: 10px;
            opacity: 0;
        }
        
        @keyframes fadeInDown { from { opacity: 0; transform: translateY(-30px); } to { opacity: 1; transform: translateY(0); } }
        @keyframes fadeInUp { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: translateY(0); } }
        @keyframes bounce { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-10px); } }
        @keyframes spin { to { transform: rotate(360deg); } }
        
        @media (max-width: 768px) { 
            .header h1 { font-size: 2.2rem; } 
            .main-card { padding: 25px; } 
            .form-grid { grid-template-columns: 1fr; } 
            .purchase-links { flex-direction: column; }
            .purchase-btn { width: 100%; }
            .gifts-grid { grid-template-columns: 1fr; }
            .category-grid { grid-template-columns: repeat(2, 1fr); }
            .relationship-grid { grid-template-columns: repeat(3, 1fr); }
            .theme-toggle { top: 10px; right: 10px; }
        }
    </style>
</head>
<body>
    <button class="theme-toggle" onclick="toggleTheme()" title="Toggle Dark Mode">
        <span class="icon" id="themeIcon">🌙</span>
    </button>
    
    <div class="container">
        <div class="header">
            <div class="emoji">🎁</div>
            <h1>GiftingGenie</h1>
            <p class="subtitle">Your Personal Indian Gifting Concierge - Find the Perfect Gift</p>
        </div>
        <div class="main-card">
            <div id="formSection">
                <h2 class="form-title">Let's Find the Perfect Gift!</h2>
                
                <!-- Step Progress -->
                <div class="step-progress">
                    <div class="step-dot active" id="dot1"></div>
                    <div class="step-line" id="line1"></div>
                    <div class="step-dot" id="dot2"></div>
                    <div class="step-line" id="line2"></div>
                    <div class="step-dot" id="dot3"></div>
                    <div class="step-line" id="line3"></div>
                    <div class="step-dot" id="dot4"></div>
                </div>
                
                <form id="giftForm">
                    <!-- Step 1: Occasion Category -->
                    <div class="form-step active" id="step1">
                        <h3 class="step-title">What's the occasion?</h3>
                        <p class="step-subtitle">Select a category to see relevant occasions</p>
                        
                        <div class="category-grid">
                            <div class="category-card" data-category="festivals" onclick="selectCategory(this)">
                                <span class="icon">🪔</span>
                                <span class="label">Festivals</span>
                            </div>
                            <div class="category-card" data-category="milestones" onclick="selectCategory(this)">
                                <span class="icon">🎉</span>
                                <span class="label">Life Events</span>
                            </div>
                            <div class="category-card" data-category="special" onclick="selectCategory(this)">
                                <span class="icon">💝</span>
                                <span class="label">Special Days</span>
                            </div>
                            <div class="category-card" data-category="religious" onclick="selectCategory(this)">
                                <span class="icon">🙏</span>
                                <span class="label">Religious</span>
                            </div>
                        </div>
                        
                        <div class="occasion-pills" id="occasionPills" style="display: none;">
                            <!-- Dynamically populated -->
                        </div>
                        
                        <input type="hidden" id="occasion" name="occasion" required>
                        
                        <div class="nav-buttons">
                            <button type="button" class="nav-btn primary" onclick="nextStep()" id="step1Next" disabled>Next →</button>
                        </div>
                    </div>
                    
                    <!-- Step 2: Relationship -->
                    <div class="form-step" id="step2">
                        <h3 class="step-title">Who is the gift for?</h3>
                        <p class="step-subtitle" id="relationshipSubtitle">Select your relationship with the recipient</p>
                        
                        <div class="relationship-grid" id="relationshipGrid">
                            <!-- Dynamically populated based on occasion -->
                        </div>
                        
                        <input type="hidden" id="relationship" name="relationship" required>
                        <input type="hidden" id="gender" name="gender">
                        
                        <div class="nav-buttons">
                            <button type="button" class="nav-btn secondary" onclick="prevStep()">← Back</button>
                            <button type="button" class="nav-btn primary" onclick="nextStep()" id="step2Next" disabled>Next →</button>
                        </div>
                    </div>
                    
                    <!-- Step 3: Details -->
                    <div class="form-step" id="step3">
                        <h3 class="step-title">A few more details...</h3>
                        <p class="step-subtitle">Help us personalize your recommendations</p>
                        
                        <div class="form-grid">
                            <div class="form-group">
                                <label>🎂 Age Group</label>
                                <select id="ageGroup" required>
                                    <option value="">Select Age Group</option>
                                    <option value="Child">Child (0-12)</option>
                                    <option value="Teenager">Teenager (13-19)</option>
                                    <option value="Adult">Adult (20-59)</option>
                                    <option value="Senior">Senior (60+)</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label>✨ Vibe/Style</label>
                                <select id="vibe" required>
                                    <option value="">Select Vibe</option>
                                    <option value="Traditional">Traditional/Ethnic</option>
                                    <option value="Modern">Modern/Contemporary</option>
                                    <option value="Personalized">Personalized</option>
                                    <option value="Luxury">Luxury/Premium</option>
                                    <option value="Wellness">Wellness-focused</option>
                                    <option value="Tech">Tech-savvy</option>
                                    <option value="Romantic">Romantic</option>
                                    <option value="Fun">Fun/Quirky</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label>💰 Budget (INR)</label>
                                <input type="number" id="budget" placeholder="e.g., 2000" min="100" max="1000000" required>
                            </div>
                            <div class="form-group full-width">
                                <label>📝 Anything special about them?</label>
                                <textarea id="notes" placeholder="e.g., She loves painting, He's a coffee enthusiast, They're into fitness..."></textarea>
                            </div>
                        </div>
                        
                        <div class="nav-buttons">
                            <button type="button" class="nav-btn secondary" onclick="prevStep()">← Back</button>
                            <button type="button" class="nav-btn primary" onclick="nextStep()" id="step3Next">Next →</button>
                        </div>
                    </div>
                    
                    <!-- Step 4: Gift Types & Submit -->
                    <div class="form-step" id="step4">
                        <h3 class="step-title">Almost there! 🎯</h3>
                        <p class="step-subtitle">Select gift types you'd like to see</p>
                        
                        <div class="gift-types-section">
                            <div class="gift-types-grid">
                                <input type="checkbox" id="type-formal" class="gift-type-checkbox" checked>
                                <label for="type-formal" class="gift-type-label">💼 Formal</label>
                                <input type="checkbox" id="type-funky" class="gift-type-checkbox" checked>
                                <label for="type-funky" class="gift-type-label">🎉 Funky</label>
                                <input type="checkbox" id="type-romantic" class="gift-type-checkbox" checked>
                                <label for="type-romantic" class="gift-type-label">💕 Romantic</label>
                                <input type="checkbox" id="type-practical" class="gift-type-checkbox" checked>
                                <label for="type-practical" class="gift-type-label">🔧 Practical</label>
                                <input type="checkbox" id="type-traditional" class="gift-type-checkbox" checked>
                                <label for="type-traditional" class="gift-type-label">🪔 Traditional</label>
                                <input type="checkbox" id="type-luxury" class="gift-type-checkbox" checked>
                                <label for="type-luxury" class="gift-type-label">💎 Luxury</label>
                            </div>
                        </div>
                        
                        <div class="nav-buttons" style="flex-direction: column; gap: 15px;">
                            <button type="submit" class="submit-btn">✨ Find Perfect Gifts</button>
                            <button type="button" class="nav-btn secondary" onclick="prevStep()" style="width: 100%;">← Back</button>
                        </div>
                    </div>
                </form>
                <div class="error" id="error"></div>
            </div>
            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p style="color: var(--accent-primary); font-size: 1.1rem;">🔮 Finding perfect gifts for you...</p>
                <p style="color: var(--text-secondary); font-size: 0.9rem; margin-top: 10px;">Analyzing preferences and cultural context</p>
            </div>
            <div class="results-section" id="results">
                <div class="results-header">
                    <h2>🎁 Your Perfect Gift Ideas</h2>
                </div>
                <div class="thinking-trace" id="thinkingTrace">
                    <h3>💭 Our Recommendation Logic</h3>
                    <p id="thinkingText"></p>
                </div>
                <div class="gifts-grid" id="giftsGrid"></div>
                <div class="pro-tip" id="proTip">
                    <h3>💡 Pro Tip</h3>
                    <p id="proTipText"></p>
                </div>
                <div class="button-group">
                    <button class="edit-btn" onclick="editRequest()">✏️ Edit Request</button>
                    <button class="back-btn" onclick="reset()">🔄 Start Over</button>
                </div>
            </div>
        </div>
    </div>
    
    <div class="confetti" id="confetti"></div>
    
    <script>
        // Theme Management
        function toggleTheme() {
            const html = document.documentElement;
            const currentTheme = html.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            html.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            document.getElementById('themeIcon').textContent = newTheme === 'dark' ? '☀️' : '🌙';
        }
        
        // Load saved theme
        (function() {
            const savedTheme = localStorage.getItem('theme') || 'light';
            document.documentElement.setAttribute('data-theme', savedTheme);
            document.getElementById('themeIcon').textContent = savedTheme === 'dark' ? '☀️' : '🌙';
        })();
        
        // Step Management
        let currentStep = 1;
        const totalSteps = 4;
        
        // Data
        const OCCASION_CATEGORIES = {
            festivals: [
                { value: 'Diwali', label: '🪔 Diwali' },
                { value: 'Holi', label: '🎨 Holi' },
                { value: 'Raksha Bandhan', label: '🧵 Raksha Bandhan' },
                { value: 'Durga Puja', label: '🙏 Durga Puja' },
                { value: 'Ganesh Chaturthi', label: '🐘 Ganesh Chaturthi' },
                { value: 'Navratri', label: '💃 Navratri' },
                { value: 'Karva Chauth', label: '🌙 Karva Chauth' },
                { value: 'Pongal', label: '🌾 Pongal' },
                { value: 'Onam', label: '🛶 Onam' }
            ],
            milestones: [
                { value: 'Birthday', label: '🎂 Birthday' },
                { value: 'Anniversary', label: '💑 Anniversary' },
                { value: 'Wedding', label: '💒 Wedding' },
                { value: 'Graduation', label: '🎓 Graduation' },
                { value: 'Promotion', label: '📈 Promotion' },
                { value: 'Baby Shower', label: '👶 Baby Shower' },
                { value: 'House Warming', label: '🏠 House Warming' },
                { value: 'Retirement', label: '🌅 Retirement' }
            ],
            special: [
                { value: "Valentine's Day", label: '💕 Valentine\\'s Day' },
                { value: "Mother's Day", label: '👩 Mother\\'s Day' },
                { value: "Father's Day", label: '👨 Father\\'s Day' },
                { value: 'New Year', label: '🎆 New Year' }
            ],
            religious: [
                { value: 'Eid', label: '☪️ Eid' },
                { value: 'Christmas', label: '🎄 Christmas' }
            ]
        };
        
        const RELATIONSHIPS = {
            immediate: [
                { value: 'Mother', label: 'Mother', emoji: '👩', gender: 'Female' },
                { value: 'Father', label: 'Father', emoji: '👨', gender: 'Male' },
                { value: 'Brother', label: 'Brother', emoji: '👦', gender: 'Male' },
                { value: 'Sister', label: 'Sister', emoji: '👧', gender: 'Female' },
                { value: 'Wife', label: 'Wife', emoji: '👰', gender: 'Female' },
                { value: 'Husband', label: 'Husband', emoji: '🤵', gender: 'Male' },
                { value: 'Son', label: 'Son', emoji: '👦', gender: 'Male' },
                { value: 'Daughter', label: 'Daughter', emoji: '👧', gender: 'Female' },
                { value: 'Grandparent', label: 'Grandparent', emoji: '👴', gender: '' },
                { value: 'Grandchild', label: 'Grandchild', emoji: '👶', gender: '' }
            ],
            extended: [
                { value: 'Uncle', label: 'Uncle', emoji: '👨', gender: 'Male' },
                { value: 'Aunt', label: 'Aunt', emoji: '👩', gender: 'Female' },
                { value: 'Cousin', label: 'Cousin', emoji: '🧑', gender: '' },
                { value: 'Nephew', label: 'Nephew', emoji: '👦', gender: 'Male' },
                { value: 'Niece', label: 'Niece', emoji: '👧', gender: 'Female' },
                { value: 'Saali', label: 'Saali', emoji: '👩', gender: 'Female' }
            ],
            professional: [
                { value: 'Boss', label: 'Boss', emoji: '💼', gender: '' },
                { value: 'Colleague', label: 'Colleague', emoji: '🤝', gender: '' }
            ],
            social: [
                { value: 'Friend', label: 'Friend', emoji: '🧑‍🤝‍🧑', gender: '' },
                { value: 'Boyfriend', label: 'Boyfriend', emoji: '💑', gender: 'Male' },
                { value: 'Girlfriend', label: 'Girlfriend', emoji: '💑', gender: 'Female' }
            ]
        };
        
        const OCCASION_SUGGESTIONS = {
            'Raksha Bandhan': ['Brother', 'Sister'],
            "Valentine's Day": ['Boyfriend', 'Girlfriend', 'Husband', 'Wife'],
            "Mother's Day": ['Mother'],
            "Father's Day": ['Father'],
            'Karva Chauth': ['Husband', 'Wife'],
            'Anniversary': ['Husband', 'Wife', 'Boyfriend', 'Girlfriend']
        };
        
        let selectedCategory = '';
        let selectedOccasion = '';
        let selectedRelationship = '';
        let selectedGender = '';
        
        function selectCategory(element) {
            // Remove previous selection
            document.querySelectorAll('.category-card').forEach(c => c.classList.remove('selected'));
            element.classList.add('selected');
            
            selectedCategory = element.dataset.category;
            
            // Show occasions
            const pillsContainer = document.getElementById('occasionPills');
            const occasions = OCCASION_CATEGORIES[selectedCategory] || [];
            
            pillsContainer.innerHTML = occasions.map(o => 
                `<div class="occasion-pill" data-value="${o.value}" onclick="selectOccasion(this)">${o.label}</div>`
            ).join('');
            
            pillsContainer.style.display = 'flex';
            selectedOccasion = '';
            document.getElementById('step1Next').disabled = true;
        }
        
        function selectOccasion(element) {
            document.querySelectorAll('.occasion-pill').forEach(p => p.classList.remove('selected'));
            element.classList.add('selected');
            
            selectedOccasion = element.dataset.value;
            document.getElementById('occasion').value = selectedOccasion;
            document.getElementById('step1Next').disabled = false;
        }
        
        function populateRelationships() {
            const grid = document.getElementById('relationshipGrid');
            const suggestions = OCCASION_SUGGESTIONS[selectedOccasion] || [];
            
            let html = '';
            const allRelationships = [
                ...RELATIONSHIPS.immediate,
                ...RELATIONSHIPS.extended,
                ...RELATIONSHIPS.professional,
                ...RELATIONSHIPS.social
            ];
            
            // Sort: suggested first
            const sorted = [...allRelationships].sort((a, b) => {
                const aIsSuggested = suggestions.includes(a.value);
                const bIsSuggested = suggestions.includes(b.value);
                if (aIsSuggested && !bIsSuggested) return -1;
                if (!aIsSuggested && bIsSuggested) return 1;
                return 0;
            });
            
            html = sorted.map(r => {
                const isSuggested = suggestions.includes(r.value);
                return `<div class="relationship-card ${isSuggested ? 'suggested' : ''}" 
                            data-value="${r.value}" 
                            data-gender="${r.gender}"
                            onclick="selectRelationship(this)">
                    <span class="emoji">${r.emoji}</span>
                    <span class="name">${r.label}</span>
                </div>`;
            }).join('');
            
            grid.innerHTML = html;
            
            // Update subtitle
            if (suggestions.length > 0) {
                document.getElementById('relationshipSubtitle').innerHTML = 
                    `<span style="color: var(--accent-primary);">★ Suggested for ${selectedOccasion}:</span> ${suggestions.join(', ')}`;
            } else {
                document.getElementById('relationshipSubtitle').textContent = 'Select your relationship with the recipient';
            }
        }
        
        function selectRelationship(element) {
            document.querySelectorAll('.relationship-card').forEach(c => c.classList.remove('selected'));
            element.classList.add('selected');
            
            selectedRelationship = element.dataset.value;
            selectedGender = element.dataset.gender;
            
            document.getElementById('relationship').value = selectedRelationship;
            document.getElementById('gender').value = selectedGender;
            document.getElementById('step2Next').disabled = false;
        }
        
        function updateProgress() {
            for (let i = 1; i <= totalSteps; i++) {
                const dot = document.getElementById(`dot${i}`);
                const line = document.getElementById(`line${i}`);
                
                dot.classList.remove('active', 'completed');
                if (i < currentStep) {
                    dot.classList.add('completed');
                } else if (i === currentStep) {
                    dot.classList.add('active');
                }
                
                if (line) {
                    line.classList.remove('completed');
                    if (i < currentStep) {
                        line.classList.add('completed');
                    }
                }
            }
        }
        
        function showStep(step) {
            document.querySelectorAll('.form-step').forEach(s => s.classList.remove('active'));
            document.getElementById(`step${step}`).classList.add('active');
            updateProgress();
        }
        
        function nextStep() {
            if (currentStep === 1 && !selectedOccasion) return;
            if (currentStep === 2 && !selectedRelationship) return;
            
            if (currentStep === 1) {
                populateRelationships();
            }
            
            if (currentStep < totalSteps) {
                currentStep++;
                showStep(currentStep);
            }
        }
        
        function prevStep() {
            if (currentStep > 1) {
                currentStep--;
                showStep(currentStep);
            }
        }
        
        function getSelectedGiftTypes() {
            const types = [];
            if (document.getElementById('type-formal').checked) types.push('Formal');
            if (document.getElementById('type-funky').checked) types.push('Funky');
            if (document.getElementById('type-romantic').checked) types.push('Romantic');
            if (document.getElementById('type-practical').checked) types.push('Practical');
            if (document.getElementById('type-traditional').checked) types.push('Traditional');
            if (document.getElementById('type-luxury').checked) types.push('Luxury');
            return types.length > 0 ? types : ['Formal', 'Funky', 'Romantic', 'Practical', 'Traditional', 'Luxury'];
        }
        
        // Confetti effect
        function createConfetti() {
            const container = document.getElementById('confetti');
            container.innerHTML = '';
            const colors = ['#0d9488', '#0891b2', '#6366f1', '#8b5cf6', '#ec4899', '#f59e0b'];
            
            for (let i = 0; i < 100; i++) {
                const piece = document.createElement('div');
                piece.className = 'confetti-piece';
                piece.style.left = Math.random() * 100 + '%';
                piece.style.background = colors[Math.floor(Math.random() * colors.length)];
                piece.style.transform = `rotate(${Math.random() * 360}deg)`;
                piece.style.animation = `confettiFall ${2 + Math.random() * 2}s ease-out forwards`;
                piece.style.animationDelay = Math.random() * 0.5 + 's';
                container.appendChild(piece);
            }
            
            setTimeout(() => container.innerHTML = '', 4000);
        }
        
        // Add confetti animation
        const style = document.createElement('style');
        style.textContent = `
            @keyframes confettiFall {
                0% { opacity: 1; transform: translateY(-100vh) rotate(0deg); }
                100% { opacity: 0; transform: translateY(100vh) rotate(720deg); }
            }
        `;
        document.head.appendChild(style);
        
        document.getElementById('giftForm').onsubmit = async (e) => {
            e.preventDefault();
            const data = {
                relationship: document.getElementById('relationship').value,
                occasion: document.getElementById('occasion').value,
                age_group: document.getElementById('ageGroup').value,
                gender: document.getElementById('gender').value,
                vibe: document.getElementById('vibe').value,
                budget: parseInt(document.getElementById('budget').value),
                notes: document.getElementById('notes').value,
                gift_types: getSelectedGiftTypes()
            };
            document.getElementById('formSection').style.display = 'none';
            document.getElementById('loading').style.display = 'block';
            document.getElementById('error').style.display = 'none';
            try {
                const res = await fetch('/api/recommend', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(data)
                });
                if (!res.ok) throw new Error('Failed');
                showResults(await res.json());
                createConfetti();
            } catch (err) {
                document.getElementById('loading').style.display = 'none';
                document.getElementById('formSection').style.display = 'block';
                document.getElementById('error').textContent = 'Something went wrong. Please try again.';
                document.getElementById('error').style.display = 'block';
            }
        };

        function showResults(data) {
            document.getElementById('loading').style.display = 'none';
            document.getElementById('results').style.display = 'block';
            document.getElementById('thinkingText').textContent = data.thinking_trace;
            document.getElementById('proTipText').textContent = data.pro_tip;
            document.getElementById('giftsGrid').innerHTML = data.recommendations.map(g => {
                const tagClass = 'tag-' + (g.gift_type || 'practical').toLowerCase();
                
                let linksHtml = '';
                if (g.purchase_links.amazon) {
                    linksHtml += '<a href="' + g.purchase_links.amazon + '" target="_blank" class="purchase-btn amazon-btn">Amazon</a>';
                }
                if (g.purchase_links.flipkart) {
                    linksHtml += '<a href="' + g.purchase_links.flipkart + '" target="_blank" class="purchase-btn flipkart-btn">Flipkart</a>';
                }
                if (g.purchase_links.myntra) {
                    linksHtml += '<a href="' + g.purchase_links.myntra + '" target="_blank" class="purchase-btn myntra-btn">Myntra</a>';
                }
                if (g.purchase_links.shoppersstop) {
                    linksHtml += '<a href="' + g.purchase_links.shoppersstop + '" target="_blank" class="purchase-btn shoppersstop-btn">Shoppers Stop</a>';
                }
                if (g.purchase_links.blinkit) {
                    linksHtml += '<a href="' + g.purchase_links.blinkit + '" target="_blank" class="purchase-btn blinkit-btn">Blinkit</a>';
                }
                if (g.purchase_links.meesho) {
                    linksHtml += '<a href="' + g.purchase_links.meesho + '" target="_blank" class="purchase-btn meesho-btn">Meesho</a>';
                }
                
                return '<div class="gift-card">' +
                    '<span class="gift-type-tag ' + tagClass + '">' + (g.gift_type || 'Practical') + '</span>' +
                    '<div class="gift-header">' +
                        '<div class="gift-icon">' + g.icon + '</div>' +
                        '<div class="gift-info">' +
                            '<div class="gift-number">' + g.id + '</div>' +
                            '<div class="gift-title">' + g.title + '</div>' +
                        '</div>' +
                    '</div>' +
                    '<div class="gift-description">' + g.description + '</div>' +
                    '<div class="gift-why">' +
                        '<div class="gift-why-label">💡 Why this gift?</div>' +
                        '<div class="gift-why-text">' + g.why_applicable + '</div>' +
                    '</div>' +
                    '<div class="gift-price">' + g.approx_price_inr + '</div>' +
                    '<div class="purchase-links">' + linksHtml + '</div>' +
                '</div>';
            }).join('');
            document.getElementById('results').scrollIntoView({ behavior: 'smooth' });
        }

        function reset() {
            document.getElementById('giftForm').reset();
            document.querySelectorAll('.gift-type-checkbox').forEach(cb => cb.checked = true);
            document.querySelectorAll('.category-card').forEach(c => c.classList.remove('selected'));
            document.querySelectorAll('.occasion-pill').forEach(p => p.classList.remove('selected'));
            document.querySelectorAll('.relationship-card').forEach(c => c.classList.remove('selected'));
            document.getElementById('occasionPills').style.display = 'none';
            document.getElementById('results').style.display = 'none';
            document.getElementById('formSection').style.display = 'block';
            
            selectedCategory = '';
            selectedOccasion = '';
            selectedRelationship = '';
            selectedGender = '';
            currentStep = 1;
            showStep(1);
            
            document.getElementById('step1Next').disabled = true;
            document.getElementById('step2Next').disabled = true;
            
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

        function editRequest() {
            document.getElementById('results').style.display = 'none';
            document.getElementById('formSection').style.display = 'block';
            currentStep = 1;
            showStep(1);
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    </script>
</body>
</html>'''


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Cache-Control', 'no-cache')
        self.end_headers()
        self.wfile.write(HTML_PAGE.encode('utf-8'))

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
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
