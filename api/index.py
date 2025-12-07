"""
Vercel serverless function - GiftingGenie API
All code consolidated to ensure proper bundling
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, Response
from pydantic import BaseModel, Field
from typing import Optional, Dict, List, Any
from urllib.parse import quote_plus
from mangum import Mangum
import random


# ============================================
# GIFTING ENGINE
# ============================================
class GiftingEngine:
    """Core engine for generating culturally-aware gift recommendations"""

    RELATIONSHIP_CONTEXT = {
        "saali": {"formality": "casual", "closeness": "family", "special_note": "brother-in-law relationship"},
        "boss": {"formality": "formal", "closeness": "professional", "special_note": "workplace hierarchy"},
        "mother": {"formality": "casual", "closeness": "immediate_family", "special_note": "most respected"},
        "father": {"formality": "casual", "closeness": "immediate_family", "special_note": "family head"},
        "wife": {"formality": "casual", "closeness": "immediate_family", "special_note": "life partner"},
        "husband": {"formality": "casual", "closeness": "immediate_family", "special_note": "life partner"},
        "brother": {"formality": "casual", "closeness": "immediate_family", "special_note": "sibling bond"},
        "sister": {"formality": "casual", "closeness": "immediate_family", "special_note": "sibling bond"},
        "son": {"formality": "casual", "closeness": "immediate_family", "special_note": "parent-child"},
        "daughter": {"formality": "casual", "closeness": "immediate_family", "special_note": "parent-child"},
        "uncle": {"formality": "casual", "closeness": "extended_family", "special_note": "parental generation"},
        "aunt": {"formality": "casual", "closeness": "extended_family", "special_note": "parental generation"},
        "cousin": {"formality": "casual", "closeness": "extended_family", "special_note": "peer generation"},
        "nephew": {"formality": "casual", "closeness": "extended_family", "special_note": "next generation"},
        "niece": {"formality": "casual", "closeness": "extended_family", "special_note": "next generation"},
        "friend": {"formality": "casual", "closeness": "social", "special_note": "peer relationship"},
        "colleague": {"formality": "semi-formal", "closeness": "professional", "special_note": "work peer"},
        "boyfriend": {"formality": "casual", "closeness": "romantic", "special_note": "romantic partner"},
        "girlfriend": {"formality": "casual", "closeness": "romantic", "special_note": "romantic partner"},
        "grandparent": {"formality": "casual", "closeness": "immediate_family", "special_note": "elder respect"},
        "grandchild": {"formality": "casual", "closeness": "immediate_family", "special_note": "youngest generation"},
    }

    OCCASION_CONTEXT = {
        "diwali": {"type": "festival", "cultural_significance": "very_high", "theme": "prosperity"},
        "holi": {"type": "festival", "cultural_significance": "high", "theme": "colors and joy"},
        "raksha bandhan": {"type": "festival", "cultural_significance": "high", "theme": "sibling bond"},
        "durga puja": {"type": "festival", "cultural_significance": "very_high", "theme": "divine blessings"},
        "ganesh chaturthi": {"type": "festival", "cultural_significance": "very_high", "theme": "new beginnings"},
        "navratri": {"type": "festival", "cultural_significance": "very_high", "theme": "devotion"},
        "janmashtami": {"type": "festival", "cultural_significance": "high", "theme": "celebration"},
        "eid": {"type": "festival", "cultural_significance": "very_high", "theme": "togetherness"},
        "christmas": {"type": "festival", "cultural_significance": "high", "theme": "joy and giving"},
        "pongal": {"type": "festival", "cultural_significance": "high", "theme": "harvest celebration"},
        "onam": {"type": "festival", "cultural_significance": "high", "theme": "harvest prosperity"},
        "baisakhi": {"type": "festival", "cultural_significance": "high", "theme": "harvest festival"},
        "new year": {"type": "celebration", "cultural_significance": "high", "theme": "new beginnings"},
        "diwali new year": {"type": "festival", "cultural_significance": "very_high", "theme": "fresh start"},
        "puja": {"type": "religious", "cultural_significance": "high", "theme": "spiritual"},
        "temple visit": {"type": "religious", "cultural_significance": "medium", "theme": "devotion"},
        "wedding": {"type": "milestone", "cultural_significance": "very_high", "theme": "new beginnings"},
        "anniversary": {"type": "milestone", "cultural_significance": "high", "theme": "togetherness"},
        "birthday": {"type": "celebration", "cultural_significance": "medium", "theme": "personal"},
        "graduation": {"type": "milestone", "cultural_significance": "high", "theme": "achievement"},
        "promotion": {"type": "milestone", "cultural_significance": "medium", "theme": "career growth"},
        "baby shower": {"type": "milestone", "cultural_significance": "high", "theme": "new life"},
        "house warming": {"type": "milestone", "cultural_significance": "high", "theme": "new home"},
        "retirement": {"type": "milestone", "cultural_significance": "high", "theme": "new chapter"},
        "valentine's day": {"type": "celebration", "cultural_significance": "medium", "theme": "romance"},
        "karva chauth": {"type": "festival", "cultural_significance": "high", "theme": "marital bond"},
        "mother's day": {"type": "celebration", "cultural_significance": "medium", "theme": "maternal love"},
        "father's day": {"type": "celebration", "cultural_significance": "medium", "theme": "paternal love"},
    }

    GIFT_DATABASE = {
        "traditional": [
            "Silver Pooja Items", "Brass Diya Set", "Traditional Silk Saree",
            "Kurta Pajama Set", "Handcrafted Jewelry", "Traditional Art Painting",
            "Silver Coins", "Copper Water Bottle", "Traditional Sweet Box"
        ],
        "modern": [
            "Smart Watch", "Bluetooth Speaker", "Power Bank", "Wireless Earbuds",
            "Coffee Maker", "Air Purifier", "Electric Kettle", "Grooming Kit"
        ],
        "personalized": [
            "Customized Photo Frame", "Engraved Pen Set", "Personalized Cushion",
            "Custom Name Plate", "Photo Coffee Mug", "Customized Diary"
        ],
        "luxury": [
            "Designer Perfume", "Premium Watch", "Leather Wallet", "Designer Sunglasses",
            "Branded Handbag", "Premium Tea/Coffee Gift Set", "Luxury Chocolate Box"
        ],
        "wellness": [
            "Yoga Mat", "Essential Oil Diffuser", "Spa Gift Hamper", "Fitness Tracker",
            "Organic Skincare Set", "Meditation Kit", "Healthy Snack Box"
        ],
        "tech": [
            "Tablet", "Kindle E-reader", "Smart Home Device", "Gaming Accessories",
            "Portable Projector", "Action Camera", "Drone"
        ],
        "festive": [
            "Decorative Diya Set", "Rangoli Kit", "Festival Sweet Hamper",
            "Decorative Toran", "Festive Dry Fruit Box", "Pooja Thali Set"
        ],
        "romantic": [
            "Couple Watches", "Heart-shaped Jewelry", "Romantic Dinner Voucher",
            "Perfume Gift Set", "Couple Keychains", "Love Letter Kit"
        ],
        "kids": [
            "Educational Toys", "Building Blocks Set", "Art and Craft Kit",
            "Remote Control Car", "Story Books Set", "Kids Smartwatch"
        ],
        "home": [
            "Wall Clock", "Decorative Showpiece", "Table Lamp", "Bedsheet Set",
            "Dinner Set", "Kitchen Appliance", "Indoor Plant with Planter"
        ]
    }

    def __init__(self):
        pass

    def analyze_context(self, relationship: str, occasion: str, age_group: str,
                       vibe: str, budget: int) -> Dict[str, Any]:
        relationship_lower = relationship.lower()
        occasion_lower = occasion.lower()
        context = {
            "relationship_type": self.RELATIONSHIP_CONTEXT.get(relationship_lower, {
                "formality": "casual", "closeness": "general", "special_note": "general relationship"
            }),
            "occasion_type": self.OCCASION_CONTEXT.get(occasion_lower, {
                "type": "celebration", "cultural_significance": "medium", "theme": "general"
            }),
            "budget_range": budget,
            "age_group": age_group,
            "vibe": vibe
        }
        return context

    def select_gift_categories(self, context: Dict[str, Any]) -> List[str]:
        categories = []
        occasion_theme = context["occasion_type"]["theme"]
        if "festival" in context["occasion_type"]["type"]:
            categories.extend(["traditional", "festive"])
        elif occasion_theme == "romance":
            categories.extend(["romantic", "personalized"])
        elif occasion_theme == "new beginnings":
            categories.extend(["traditional", "home"])

        if context["relationship_type"]["closeness"] == "immediate_family":
            categories.extend(["personalized", "luxury", "wellness"])
        elif context["relationship_type"]["closeness"] == "professional":
            categories.extend(["modern", "luxury"])
        elif context["relationship_type"]["closeness"] == "romantic":
            categories.extend(["romantic", "personalized"])

        vibe_lower = context["vibe"].lower()
        if "traditional" in vibe_lower or "ethnic" in vibe_lower:
            categories.append("traditional")
        if "modern" in vibe_lower or "tech" in vibe_lower:
            categories.extend(["modern", "tech"])
        if "personal" in vibe_lower:
            categories.append("personalized")

        if len(categories) < 3:
            categories.extend(["modern", "personalized", "home"])

        return list(set(categories))[:5]

    def generate_gift_item(self, category: str, context: Dict[str, Any],
                          used_items: set) -> Dict[str, Any]:
        available_items = [item for item in self.GIFT_DATABASE.get(category, [])
                          if item not in used_items]

        if not available_items:
            all_items = []
            for cat_items in self.GIFT_DATABASE.values():
                all_items.extend([item for item in cat_items if item not in used_items])
            available_items = all_items

        if not available_items:
            return None

        random.seed(hash(str(context)) + len(used_items))
        item = random.choice(available_items)
        used_items.add(item)

        budget = context["budget_range"]
        base_price = int(budget * random.uniform(0.7, 1.1))
        rounded_price = round(base_price / 50) * 50

        return {
            "item": item,
            "category": category,
            "price": rounded_price
        }

    def create_search_url(self, item_name: str, platform: str) -> str:
        encoded_search = quote_plus(item_name)
        if platform == "amazon":
            return f"https://www.amazon.in/s?k={encoded_search}"
        elif platform == "flipkart":
            return f"https://www.flipkart.com/search?q={encoded_search}"
        return ""

    def generate_description(self, item: str, relationship: str, occasion: str) -> str:
        templates = [
            f"Perfect for {relationship} on {occasion}, combines thoughtfulness with utility",
            f"Culturally appropriate choice that honors the {occasion} celebration tradition",
            f"Shows respect and affection, ideal for {relationship} relationship",
            f"Meaningful gift that celebrates {occasion} with traditional values",
            f"Thoughtful present that strengthens {relationship} bond on {occasion}"
        ]
        random.seed(hash(item + relationship + occasion))
        return random.choice(templates)

    def generate_pro_tip(self, occasion: str, relationship: str) -> str:
        occasion_lower = occasion.lower()
        relationship_lower = relationship.lower()
        tips = {
            "diwali": "Always include a handwritten card with Diwali wishes. Avoid black colored gifts.",
            "raksha bandhan": "Present the gift after the rakhi ceremony. Include sweets for tradition.",
            "wedding": "Gifts in odd numbers are considered auspicious. Include shagun envelope.",
            "birthday": "Personalized gifts show extra thought. Consider their hobbies and interests.",
            "anniversary": "Gifts symbolizing togetherness work best. Avoid sharp objects like knives.",
        }
        for key, tip in tips.items():
            if key in occasion_lower:
                return tip
        if "boss" in relationship_lower or "colleague" in relationship_lower:
            return "Keep professional gifts neutral and practical. Avoid overly personal items."
        return "Present with both hands as a sign of respect. Include a personalized message."

    def generate_recommendations(self, relationship: str, occasion: str,
                                age_group: str, vibe: str, budget: int) -> Dict[str, Any]:
        context = self.analyze_context(relationship, occasion, age_group, vibe, budget)
        thinking_trace = (
            f"Analyzing gift for {relationship} on {occasion}. "
            f"Considering {context['relationship_type']['formality']} formality, "
            f"{context['occasion_type']['cultural_significance']} cultural significance, "
            f"and Rs.{budget} budget. Selecting from traditional and modern categories."
        )
        categories = self.select_gift_categories(context)
        recommendations = []
        used_items = set()

        for i in range(5):
            category = categories[i % len(categories)]
            gift_item = self.generate_gift_item(category, context, used_items)
            if not gift_item:
                continue
            recommendation = {
                "id": i + 1,
                "title": gift_item["item"],
                "description": self.generate_description(
                    gift_item["item"], relationship, occasion
                ),
                "approx_price_inr": f"Rs.{gift_item['price']:,}",
                "purchase_links": {
                    "amazon_in": self.create_search_url(gift_item["item"], "amazon"),
                    "flipkart": self.create_search_url(gift_item["item"], "flipkart")
                }
            }
            recommendations.append(recommendation)

        pro_tip = self.generate_pro_tip(occasion, relationship)
        return {
            "thinking_trace": thinking_trace,
            "recommendations": recommendations,
            "pro_tip": pro_tip
        }


# ============================================
# FASTAPI APP
# ============================================
app = FastAPI(
    title="GiftingGenie API",
    description="Expert Indian Personal Shopper & Gifting Concierge",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

gifting_engine = GiftingEngine()


class GiftRequest(BaseModel):
    relationship: str = Field(..., description="Relationship type", example="Saali")
    occasion: str = Field(..., description="Occasion", example="Raksha Bandhan")
    age_group: Optional[str] = Field("Adult", description="Age group")
    vibe: Optional[str] = Field("Traditional", description="Gift vibe/style")
    budget: int = Field(..., description="Budget in INR", ge=100, le=1000000)


# HTML Template embedded directly
HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GiftingGenie - Your Personal Gifting Concierge</title>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🎁</text></svg>">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Poppins', sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; color: #333; }
        .container { max-width: 1400px; margin: 0 auto; }
        .header { text-align: center; color: white; margin-bottom: 40px; animation: fadeInDown 0.8s ease-out; }
        .header h1 { font-size: 3.5rem; font-weight: 700; margin-bottom: 10px; text-shadow: 2px 2px 4px rgba(0,0,0,0.2); }
        .header .subtitle { font-size: 1.3rem; font-weight: 300; opacity: 0.95; }
        .header .emoji { font-size: 4rem; display: inline-block; animation: bounce 2s infinite; }
        .main-card { background: white; border-radius: 30px; padding: 50px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); animation: fadeInUp 0.8s ease-out; }
        .form-section { margin-bottom: 40px; }
        .form-title { font-size: 2rem; color: #667eea; margin-bottom: 30px; text-align: center; font-weight: 600; }
        .form-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 25px; margin-bottom: 30px; }
        .form-group { display: flex; flex-direction: column; }
        .form-group label { font-weight: 600; margin-bottom: 8px; color: #555; font-size: 0.95rem; }
        .form-group input, .form-group select { padding: 14px 18px; border: 2px solid #e0e0e0; border-radius: 12px; font-size: 1rem; font-family: 'Poppins', sans-serif; transition: all 0.3s ease; background: #f8f9fa; }
        .form-group input:focus, .form-group select:focus { outline: none; border-color: #667eea; background: white; box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1); }
        .budget-input { position: relative; }
        .budget-input input { padding-left: 35px; }
        .budget-input::before { content: 'Rs.'; position: absolute; left: 12px; top: 50%; transform: translateY(-50%); font-weight: 600; color: #667eea; font-size: 0.9rem; }
        .submit-btn { width: 100%; padding: 18px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 12px; font-size: 1.2rem; font-weight: 600; cursor: pointer; transition: all 0.3s ease; box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4); }
        .submit-btn:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6); }
        .submit-btn:disabled { opacity: 0.6; cursor: not-allowed; }
        .loading { display: none; text-align: center; padding: 40px; }
        .spinner { border: 4px solid #f3f3f3; border-top: 4px solid #667eea; border-radius: 50%; width: 50px; height: 50px; animation: spin 1s linear infinite; margin: 0 auto 20px; }
        .results-section { display: none; margin-top: 50px; }
        .results-header { text-align: center; margin-bottom: 30px; }
        .results-header h2 { font-size: 2.5rem; color: #667eea; margin-bottom: 10px; }
        .thinking-trace { background: #f8f9fa; padding: 20px; border-radius: 12px; margin-bottom: 30px; border-left: 4px solid #667eea; }
        .thinking-trace h3 { color: #667eea; font-size: 1.1rem; margin-bottom: 10px; }
        .thinking-trace p { color: #666; line-height: 1.6; }
        .gifts-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 25px; margin-bottom: 30px; }
        .gift-card { background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%); border-radius: 20px; padding: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); transition: all 0.3s ease; border: 2px solid transparent; }
        .gift-card:hover { transform: translateY(-5px); box-shadow: 0 15px 40px rgba(102, 126, 234, 0.2); border-color: #667eea; }
        .gift-number { display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; width: 35px; height: 35px; border-radius: 50%; text-align: center; line-height: 35px; font-weight: 600; margin-bottom: 15px; }
        .gift-title { font-size: 1.4rem; color: #333; margin-bottom: 12px; font-weight: 600; }
        .gift-description { color: #666; margin-bottom: 15px; line-height: 1.6; font-size: 0.95rem; }
        .gift-price { font-size: 1.8rem; color: #667eea; font-weight: 700; margin-bottom: 20px; }
        .purchase-links { display: flex; gap: 12px; }
        .purchase-btn { flex: 1; padding: 12px; border-radius: 10px; text-decoration: none; text-align: center; font-weight: 600; transition: all 0.3s ease; font-size: 0.9rem; }
        .amazon-btn { background: #FF9900; color: white; }
        .amazon-btn:hover { background: #e88b00; transform: scale(1.05); }
        .flipkart-btn { background: #2874F0; color: white; }
        .flipkart-btn:hover { background: #1d5fc7; transform: scale(1.05); }
        .pro-tip { background: linear-gradient(135deg, #ffd89b 0%, #19547b 100%); color: white; padding: 25px; border-radius: 15px; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }
        .pro-tip h3 { font-size: 1.3rem; margin-bottom: 10px; }
        .pro-tip p { font-size: 1.05rem; line-height: 1.6; }
        @keyframes fadeInDown { from { opacity: 0; transform: translateY(-30px); } to { opacity: 1; transform: translateY(0); } }
        @keyframes fadeInUp { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: translateY(0); } }
        @keyframes bounce { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-10px); } }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        @media (max-width: 768px) { .header h1 { font-size: 2.5rem; } .header .subtitle { font-size: 1.1rem; } .main-card { padding: 30px 20px; } .form-grid { grid-template-columns: 1fr; } .gifts-grid { grid-template-columns: 1fr; } .purchase-links { flex-direction: column; } }
        .error-message { background: #ff4444; color: white; padding: 15px; border-radius: 10px; margin-top: 20px; display: none; }
        .back-btn { display: block; padding: 12px 30px; background: white; color: #667eea; border: 2px solid #667eea; border-radius: 10px; text-decoration: none; font-weight: 600; margin: 30px auto; width: fit-content; cursor: pointer; transition: all 0.3s ease; }
        .back-btn:hover { background: #667eea; color: white; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="emoji">🎁</div>
            <h1>GiftingGenie</h1>
            <p class="subtitle">Your Personal Indian Gifting Concierge - Find the Perfect Gift in Seconds</p>
        </div>
        <div class="main-card">
            <div class="form-section" id="formSection">
                <h2 class="form-title">Tell Us About Your Gift Recipient</h2>
                <form id="giftForm">
                    <div class="form-grid">
                        <div class="form-group">
                            <label for="relationship">Relationship</label>
                            <select id="relationship" required>
                                <option value="">Select Relationship</option>
                                <optgroup label="Immediate Family">
                                    <option value="Mother">Mother</option>
                                    <option value="Father">Father</option>
                                    <option value="Brother">Brother</option>
                                    <option value="Sister">Sister</option>
                                    <option value="Wife">Wife</option>
                                    <option value="Husband">Husband</option>
                                    <option value="Son">Son</option>
                                    <option value="Daughter">Daughter</option>
                                    <option value="Grandparent">Grandparent</option>
                                    <option value="Grandchild">Grandchild</option>
                                </optgroup>
                                <optgroup label="Extended Family">
                                    <option value="Uncle">Uncle</option>
                                    <option value="Aunt">Aunt</option>
                                    <option value="Cousin">Cousin</option>
                                    <option value="Nephew">Nephew</option>
                                    <option value="Niece">Niece</option>
                                    <option value="Saali">Saali (Sister-in-law)</option>
                                </optgroup>
                                <optgroup label="Professional">
                                    <option value="Boss">Boss</option>
                                    <option value="Colleague">Colleague</option>
                                </optgroup>
                                <optgroup label="Social & Romantic">
                                    <option value="Friend">Friend</option>
                                    <option value="Boyfriend">Boyfriend</option>
                                    <option value="Girlfriend">Girlfriend</option>
                                </optgroup>
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="occasion">Occasion</label>
                            <select id="occasion" required>
                                <option value="">Select Occasion</option>
                                <optgroup label="Major Festivals">
                                    <option value="Diwali">Diwali</option>
                                    <option value="Holi">Holi</option>
                                    <option value="Raksha Bandhan">Raksha Bandhan</option>
                                    <option value="Durga Puja">Durga Puja</option>
                                    <option value="Ganesh Chaturthi">Ganesh Chaturthi</option>
                                    <option value="Navratri">Navratri</option>
                                    <option value="Janmashtami">Janmashtami</option>
                                    <option value="Eid">Eid</option>
                                    <option value="Christmas">Christmas</option>
                                    <option value="Pongal">Pongal</option>
                                    <option value="Onam">Onam</option>
                                    <option value="Baisakhi">Baisakhi</option>
                                    <option value="Karva Chauth">Karva Chauth</option>
                                </optgroup>
                                <optgroup label="New Year & Religious">
                                    <option value="New Year">New Year</option>
                                    <option value="Diwali New Year">Diwali New Year</option>
                                    <option value="Puja">Puja</option>
                                    <option value="Temple Visit">Temple Visit</option>
                                </optgroup>
                                <optgroup label="Life Milestones">
                                    <option value="Birthday">Birthday</option>
                                    <option value="Anniversary">Anniversary</option>
                                    <option value="Wedding">Wedding</option>
                                    <option value="Graduation">Graduation</option>
                                    <option value="Promotion">Promotion</option>
                                    <option value="Baby Shower">Baby Shower</option>
                                    <option value="House Warming">House Warming</option>
                                    <option value="Retirement">Retirement</option>
                                </optgroup>
                                <optgroup label="Other Occasions">
                                    <option value="Valentine's Day">Valentine's Day</option>
                                    <option value="Mother's Day">Mother's Day</option>
                                    <option value="Father's Day">Father's Day</option>
                                </optgroup>
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="ageGroup">Age Group</label>
                            <select id="ageGroup" required>
                                <option value="">Select Age Group</option>
                                <option value="Child">Child (0-12)</option>
                                <option value="Teenager">Teenager (13-19)</option>
                                <option value="Adult">Adult (20-59)</option>
                                <option value="Senior">Senior (60+)</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="vibe">Vibe/Style</label>
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
                        <div class="form-group budget-input">
                            <label for="budget">Budget (INR)</label>
                            <input type="number" id="budget" placeholder="2000" min="100" max="1000000" required>
                        </div>
                    </div>
                    <button type="submit" class="submit-btn" id="submitBtn">Find Perfect Gifts</button>
                </form>
                <div class="error-message" id="errorMessage"></div>
            </div>
            <div class="loading" id="loadingSection">
                <div class="spinner"></div>
                <p style="color: #667eea; font-size: 1.2rem; font-weight: 600;">Finding the perfect gifts for you...</p>
            </div>
            <div class="results-section" id="resultsSection">
                <div class="results-header"><h2>Your Perfect Gift Ideas</h2></div>
                <div class="thinking-trace" id="thinkingTrace">
                    <h3>Our Recommendation Logic</h3>
                    <p id="thinkingText"></p>
                </div>
                <div class="gifts-grid" id="giftsGrid"></div>
                <div class="pro-tip" id="proTip">
                    <h3>Pro Tip</h3>
                    <p id="proTipText"></p>
                </div>
                <button class="back-btn" onclick="resetForm()">Find More Gifts</button>
            </div>
        </div>
    </div>
    <script>
        const API_URL = '/api/v1/recommend';
        document.getElementById('giftForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = {
                relationship: document.getElementById('relationship').value,
                occasion: document.getElementById('occasion').value,
                age_group: document.getElementById('ageGroup').value,
                vibe: document.getElementById('vibe').value,
                budget: parseInt(document.getElementById('budget').value)
            };
            document.getElementById('formSection').style.display = 'none';
            document.getElementById('loadingSection').style.display = 'block';
            document.getElementById('errorMessage').style.display = 'none';
            try {
                const response = await fetch(API_URL, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(formData)
                });
                if (!response.ok) throw new Error('Failed to fetch recommendations');
                const data = await response.json();
                displayResults(data);
            } catch (error) {
                console.error('Error:', error);
                document.getElementById('loadingSection').style.display = 'none';
                document.getElementById('formSection').style.display = 'block';
                const errorMsg = document.getElementById('errorMessage');
                errorMsg.textContent = 'Oops! Something went wrong. Please try again.';
                errorMsg.style.display = 'block';
            }
        });
        function displayResults(data) {
            document.getElementById('loadingSection').style.display = 'none';
            document.getElementById('resultsSection').style.display = 'block';
            document.getElementById('thinkingText').textContent = data.thinking_trace;
            const giftsGrid = document.getElementById('giftsGrid');
            giftsGrid.innerHTML = '';
            data.recommendations.forEach((gift, index) => {
                const giftCard = document.createElement('div');
                giftCard.className = 'gift-card';
                giftCard.innerHTML = '<div class="gift-number">' + gift.id + '</div><h3 class="gift-title">' + gift.title + '</h3><p class="gift-description">' + gift.description + '</p><div class="gift-price">' + gift.approx_price_inr + '</div><div class="purchase-links"><a href="' + gift.purchase_links.amazon_in + '" target="_blank" class="purchase-btn amazon-btn">Amazon</a><a href="' + gift.purchase_links.flipkart + '" target="_blank" class="purchase-btn flipkart-btn">Flipkart</a></div>';
                giftsGrid.appendChild(giftCard);
            });
            document.getElementById('proTipText').textContent = data.pro_tip;
            setTimeout(() => { document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth', block: 'start' }); }, 100);
        }
        function resetForm() {
            document.getElementById('giftForm').reset();
            document.getElementById('resultsSection').style.display = 'none';
            document.getElementById('formSection').style.display = 'block';
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    </script>
</body>
</html>'''


@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main landing page"""
    return HTML_TEMPLATE


@app.get("/favicon.ico")
async def favicon():
    """Serve favicon"""
    svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><text y=".9em" font-size="90">🎁</text></svg>"""
    return Response(content=svg_content, media_type="image/svg+xml")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.post("/api/v1/recommend")
async def recommend_gifts(request: GiftRequest):
    """Generate gift recommendations"""
    try:
        recommendations = gifting_engine.generate_recommendations(
            relationship=request.relationship,
            occasion=request.occasion,
            age_group=request.age_group or "Adult",
            vibe=request.vibe or "Traditional",
            budget=request.budget
        )
        return recommendations
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating recommendations: {str(e)}")


@app.get("/api/v1/occasions")
async def list_occasions():
    """List all supported occasions"""
    return {"occasions": list(gifting_engine.OCCASION_CONTEXT.keys())}


@app.get("/api/v1/relationships")
async def list_relationships():
    """List all supported relationship types"""
    return {"relationships": list(gifting_engine.RELATIONSHIP_CONTEXT.keys())}


# Vercel serverless handler
handler = Mangum(app, lifespan="off")
