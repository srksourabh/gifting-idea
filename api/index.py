"""
GiftingGenie API - Vercel Serverless Function
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, Response
from pydantic import BaseModel, Field
from typing import Optional, Dict, List, Any
from urllib.parse import quote_plus
from mangum import Mangum
import random

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


class GiftRequest(BaseModel):
    relationship: str = Field(..., description="Relationship type")
    occasion: str = Field(..., description="Occasion")
    age_group: Optional[str] = Field("Adult", description="Age group")
    vibe: Optional[str] = Field("Traditional", description="Gift vibe/style")
    budget: int = Field(..., description="Budget in INR", ge=100, le=1000000)


RELATIONSHIP_CONTEXT = {
    "saali": {"formality": "casual", "closeness": "family"},
    "boss": {"formality": "formal", "closeness": "professional"},
    "mother": {"formality": "casual", "closeness": "immediate_family"},
    "father": {"formality": "casual", "closeness": "immediate_family"},
    "wife": {"formality": "casual", "closeness": "immediate_family"},
    "husband": {"formality": "casual", "closeness": "immediate_family"},
    "brother": {"formality": "casual", "closeness": "immediate_family"},
    "sister": {"formality": "casual", "closeness": "immediate_family"},
    "son": {"formality": "casual", "closeness": "immediate_family"},
    "daughter": {"formality": "casual", "closeness": "immediate_family"},
    "uncle": {"formality": "casual", "closeness": "extended_family"},
    "aunt": {"formality": "casual", "closeness": "extended_family"},
    "cousin": {"formality": "casual", "closeness": "extended_family"},
    "nephew": {"formality": "casual", "closeness": "extended_family"},
    "niece": {"formality": "casual", "closeness": "extended_family"},
    "friend": {"formality": "casual", "closeness": "social"},
    "colleague": {"formality": "semi-formal", "closeness": "professional"},
    "boyfriend": {"formality": "casual", "closeness": "romantic"},
    "girlfriend": {"formality": "casual", "closeness": "romantic"},
    "grandparent": {"formality": "casual", "closeness": "immediate_family"},
    "grandchild": {"formality": "casual", "closeness": "immediate_family"},
}

OCCASION_CONTEXT = {
    "diwali": {"type": "festival", "significance": "very_high"},
    "holi": {"type": "festival", "significance": "high"},
    "raksha bandhan": {"type": "festival", "significance": "high"},
    "durga puja": {"type": "festival", "significance": "very_high"},
    "ganesh chaturthi": {"type": "festival", "significance": "very_high"},
    "navratri": {"type": "festival", "significance": "very_high"},
    "janmashtami": {"type": "festival", "significance": "high"},
    "eid": {"type": "festival", "significance": "very_high"},
    "christmas": {"type": "festival", "significance": "high"},
    "pongal": {"type": "festival", "significance": "high"},
    "onam": {"type": "festival", "significance": "high"},
    "baisakhi": {"type": "festival", "significance": "high"},
    "new year": {"type": "celebration", "significance": "high"},
    "wedding": {"type": "milestone", "significance": "very_high"},
    "anniversary": {"type": "milestone", "significance": "high"},
    "birthday": {"type": "celebration", "significance": "medium"},
    "graduation": {"type": "milestone", "significance": "high"},
    "promotion": {"type": "milestone", "significance": "medium"},
    "baby shower": {"type": "milestone", "significance": "high"},
    "house warming": {"type": "milestone", "significance": "high"},
    "retirement": {"type": "milestone", "significance": "high"},
    "valentine's day": {"type": "celebration", "significance": "medium"},
    "karva chauth": {"type": "festival", "significance": "high"},
    "mother's day": {"type": "celebration", "significance": "medium"},
    "father's day": {"type": "celebration", "significance": "medium"},
}

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


def get_recommendations(relationship, occasion, age_group, vibe, budget):
    rel_ctx = RELATIONSHIP_CONTEXT.get(relationship.lower(), {"formality": "casual", "closeness": "general"})
    occ_ctx = OCCASION_CONTEXT.get(occasion.lower(), {"type": "celebration", "significance": "medium"})

    categories = ["traditional", "modern", "personalized"]
    if rel_ctx["closeness"] == "immediate_family":
        categories = ["personalized", "luxury", "wellness"]
    elif rel_ctx["closeness"] == "professional":
        categories = ["modern", "luxury"]
    elif rel_ctx["closeness"] == "romantic":
        categories = ["romantic", "personalized", "luxury"]
    if occ_ctx["type"] == "festival":
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


HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="0">
    <title>GiftingGenie</title>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🎁</text></svg>">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: system-ui, sans-serif; background: linear-gradient(135deg, #667eea, #764ba2); min-height: 100vh; padding: 20px; }
        .container { max-width: 800px; margin: 0 auto; }
        .header { text-align: center; color: white; margin-bottom: 30px; }
        .header h1 { font-size: 2.5rem; margin-bottom: 10px; }
        .card { background: white; border-radius: 20px; padding: 30px; box-shadow: 0 10px 40px rgba(0,0,0,0.2); }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 8px; font-weight: 600; color: #333; }
        .form-group select, .form-group input { width: 100%; padding: 12px; border: 2px solid #e0e0e0; border-radius: 8px; font-size: 16px; }
        .form-group select:focus, .form-group input:focus { outline: none; border-color: #667eea; }
        .btn { width: 100%; padding: 15px; background: linear-gradient(135deg, #667eea, #764ba2); color: white; border: none; border-radius: 8px; font-size: 18px; font-weight: 600; cursor: pointer; }
        .btn:hover { opacity: 0.9; }
        .btn:disabled { opacity: 0.5; cursor: not-allowed; }
        .results { display: none; margin-top: 30px; }
        .gift-card { background: #f8f9fa; border-radius: 12px; padding: 20px; margin-bottom: 15px; }
        .gift-title { font-size: 1.2rem; font-weight: 600; color: #333; margin-bottom: 8px; }
        .gift-price { font-size: 1.5rem; color: #667eea; font-weight: 700; margin-bottom: 10px; }
        .gift-links { display: flex; gap: 10px; }
        .gift-links a { flex: 1; padding: 10px; text-align: center; border-radius: 6px; text-decoration: none; font-weight: 600; color: white; }
        .amazon { background: #FF9900; }
        .flipkart { background: #2874F0; }
        .error { background: #ff4444; color: white; padding: 15px; border-radius: 8px; margin-top: 15px; display: none; }
        .loading { display: none; text-align: center; padding: 30px; }
        .spinner { width: 40px; height: 40px; border: 4px solid #f3f3f3; border-top: 4px solid #667eea; border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto 15px; }
        @keyframes spin { to { transform: rotate(360deg); } }
        .back-btn { display: block; margin: 20px auto; padding: 10px 30px; background: white; color: #667eea; border: 2px solid #667eea; border-radius: 8px; cursor: pointer; font-weight: 600; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎁 GiftingGenie</h1>
            <p>Your Personal Indian Gifting Concierge</p>
        </div>
        <div class="card">
            <div id="formSection">
                <form id="giftForm">
                    <div class="form-group">
                        <label>Relationship</label>
                        <select id="relationship" required>
                            <option value="">Select...</option>
                            <option value="Mother">Mother</option>
                            <option value="Father">Father</option>
                            <option value="Brother">Brother</option>
                            <option value="Sister">Sister</option>
                            <option value="Wife">Wife</option>
                            <option value="Husband">Husband</option>
                            <option value="Friend">Friend</option>
                            <option value="Boss">Boss</option>
                            <option value="Colleague">Colleague</option>
                            <option value="Saali">Saali</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Occasion</label>
                        <select id="occasion" required>
                            <option value="">Select...</option>
                            <option value="Birthday">Birthday</option>
                            <option value="Diwali">Diwali</option>
                            <option value="Wedding">Wedding</option>
                            <option value="Anniversary">Anniversary</option>
                            <option value="Raksha Bandhan">Raksha Bandhan</option>
                            <option value="Holi">Holi</option>
                            <option value="New Year">New Year</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Budget (INR)</label>
                        <input type="number" id="budget" placeholder="2000" min="100" max="1000000" required>
                    </div>
                    <button type="submit" class="btn" id="submitBtn">Find Perfect Gifts</button>
                </form>
                <div class="error" id="error"></div>
            </div>
            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p>Finding perfect gifts...</p>
            </div>
            <div class="results" id="results">
                <div id="giftsContainer"></div>
                <button class="back-btn" onclick="reset()">Find More Gifts</button>
            </div>
        </div>
    </div>
    <script>
        document.getElementById('giftForm').onsubmit = async (e) => {
            e.preventDefault();
            const data = {
                relationship: document.getElementById('relationship').value,
                occasion: document.getElementById('occasion').value,
                age_group: 'Adult',
                vibe: 'Traditional',
                budget: parseInt(document.getElementById('budget').value)
            };
            document.getElementById('formSection').style.display = 'none';
            document.getElementById('loading').style.display = 'block';
            document.getElementById('error').style.display = 'none';
            try {
                const res = await fetch('/api/v1/recommend', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(data)
                });
                if (!res.ok) throw new Error('Request failed');
                const result = await res.json();
                showResults(result);
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
            const container = document.getElementById('giftsContainer');
            container.innerHTML = data.recommendations.map(g =>
                '<div class="gift-card"><div class="gift-title">' + g.title + '</div><div class="gift-price">' + g.approx_price_inr + '</div><div class="gift-links"><a href="' + g.purchase_links.amazon_in + '" target="_blank" class="amazon">Amazon</a><a href="' + g.purchase_links.flipkart + '" target="_blank" class="flipkart">Flipkart</a></div></div>'
            ).join('');
        }
        function reset() {
            document.getElementById('giftForm').reset();
            document.getElementById('results').style.display = 'none';
            document.getElementById('formSection').style.display = 'block';
        }
    </script>
</body>
</html>"""


@app.get("/", response_class=HTMLResponse)
async def root():
    return HTMLResponse(
        content=HTML_PAGE,
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0"
        }
    )


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.get("/favicon.ico")
async def favicon():
    return Response(
        content='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><text y=".9em" font-size="90">🎁</text></svg>',
        media_type="image/svg+xml"
    )


@app.post("/api/v1/recommend")
async def recommend(request: GiftRequest):
    try:
        return get_recommendations(
            request.relationship,
            request.occasion,
            request.age_group or "Adult",
            request.vibe or "Traditional",
            request.budget
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/occasions")
async def occasions():
    return {"occasions": list(OCCASION_CONTEXT.keys())}


@app.get("/api/v1/relationships")
async def relationships():
    return {"relationships": list(RELATIONSHIP_CONTEXT.keys())}


# Vercel handler
handler = Mangum(app, lifespan="off")
