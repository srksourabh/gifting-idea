# 🚀 GiftingGenie - Quick Start Guide

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation & Running

### Option 1: Using the Start Script (Easiest)

```bash
# Make the script executable (first time only)
chmod +x start.sh

# Run the start script
./start.sh
```

The script will:
1. Install all dependencies
2. Start the server automatically
3. Display the URLs you need

### Option 2: Manual Installation

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start the server
python app.py
```

### Option 3: Using uvicorn directly

```bash
# Install dependencies
pip install -r requirements.txt

# Start with uvicorn
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

## Access the Application

Once the server is running, open your browser and go to:

🌐 **Web Interface:** http://localhost:8000

📖 **API Documentation:** http://localhost:8000/docs

✅ **Health Check:** http://localhost:8000/health

## Using the Web Interface

1. **Fill in the form:**
   - Select relationship (Mother, Boss, Saali, Friend, etc.)
   - Choose occasion (Diwali, Birthday, Wedding, etc.)
   - Pick age group (Child, Adult, Senior, etc.)
   - Select vibe (Traditional, Modern, Luxury, etc.)
   - Enter budget in INR

2. **Click "Find Perfect Gifts"**

3. **Get your recommendations:**
   - 5 personalized gift ideas
   - Prices in INR
   - Direct Amazon & Flipkart shopping links
   - Cultural pro tips

4. **Shop directly** by clicking the Amazon or Flipkart buttons

## Troubleshooting

### Port Already in Use

If you see an error about port 8000 being in use:

```bash
# Option 1: Kill the process using port 8000
# On Linux/Mac:
lsof -ti:8000 | xargs kill -9

# Option 2: Use a different port
uvicorn app:app --port 8080
```

Then access at http://localhost:8080

### Module Not Found Errors

If you see errors about missing modules:

```bash
# Make sure you're in the project directory
cd gifting-idea

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### API Not Responding

If the web interface shows "Failed to fetch":

1. Make sure the server is running (you should see startup logs)
2. Check that you're accessing http://localhost:8000 (not a different port)
3. Check browser console for errors (F12 → Console tab)
4. Verify the API is working: http://localhost:8000/health

## Testing the API

### Using the Web Interface
Simply go to http://localhost:8000 and use the form!

### Using the Interactive API Docs
Go to http://localhost:8000/docs and try the `/api/v1/recommend` endpoint

### Using curl

```bash
curl -X POST "http://localhost:8000/api/v1/recommend" \
  -H "Content-Type: application/json" \
  -d '{
    "relationship": "Mother",
    "occasion": "Diwali",
    "age_group": "Senior",
    "vibe": "Traditional",
    "budget": 3000
  }'
```

### Using Python Test Script

```bash
python test_api.py
```

## Features

✨ **Beautiful Web UI** - No coding required!
🇮🇳 **Indian Context** - Culturally appropriate recommendations
💰 **Budget-Aware** - Suggestions within your budget
🛒 **Direct Shopping** - Links to Amazon India & Flipkart
💡 **Pro Tips** - Cultural advice for gifting
📱 **Mobile Friendly** - Works on all devices

## Next Steps

- Try different relationship and occasion combinations
- Adjust budgets to see different recommendations
- Share the URL with friends and family
- Check out the API docs to integrate with your app

## Support

For issues or questions, check:
- README.md - Full documentation
- API_EXAMPLES.md - API usage examples
- WEB_INTERFACE.md - Web UI details

---

**Enjoy finding the perfect gifts! 🎁**
