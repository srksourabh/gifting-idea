# 🚀 Vercel Deployment Guide for GiftingGenie

This guide will help you deploy the GiftingGenie API to Vercel so you can share it with anyone via a public URL.

## ✅ Prerequisites

- GitHub account
- Vercel account (free tier works perfectly)
- This repository pushed to GitHub

## 📋 Deployment Steps

### Option 1: Deploy via Vercel Dashboard (Easiest)

1. **Go to Vercel**
   - Visit [vercel.com](https://vercel.com)
   - Sign in with your GitHub account

2. **Import Project**
   - Click "Add New..." → "Project"
   - Select your `gifting-idea` repository
   - Click "Import"

3. **Configure Project**
   - **Framework Preset:** Other
   - **Root Directory:** `./` (leave as default)
   - **Build Command:** Leave empty
   - **Output Directory:** Leave empty
   - **Install Command:** `pip install -r requirements.txt`

4. **Deploy**
   - Click "Deploy"
   - Wait 2-3 minutes for deployment
   - Your app will be live at `https://your-project.vercel.app`

### Option 2: Deploy via Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy
vercel

# For production deployment
vercel --prod
```

## 🌐 Your Deployed URLs

After deployment, you'll get:

- **Web Interface:** `https://your-project.vercel.app`
- **API Docs:** `https://your-project.vercel.app/docs`
- **API Endpoint:** `https://your-project.vercel.app/api/v1/recommend`
- **Health Check:** `https://your-project.vercel.app/health`

## 📁 Vercel Configuration Files

This project includes:

- **`vercel.json`** - Vercel configuration
- **`api/index.py`** - Serverless function entry point
- **`requirements.txt`** - Python dependencies

These files are already configured for you!

## ✨ What Works on Vercel

✅ Full web interface at root URL
✅ All API endpoints
✅ Static file serving
✅ CORS enabled for API calls
✅ Automatic HTTPS
✅ Global CDN distribution
✅ Auto-scaling

## 🎯 Sharing Your Deployed App

Once deployed, share these URLs with users:

**For End Users (Non-Technical):**
```
🎁 Find Perfect Gifts: https://your-project.vercel.app

Simply fill the form and get 5 gift recommendations instantly!
```

**For Developers:**
```
📖 API Documentation: https://your-project.vercel.app/docs

Try our Indian gifting recommendation API with cultural intelligence.
```

## 🔧 Environment Variables (Optional)

If you need to add environment variables:

1. Go to your project on Vercel
2. Click "Settings" → "Environment Variables"
3. Add your variables
4. Redeploy

## 🐛 Troubleshooting

### Deployment Failed

**Check the build logs:**
1. Go to your deployment on Vercel
2. Click on the failed deployment
3. Check the "Build Logs" section

**Common issues:**
- Missing dependencies → Make sure `requirements.txt` is complete
- Python version → Vercel uses Python 3.9 by default
- Import errors → Check that all files are committed

### API Not Working

**Check these:**
1. Visit `/health` endpoint - should return `{"status": "healthy"}`
2. Check `/docs` - should show FastAPI documentation
3. Check browser console for errors

### Static Files Not Loading

The web interface should load automatically at the root URL (`/`). If not:
1. Check that `static/index.html` exists
2. Verify `app.py` has the `FileResponse` for root path
3. Check Vercel logs for errors

## 🔄 Updating Your Deployment

Vercel automatically redeploys when you push to GitHub:

```bash
# Make changes to your code
git add .
git commit -m "Update features"
git push

# Vercel will automatically redeploy!
```

## 💰 Pricing

**Vercel Free Tier includes:**
- Unlimited deployments
- Automatic HTTPS
- 100 GB bandwidth/month
- Serverless function executions
- Custom domains (if you have one)

This is perfect for the GiftingGenie app!

## 🎨 Custom Domain (Optional)

To use your own domain:

1. Go to project settings on Vercel
2. Click "Domains"
3. Add your custom domain
4. Update DNS records as instructed
5. Done! Your app will be at `yourdomain.com`

## 📊 Monitoring

Vercel provides built-in analytics:

- **Usage:** Track API calls and page views
- **Performance:** Monitor response times
- **Errors:** See runtime errors
- **Logs:** Real-time function logs

Access via: Project → "Analytics" or "Logs"

## 🚀 Performance Tips

1. **Caching:** Vercel automatically caches static assets
2. **Edge Network:** Your app is served from global CDN
3. **Serverless:** API scales automatically with traffic
4. **HTTPS:** Enabled by default, improves SEO

## 📱 Testing Your Deployment

After deployment, test these URLs:

```bash
# Test health endpoint
curl https://your-project.vercel.app/health

# Test API recommendation
curl -X POST "https://your-project.vercel.app/api/v1/recommend" \
  -H "Content-Type: application/json" \
  -d '{
    "relationship": "Mother",
    "occasion": "Diwali",
    "age_group": "Senior",
    "vibe": "Traditional",
    "budget": 3000
  }'

# Test web interface
# Open in browser: https://your-project.vercel.app
```

## 🎉 Success!

Your GiftingGenie app is now live and accessible to anyone worldwide!

**Share your URL and help people find the perfect gifts! 🎁**

---

## 📞 Support

If you encounter issues:

1. Check Vercel's deployment logs
2. Review this deployment guide
3. Check the main README.md for API details
4. Verify all files are committed to Git

## 🔗 Useful Links

- [Vercel Documentation](https://vercel.com/docs)
- [FastAPI on Vercel](https://vercel.com/guides/using-fastapi-with-vercel)
- [Vercel CLI Reference](https://vercel.com/docs/cli)

---

**Made with ❤️ for the Indian gifting experience**
