from http.server import BaseHTTPRequestHandler
import json
import random
from urllib.parse import quote_plus, parse_qs, urlparse


# Gift data
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

OCCASIONS = ["diwali", "holi", "raksha bandhan", "birthday", "wedding", "anniversary", "new year"]


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


HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GiftingGenie</title>
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
        .btn { width: 100%; padding: 15px; background: linear-gradient(135deg, #667eea, #764ba2); color: white; border: none; border-radius: 8px; font-size: 18px; font-weight: 600; cursor: pointer; }
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
        #results { display: none; }
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
                    <button type="submit" class="btn">Find Perfect Gifts</button>
                </form>
                <div class="error" id="error"></div>
            </div>
            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p>Finding perfect gifts...</p>
            </div>
            <div id="results">
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
                budget: parseInt(document.getElementById('budget').value)
            };
            document.getElementById('formSection').style.display = 'none';
            document.getElementById('loading').style.display = 'block';
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
            document.getElementById('giftsContainer').innerHTML = data.recommendations.map(g =>
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


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "healthy"}).encode())
        else:
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode())

    def do_POST(self):
        if self.path == '/api/recommend':
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
        else:
            self.send_response(404)
            self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
