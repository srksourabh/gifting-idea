"""
GiftingGenie Recommendation Engine
Handles gift recommendations based on Indian cultural context
"""
from urllib.parse import quote_plus
from typing import Dict, List, Any


class GiftingEngine:
    """Core engine for generating culturally-aware gift recommendations"""

    # Indian cultural context mappings
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
        # Major Indian Festivals
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

        # New Year Celebrations
        "new year": {"type": "celebration", "cultural_significance": "high", "theme": "new beginnings"},
        "diwali new year": {"type": "festival", "cultural_significance": "very_high", "theme": "fresh start"},

        # Religious Occasions
        "puja": {"type": "religious", "cultural_significance": "high", "theme": "spiritual"},
        "temple visit": {"type": "religious", "cultural_significance": "medium", "theme": "devotion"},

        # Milestones
        "wedding": {"type": "milestone", "cultural_significance": "very_high", "theme": "new beginnings"},
        "anniversary": {"type": "milestone", "cultural_significance": "high", "theme": "togetherness"},
        "birthday": {"type": "celebration", "cultural_significance": "medium", "theme": "personal"},
        "graduation": {"type": "milestone", "cultural_significance": "high", "theme": "achievement"},
        "promotion": {"type": "milestone", "cultural_significance": "medium", "theme": "career growth"},
        "baby shower": {"type": "milestone", "cultural_significance": "high", "theme": "new life"},
        "house warming": {"type": "milestone", "cultural_significance": "high", "theme": "new home"},
        "retirement": {"type": "milestone", "cultural_significance": "high", "theme": "new chapter"},

        # Other Celebrations
        "valentine's day": {"type": "celebration", "cultural_significance": "medium", "theme": "romance"},
        "karva chauth": {"type": "festival", "cultural_significance": "high", "theme": "marital bond"},
        "mother's day": {"type": "celebration", "cultural_significance": "medium", "theme": "maternal love"},
        "father's day": {"type": "celebration", "cultural_significance": "medium", "theme": "paternal love"},
    }

    # Gift categories with Indian context
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
        """Initialize the gifting engine"""
        pass

    def analyze_context(self, relationship: str, occasion: str, age_group: str,
                       vibe: str, budget: int) -> Dict[str, Any]:
        """Analyze the cultural and contextual requirements"""
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
        """Select appropriate gift categories based on context"""
        categories = []

        # Based on occasion
        occasion_theme = context["occasion_type"]["theme"]
        if "festival" in context["occasion_type"]["type"]:
            categories.extend(["traditional", "festive"])
        elif occasion_theme == "romance":
            categories.extend(["romantic", "personalized"])
        elif occasion_theme == "new beginnings":
            categories.extend(["traditional", "home"])

        # Based on relationship
        if context["relationship_type"]["closeness"] == "immediate_family":
            categories.extend(["personalized", "luxury", "wellness"])
        elif context["relationship_type"]["closeness"] == "professional":
            categories.extend(["modern", "luxury"])
        elif context["relationship_type"]["closeness"] == "romantic":
            categories.extend(["romantic", "personalized"])

        # Based on vibe
        vibe_lower = context["vibe"].lower()
        if "traditional" in vibe_lower or "ethnic" in vibe_lower:
            categories.append("traditional")
        if "modern" in vibe_lower or "tech" in vibe_lower:
            categories.extend(["modern", "tech"])
        if "personal" in vibe_lower:
            categories.append("personalized")

        # Ensure we have enough categories
        if len(categories) < 3:
            categories.extend(["modern", "personalized", "home"])

        return list(set(categories))[:5]  # Return unique categories

    def generate_gift_item(self, category: str, context: Dict[str, Any],
                          used_items: set) -> Dict[str, Any]:
        """Generate a single gift recommendation"""
        available_items = [item for item in self.GIFT_DATABASE.get(category, [])
                          if item not in used_items]

        if not available_items:
            # Fallback to any category if current is exhausted
            all_items = []
            for cat_items in self.GIFT_DATABASE.values():
                all_items.extend([item for item in cat_items if item not in used_items])
            available_items = all_items

        if not available_items:
            return None

        import random
        random.seed(hash(str(context)) + len(used_items))
        item = random.choice(available_items)
        used_items.add(item)

        # Generate price within budget
        budget = context["budget_range"]
        base_price = int(budget * random.uniform(0.7, 1.1))
        rounded_price = round(base_price / 50) * 50  # Round to nearest 50

        return {
            "item": item,
            "category": category,
            "price": rounded_price
        }

    def create_search_url(self, item_name: str, platform: str) -> str:
        """Create properly encoded search URL for e-commerce platforms"""
        encoded_search = quote_plus(item_name)

        if platform == "amazon":
            return f"https://www.amazon.in/s?k={encoded_search}"
        elif platform == "flipkart":
            return f"https://www.flipkart.com/search?q={encoded_search}"

        return ""

    def generate_description(self, item: str, relationship: str, occasion: str) -> str:
        """Generate culturally appropriate description"""
        templates = [
            f"Perfect for {relationship} on {occasion}, combines thoughtfulness with utility",
            f"Culturally appropriate choice that honors the {occasion} celebration tradition",
            f"Shows respect and affection, ideal for {relationship} relationship",
            f"Meaningful gift that celebrates {occasion} with traditional values",
            f"Thoughtful present that strengthens {relationship} bond on {occasion}"
        ]

        import random
        random.seed(hash(item + relationship + occasion))
        return random.choice(templates)

    def generate_pro_tip(self, occasion: str, relationship: str) -> str:
        """Generate a helpful pro tip"""
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
        """Main method to generate 5 gift recommendations"""

        # Analyze context
        context = self.analyze_context(relationship, occasion, age_group, vibe, budget)

        # Generate thinking trace
        thinking_trace = (
            f"Analyzing gift for {relationship} on {occasion}. "
            f"Considering {context['relationship_type']['formality']} formality, "
            f"{context['occasion_type']['cultural_significance']} cultural significance, "
            f"and ₹{budget} budget. Selecting from traditional and modern categories."
        )

        # Select categories
        categories = self.select_gift_categories(context)

        # Generate 5 recommendations
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
                "approx_price_inr": f"₹{gift_item['price']:,}",
                "purchase_links": {
                    "amazon_in": self.create_search_url(gift_item["item"], "amazon"),
                    "flipkart": self.create_search_url(gift_item["item"], "flipkart")
                }
            }
            recommendations.append(recommendation)

        # Generate pro tip
        pro_tip = self.generate_pro_tip(occasion, relationship)

        return {
            "thinking_trace": thinking_trace,
            "recommendations": recommendations,
            "pro_tip": pro_tip
        }
