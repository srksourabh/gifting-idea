# 📖 GiftingGenie API - Usage Examples

## Complete Request/Response Examples

### Example 1: Raksha Bandhan Gift for Saali (Sister-in-law)

**Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/recommend" \
  -H "Content-Type: application/json" \
  -d '{
    "relationship": "Saali",
    "occasion": "Raksha Bandhan",
    "age_group": "Adult",
    "vibe": "Traditional",
    "budget": 2000
  }'
```

**Expected Response Structure:**
```json
{
  "thinking_trace": "Analyzing gift for Saali on Raksha Bandhan. Considering casual formality, very_high cultural significance, and ₹2000 budget.",
  "recommendations": [
    {
      "id": 1,
      "title": "Traditional Silk Saree",
      "description": "Perfect for Saali on Raksha Bandhan, combines thoughtfulness with utility",
      "approx_price_inr": "₹2,100",
      "purchase_links": {
        "amazon_in": "https://www.amazon.in/s?k=Traditional+Silk+Saree",
        "flipkart": "https://www.flipkart.com/search?q=Traditional+Silk+Saree"
      }
    },
    {
      "id": 2,
      "title": "Silver Pooja Items",
      "description": "Culturally appropriate choice that honors the Raksha Bandhan celebration tradition",
      "approx_price_inr": "₹1,950",
      "purchase_links": {
        "amazon_in": "https://www.amazon.in/s?k=Silver+Pooja+Items",
        "flipkart": "https://www.flipkart.com/search?q=Silver+Pooja+Items"
      }
    }
  ],
  "pro_tip": "Present the gift after the rakhi ceremony. Include sweets for tradition."
}
```

---

### Example 2: Boss Birthday (Professional Setting)

**Request:**
```json
{
  "relationship": "Boss",
  "occasion": "Birthday",
  "age_group": "Adult",
  "vibe": "Formal",
  "budget": 5000
}
```

**Key Features:**
- Formal, professional gifts
- Higher budget items
- Luxury and modern categories
- Workplace-appropriate selections

---

### Example 3: Mother on Diwali

**Request:**
```json
{
  "relationship": "Mother",
  "occasion": "Diwali",
  "age_group": "Senior",
  "vibe": "Traditional",
  "budget": 3000
}
```

**Cultural Considerations:**
- Traditional and festive categories prioritized
- Auspicious items selected
- Pro tip about avoiding black colored gifts
- Focus on traditional values

---

### Example 4: Girlfriend on Valentine's Day

**Request:**
```json
{
  "relationship": "Girlfriend",
  "occasion": "Valentine's Day",
  "age_group": "Adult",
  "vibe": "Romantic",
  "budget": 4000
}
```

**Romantic Focus:**
- Personalized and romantic categories
- Modern, thoughtful gifts
- Emphasis on emotional connection
- Valentine-specific selections

---

### Example 5: Friend's Wedding

**Request:**
```json
{
  "relationship": "Friend",
  "occasion": "Wedding",
  "age_group": "Adult",
  "vibe": "Modern",
  "budget": 10000
}
```

**Wedding Considerations:**
- Higher budget for significant milestone
- Traditional + modern mix
- Home and luxury items
- Pro tip about auspicious odd numbers

---

## Testing Different Scenarios

### Low Budget Scenario (₹500)

```json
{
  "relationship": "Colleague",
  "occasion": "Birthday",
  "age_group": "Adult",
  "vibe": "Modern",
  "budget": 500
}
```

### High Budget Scenario (₹50,000)

```json
{
  "relationship": "Wife",
  "occasion": "Anniversary",
  "age_group": "Adult",
  "vibe": "Luxury",
  "budget": 50000
}
```

### Child Recipient

```json
{
  "relationship": "Son",
  "occasion": "Birthday",
  "age_group": "Child",
  "vibe": "Fun",
  "budget": 3000
}
```

### Senior Recipient

```json
{
  "relationship": "Father",
  "occasion": "Retirement",
  "age_group": "Senior",
  "vibe": "Traditional",
  "budget": 8000
}
```

---

## Using Different HTTP Clients

### Python with requests

```python
import requests
import json

url = "http://localhost:8000/api/v1/recommend"

payload = {
    "relationship": "Mother",
    "occasion": "Birthday",
    "age_group": "Senior",
    "vibe": "Traditional",
    "budget": 2500
}

response = requests.post(url, json=payload)
result = response.json()

print(json.dumps(result, indent=2, ensure_ascii=False))
```

### JavaScript with Axios

```javascript
const axios = require('axios');

const payload = {
  relationship: 'Boss',
  occasion: 'Promotion',
  age_group: 'Adult',
  vibe: 'Formal',
  budget: 6000
};

axios.post('http://localhost:8000/api/v1/recommend', payload)
  .then(response => {
    console.log(JSON.stringify(response.data, null, 2));
  })
  .catch(error => {
    console.error('Error:', error);
  });
```

### Using Postman

1. Create a new POST request
2. URL: `http://localhost:8000/api/v1/recommend`
3. Headers: `Content-Type: application/json`
4. Body (raw JSON):
```json
{
  "relationship": "Saali",
  "occasion": "Raksha Bandhan",
  "age_group": "Adult",
  "vibe": "Traditional",
  "budget": 2000
}
```
5. Send request

---

## Utility Endpoints

### Check API Health

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy"
}
```

### List All Occasions

```bash
curl http://localhost:8000/api/v1/occasions
```

Response:
```json
{
  "occasions": [
    "raksha bandhan",
    "wedding",
    "birthday",
    "anniversary",
    "diwali",
    "holi",
    "graduation",
    "promotion",
    "baby shower",
    "house warming",
    "retirement",
    "valentine's day"
  ]
}
```

### List All Relationships

```bash
curl http://localhost:8000/api/v1/relationships
```

Response:
```json
{
  "relationships": [
    "saali",
    "boss",
    "mother",
    "father",
    "wife",
    "husband",
    "brother",
    "sister",
    "friend",
    "colleague",
    "son",
    "daughter",
    "boyfriend",
    "girlfriend"
  ]
}
```

---

## Error Handling

### Invalid Budget (Too Low)

**Request:**
```json
{
  "relationship": "Friend",
  "occasion": "Birthday",
  "age_group": "Adult",
  "vibe": "Modern",
  "budget": 50
}
```

**Response (422):**
```json
{
  "detail": [
    {
      "loc": ["body", "budget"],
      "msg": "ensure this value is greater than or equal to 100",
      "type": "value_error.number.not_ge"
    }
  ]
}
```

### Missing Required Field

**Request:**
```json
{
  "relationship": "Mother",
  "age_group": "Senior",
  "budget": 2000
}
```

**Response (422):**
```json
{
  "detail": [
    {
      "loc": ["body", "occasion"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

## Pro Tips by Occasion

| Occasion | Pro Tip |
|----------|---------|
| Diwali | Always include a handwritten card with Diwali wishes. Avoid black colored gifts. |
| Raksha Bandhan | Present the gift after the rakhi ceremony. Include sweets for tradition. |
| Wedding | Gifts in odd numbers are considered auspicious. Include shagun envelope. |
| Birthday | Personalized gifts show extra thought. Consider their hobbies and interests. |
| Anniversary | Gifts symbolizing togetherness work best. Avoid sharp objects like knives. |

---

## Integration Tips for Mobile Apps

1. **Cache occasions and relationships**: Fetch lists once and cache locally
2. **Handle network errors**: Implement retry logic for failed requests
3. **Display loading states**: API typically responds in < 500ms
4. **Deep linking**: Use the purchase_links for direct e-commerce navigation
5. **Analytics**: Track which recommendations users click on
6. **Feedback loop**: Allow users to rate recommendations

---

**Happy Gifting! 🎁**
