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

    # Select categories based on relationship and vibe
    if rel_type == "immediate_family":
        categories = ["personalized", "luxury", "wellness"]
    elif rel_type == "professional":
        categories = ["modern", "luxury"]
    elif rel_type == "romantic":
        categories = ["romantic", "personalized", "luxury"]
    else:
        categories = ["traditional", "modern", "personalized"]

    # Add vibe-specific categories
    vibe_lower = vibe.lower() if vibe else ""
    if "traditional" in vibe_lower:
        categories.insert(0, "traditional")
    if "tech" in vibe_lower:
        categories.insert(0, "tech")
    if "wellness" in vibe_lower:
        categories.insert(0, "wellness")
    if "luxury" in vibe_lower:
        categories.insert(0, "luxury")

    # Add festival-specific
    if occ_type == "festival":
        categories.insert(0, "festive")

    # Age-specific adjustments
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

    # Get pro tip
    pro_tip = PRO_TIPS.get(occasion.lower(), PRO_TIPS.get("professional" if rel_type == "professional" else "default", PRO_TIPS["default"]))

    return {
        "thinking_trace": f"Analyzing gift for {relationship} on {occasion}. Considering {rel_type} relationship type, {occ_type} occasion, {age_group} age group, {vibe} style preference, and Rs.{budget:,} budget.",
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
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Poppins', sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; color: #333; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { text-align: center; color: white; margin-bottom: 40px; animation: fadeInDown 0.8s ease-out; }
        .header h1 { font-size: 3rem; font-weight: 700; margin-bottom: 10px; text-shadow: 2px 2px 4px rgba(0,0,0,0.2); }
        .header .subtitle { font-size: 1.2rem; font-weight: 300; opacity: 0.95; }
        .header .emoji { font-size: 3.5rem; display: inline-block; animation: bounce 2s infinite; }
        .main-card { background: white; border-radius: 24px; padding: 40px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); animation: fadeInUp 0.8s ease-out; }
        .form-title { font-size: 1.8rem; color: #667eea; margin-bottom: 30px; text-align: center; font-weight: 600; }
        .form-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 20px; margin-bottom: 30px; }
        .form-group { display: flex; flex-direction: column; }
        .form-group label { font-weight: 600; margin-bottom: 8px; color: #555; font-size: 0.9rem; }
        .form-group select, .form-group input { padding: 14px 16px; border: 2px solid #e0e0e0; border-radius: 12px; font-size: 1rem; font-family: 'Poppins', sans-serif; transition: all 0.3s ease; background: #f8f9fa; }
        .form-group select:focus, .form-group input:focus { outline: none; border-color: #667eea; background: white; box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1); }
        .submit-btn { width: 100%; padding: 18px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 12px; font-size: 1.2rem; font-weight: 600; cursor: pointer; transition: all 0.3s ease; box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4); }
        .submit-btn:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6); }
        .loading { display: none; text-align: center; padding: 50px; }
        .spinner { border: 4px solid #f3f3f3; border-top: 4px solid #667eea; border-radius: 50%; width: 50px; height: 50px; animation: spin 1s linear infinite; margin: 0 auto 20px; }
        .results-section { display: none; margin-top: 40px; }
        .results-header { text-align: center; margin-bottom: 25px; }
        .results-header h2 { font-size: 2rem; color: #667eea; }
        .thinking-trace { background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); padding: 20px; border-radius: 12px; margin-bottom: 25px; border-left: 4px solid #667eea; }
        .thinking-trace h3 { color: #667eea; font-size: 1rem; margin-bottom: 8px; }
        .thinking-trace p { color: #666; line-height: 1.6; font-size: 0.95rem; }
        .gifts-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin-bottom: 25px; }
        .gift-card { background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%); border-radius: 16px; padding: 25px; box-shadow: 0 8px 25px rgba(0,0,0,0.08); transition: all 0.3s ease; border: 2px solid transparent; }
        .gift-card:hover { transform: translateY(-5px); box-shadow: 0 12px 35px rgba(102, 126, 234, 0.15); border-color: #667eea; }
        .gift-number { display: inline-flex; align-items: center; justify-content: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; width: 32px; height: 32px; border-radius: 50%; font-weight: 600; margin-bottom: 12px; font-size: 0.9rem; }
        .gift-title { font-size: 1.25rem; color: #333; margin-bottom: 10px; font-weight: 600; }
        .gift-description { color: #666; margin-bottom: 12px; line-height: 1.5; font-size: 0.9rem; }
        .gift-price { font-size: 1.6rem; color: #667eea; font-weight: 700; margin-bottom: 15px; }
        .purchase-links { display: flex; gap: 10px; }
        .purchase-btn { flex: 1; padding: 12px; border-radius: 8px; text-decoration: none; text-align: center; font-weight: 600; transition: all 0.3s ease; font-size: 0.9rem; color: white; }
        .amazon-btn { background: #FF9900; }
        .amazon-btn:hover { background: #e88b00; }
        .flipkart-btn { background: #2874F0; }
        .flipkart-btn:hover { background: #1a5dc7; }
        .pro-tip { background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); padding: 20px; border-radius: 12px; text-align: center; margin-bottom: 20px; }
        .pro-tip h3 { color: #e65100; font-size: 1.1rem; margin-bottom: 8px; }
        .pro-tip p { color: #bf360c; line-height: 1.6; }
        .back-btn { display: block; margin: 0 auto; padding: 12px 40px; background: white; color: #667eea; border: 2px solid #667eea; border-radius: 10px; font-weight: 600; cursor: pointer; transition: all 0.3s ease; font-size: 1rem; }
        .back-btn:hover { background: #667eea; color: white; }
        .error { background: #ffebee; color: #c62828; padding: 15px; border-radius: 10px; margin-top: 15px; display: none; text-align: center; }
        @keyframes fadeInDown { from { opacity: 0; transform: translateY(-30px); } to { opacity: 1; transform: translateY(0); } }
        @keyframes fadeInUp { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: translateY(0); } }
        @keyframes bounce { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-10px); } }
        @keyframes spin { to { transform: rotate(360deg); } }
        @media (max-width: 768px) { .header h1 { font-size: 2.2rem; } .main-card { padding: 25px; } .form-grid { grid-template-columns: 1fr; } }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="emoji">🎁</div>
            <h1>GiftingGenie</h1>
            <p class="subtitle">Your Personal Indian Gifting Concierge - Find the Perfect Gift</p>
        </div>
        <div class="main-card">
            <div id="formSection">
                <h2 class="form-title">Tell Us About Your Gift Recipient</h2>
                <form id="giftForm">
                    <div class="form-grid">
                        <div class="form-group">
                            <label>👥 Relationship</label>
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
                            <label>🎉 Occasion</label>
                            <select id="occasion" required>
                                <option value="">Select Occasion</option>
                                <optgroup label="Major Festivals">
                                    <option value="Diwali">Diwali</option>
                                    <option value="Holi">Holi</option>
                                    <option value="Raksha Bandhan">Raksha Bandhan</option>
                                    <option value="Durga Puja">Durga Puja</option>
                                    <option value="Ganesh Chaturthi">Ganesh Chaturthi</option>
                                    <option value="Navratri">Navratri</option>
                                    <option value="Eid">Eid</option>
                                    <option value="Christmas">Christmas</option>
                                    <option value="Pongal">Pongal</option>
                                    <option value="Onam">Onam</option>
                                    <option value="Karva Chauth">Karva Chauth</option>
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
                                <optgroup label="Other">
                                    <option value="New Year">New Year</option>
                                    <option value="Valentine's Day">Valentine's Day</option>
                                    <option value="Mother's Day">Mother's Day</option>
                                    <option value="Father's Day">Father's Day</option>
                                </optgroup>
                            </select>
                        </div>
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
                            <input type="number" id="budget" placeholder="Enter amount (e.g., 2000)" min="100" max="1000000" required>
                        </div>
                    </div>
                    <button type="submit" class="submit-btn">✨ Find Perfect Gifts</button>
                </form>
                <div class="error" id="error"></div>
            </div>
            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p style="color: #667eea; font-size: 1.1rem;">Finding the perfect gifts for you...</p>
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
                <button class="back-btn" onclick="reset()">🔄 Find More Gifts</button>
            </div>
        </div>
    </div>
    <script>
        document.getElementById('giftForm').onsubmit = async (e) => {
            e.preventDefault();
            const data = {
                relationship: document.getElementById('relationship').value,
                occasion: document.getElementById('occasion').value,
                age_group: document.getElementById('ageGroup').value,
                vibe: document.getElementById('vibe').value,
                budget: parseInt(document.getElementById('budget').value)
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
            document.getElementById('giftsGrid').innerHTML = data.recommendations.map(g =>
                '<div class="gift-card"><div class="gift-number">' + g.id + '</div><div class="gift-title">' + g.title + '</div><div class="gift-description">' + g.description + '</div><div class="gift-price">' + g.approx_price_inr + '</div><div class="purchase-links"><a href="' + g.purchase_links.amazon_in + '" target="_blank" class="purchase-btn amazon-btn">🛒 Amazon</a><a href="' + g.purchase_links.flipkart + '" target="_blank" class="purchase-btn flipkart-btn">🛍️ Flipkart</a></div></div>'
            ).join('');
            document.getElementById('results').scrollIntoView({ behavior: 'smooth' });
        }
        function reset() {
            document.getElementById('giftForm').reset();
            document.getElementById('results').style.display = 'none';
            document.getElementById('formSection').style.display = 'block';
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
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
