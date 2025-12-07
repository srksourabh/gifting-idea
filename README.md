# 🎁 GiftingGenie API

**Expert Indian Personal Shopper & Gifting Concierge Backend Engine**

A FastAPI-based recommendation system that suggests culturally-appropriate gifts for Indian occasions, relationships, and budgets.

## 🌟 Features

- **Cultural Intelligence**: Deep understanding of Indian relationships, festivals, and gifting traditions
- **Smart Recommendations**: 5 unique gift suggestions per request
- **Budget-Aware**: Intelligent price estimation within specified budget
- **E-commerce Integration**: Direct search links for Amazon India and Flipkart
- **RESTful API**: Clean, well-documented API endpoints
- **Pro Tips**: Culturally-relevant advice for each occasion

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd gifting-idea

# Install dependencies
pip install -r requirements.txt
```

### Running the API

```bash
# Start the server
python app.py

# Or use uvicorn directly
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

Interactive API documentation: `http://localhost:8000/docs`

## 📚 API Endpoints

### 1. Generate Gift Recommendations

**POST** `/api/v1/recommend`

Generate 5 culturally-appropriate gift recommendations.

**Request Body:**
```json
{
  "relationship": "Saali",
  "occasion": "Raksha Bandhan",
  "age_group": "Adult",
  "vibe": "Traditional",
  "budget": 2000
}
```

**Response:**
```json
{
  "thinking_trace": "Brief summary of recommendation logic",
  "recommendations": [
    {
      "id": 1,
      "title": "Silver Pooja Items",
      "description": "Perfect for Saali on Raksha Bandhan, combines thoughtfulness with utility",
      "approx_price_inr": "₹2,000",
      "purchase_links": {
        "amazon_in": "https://www.amazon.in/s?k=Silver+Pooja+Items",
        "flipkart": "https://www.flipkart.com/search?q=Silver+Pooja+Items"
      }
    }
  ],
  "pro_tip": "Present the gift after the rakhi ceremony. Include sweets for tradition."
}
```

### 2. Health Check

**GET** `/health`

Check API health status.

### 3. List Supported Occasions

**GET** `/api/v1/occasions`

Get all supported occasions.

### 4. List Supported Relationships

**GET** `/api/v1/relationships`

Get all supported relationship types.

## 🎯 Supported Contexts

### Relationships
- Family: Mother, Father, Brother, Sister, Wife, Husband, Son, Daughter, Saali
- Professional: Boss, Colleague
- Social: Friend, Boyfriend, Girlfriend

### Occasions
- **Festivals**: Diwali, Raksha Bandhan, Holi
- **Milestones**: Wedding, Anniversary, Birthday, Graduation, Promotion
- **Celebrations**: Valentine's Day, House Warming, Baby Shower, Retirement

### Vibes
- Traditional/Ethnic
- Modern/Contemporary
- Personalized
- Luxury
- Wellness-focused
- Tech-savvy

### Age Groups
- Child (0-12)
- Teenager (13-19)
- Adult (20-59)
- Senior (60+)

## 🧪 Testing

Run the test suite to see the API in action:

```bash
python test_api.py
```

This will:
- Test multiple scenarios (professional, family, romantic relationships)
- Validate JSON schema compliance
- Display sample recommendations for each test case

## 💡 Example Usage

### Using cURL

```bash
curl -X POST "http://localhost:8000/api/v1/recommend" \
  -H "Content-Type: application/json" \
  -d '{
    "relationship": "Boss",
    "occasion": "Birthday",
    "age_group": "Adult",
    "vibe": "Formal",
    "budget": 5000
  }'
```

### Using Python requests

```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/recommend",
    json={
        "relationship": "Mother",
        "occasion": "Diwali",
        "age_group": "Senior",
        "vibe": "Traditional",
        "budget": 3000
    }
)

recommendations = response.json()
print(recommendations)
```

### Using JavaScript (fetch)

```javascript
fetch('http://localhost:8000/api/v1/recommend', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    relationship: 'Girlfriend',
    occasion: 'Valentine\'s Day',
    age_group: 'Adult',
    vibe: 'Romantic',
    budget: 4000
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

## 🏗️ Architecture

```
gifting-idea/
├── app.py                  # FastAPI application and endpoints
├── gifting_engine.py       # Core recommendation logic
├── requirements.txt        # Python dependencies
├── test_api.py            # Test suite
├── example_request.json   # Sample request
└── README.md              # Documentation
```

### Key Components

1. **GiftingEngine** (`gifting_engine.py`)
   - Cultural context analysis
   - Gift database with Indian products
   - Smart category selection
   - URL generation for e-commerce platforms

2. **FastAPI App** (`app.py`)
   - RESTful API endpoints
   - Request validation with Pydantic
   - CORS support for mobile apps
   - Interactive API documentation

## 🎨 Cultural Intelligence

The API incorporates Indian cultural nuances:

- **Auspicious Items**: Recommends culturally appropriate gifts (silver, traditional items)
- **Taboo Awareness**: Avoids inappropriate gifts (e.g., black items for Diwali)
- **Festival-Specific**: Special handling for Raksha Bandhan, Diwali, Holi, etc.
- **Relationship Sensitivity**: Adjusts formality based on relationship (Boss vs. Friend)
- **Pro Tips**: Includes cultural advice (e.g., "present with both hands")

## 📊 Budget Handling

- Prices generated within 70-110% of specified budget
- Rounded to nearest ₹50 for realism
- Considers Indian market pricing
- Supports budgets from ₹100 to ₹10,00,000

## 🔗 E-commerce Integration

Direct search URLs for:
- **Amazon India** (amazon.in)
- **Flipkart** (flipkart.com)

URLs are properly encoded and optimized for product discovery.

## 🚦 API Response Codes

- `200 OK`: Successful recommendation generation
- `422 Unprocessable Entity`: Invalid request parameters
- `500 Internal Server Error`: Server-side error

## 🔒 Security & CORS

CORS is enabled for all origins to support mobile app integration. In production, configure specific allowed origins in `app.py`:

```python
allow_origins=["https://your-app-domain.com"]
```

## 📝 License

This project is part of the GiftingGenie mobile application ecosystem.

## 🤝 Contributing

To extend the gift database or add new cultural contexts, edit the dictionaries in `gifting_engine.py`:

- `GIFT_DATABASE`: Add new gift categories and items
- `RELATIONSHIP_CONTEXT`: Add new relationship types
- `OCCASION_CONTEXT`: Add new occasions

## 📞 Support

For issues or questions, please contact the development team.

---

**Built with ❤️ for the Indian gifting experience**
