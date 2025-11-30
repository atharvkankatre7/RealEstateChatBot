# OpenAI API Key Setup Guide

## 🔑 How to Get Your OpenAI API Key

### Step 1: Create an OpenAI Account

1. **Visit OpenAI Platform:**
   - Go to [https://platform.openai.com/](https://platform.openai.com/)

2. **Sign Up:**
   - Click "Sign Up" or "Log In"
   - Use your email, Google account, or Microsoft account
   - Complete the verification process

### Step 2: Add Payment Method (Required)

⚠️ **Important:** OpenAI requires a payment method to be added, even for free credits.

1. Go to **Settings** → **Billing**
2. Click **Add Payment Method**
3. Add your credit/debit card
4. Don't worry - you'll get free credits first (see pricing below)

### Step 3: Get Your API Key

1. **Navigate to API Keys:**
   - Go to [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
   - Or: Click your profile → **View API keys**

2. **Create New Key:**
   - Click **"Create new secret key"**
   - Give it a name (e.g., "Real Estate Chatbot")
   - Click **"Create secret key"**

3. **Copy Your Key:**
   - ⚠️ **IMPORTANT:** Copy the key immediately - you won't see it again!
   - It will look like: `sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
   - Save it securely

## 💰 Is OpenAI API Free?

### Free Credits (New Users)

✅ **Yes, you get free credits when you sign up!**

- **$5 free credits** for new accounts
- Credits expire after **3 months** (if not used)
- No credit card required initially, but you need to add one to use the API

### Pricing Model

OpenAI uses a **pay-as-you-go** model:

**GPT-3.5-turbo (used in this project):**
- **Input:** $0.50 per 1M tokens
- **Output:** $1.50 per 1M tokens

**What does this mean?**
- 1 token ≈ 4 characters
- A typical query uses ~500-1000 tokens
- **$5 free credits = ~3,000-6,000 queries** (rough estimate)

### Cost Estimation for This Project

For the Real Estate Chatbot:
- Each summary uses ~500 tokens
- **Cost per query:** ~$0.0005 - $0.001 (less than 1 cent!)
- **$5 free credits = ~5,000-10,000 queries**

### Free Alternatives

If you want to avoid costs entirely:

1. **Use Mock Summaries (Default):**
   - The app works perfectly without OpenAI
   - Just don't set the `OPENAI_API_KEY`
   - You'll get data-driven summaries (still very good!)

2. **Other Free LLM Options:**
   - **Hugging Face Inference API** (free tier available)
   - **Ollama** (local, completely free)
   - **Google Gemini** (free tier available)

## 🚀 Setting Up the API Key

### Local Development

**Option 1: Environment Variable (Recommended)**
```bash
# Windows (PowerShell)
$env:OPENAI_API_KEY="sk-your-key-here"

# Windows (CMD)
set OPENAI_API_KEY=sk-your-key-here

# macOS/Linux
export OPENAI_API_KEY=sk-your-key-here
```

**Option 2: .env File (Backend)**
Create `backend/.env`:
```env
OPENAI_API_KEY=sk-your-key-here
```

Then update `backend/backend/settings.py` to load it:
```python
from dotenv import load_dotenv
load_dotenv()
```

### Production (Render)

1. Go to your Render dashboard
2. Select your backend service
3. Go to **Environment** tab
4. Click **Add Environment Variable**
5. Add:
   - **Key:** `OPENAI_API_KEY`
   - **Value:** `sk-your-key-here`
6. Save and redeploy

## 🔒 Security Best Practices

1. **Never commit API keys to Git:**
   - Add `.env` to `.gitignore`
   - Never share keys in code or screenshots

2. **Use Environment Variables:**
   - Always use environment variables, not hardcoded keys

3. **Rotate Keys Regularly:**
   - If a key is exposed, delete it and create a new one

4. **Set Usage Limits:**
   - In OpenAI dashboard, set monthly spending limits
   - Get alerts when approaching limits

## 📊 Monitoring Usage

### Check Your Usage:

1. Go to [https://platform.openai.com/usage](https://platform.openai.com/usage)
2. View:
   - Tokens used
   - Cost incurred
   - Requests made

### Set Spending Limits:

1. Go to **Settings** → **Billing** → **Limits**
2. Set **Hard limit** (stops when reached)
3. Set **Soft limit** (sends email warning)

## 🎯 Recommendation

### For Development/Testing:
- ✅ Use the **$5 free credits** - plenty for testing
- ✅ Set a **spending limit** ($5-10) to avoid surprises

### For Production:
- ✅ Start with **free credits** to test
- ✅ Set **usage limits** and **alerts**
- ✅ Monitor usage regularly
- ✅ Consider **mock summaries** if costs are a concern

### If You Don't Want to Use OpenAI:
- ✅ **No problem!** The app works great without it
- ✅ Just don't set `OPENAI_API_KEY`
- ✅ You'll get intelligent mock summaries based on data

## 🆘 Troubleshooting

### "Invalid API Key" Error:
- Check that key starts with `sk-`
- Verify no extra spaces
- Make sure key is active in OpenAI dashboard

### "Insufficient Credits" Error:
- Check your usage at platform.openai.com/usage
- Add credits or payment method
- Check if free credits expired

### API Not Working:
- Verify API key is set correctly
- Check internet connection
- Check OpenAI status: status.openai.com

## 📝 Summary

- ✅ **Free credits available:** $5 for new users
- ✅ **Very affordable:** Less than 1 cent per query
- ✅ **Optional:** App works without it
- ✅ **Easy setup:** Just set environment variable
- ✅ **Safe:** Set spending limits

**Bottom line:** Try it with free credits! If you like it, it's very affordable. If not, the app works perfectly without it.

---

**Need Help?**
- OpenAI Docs: https://platform.openai.com/docs
- OpenAI Support: https://help.openai.com/

