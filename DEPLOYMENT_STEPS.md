# 🚀 Quick Deployment Steps

Simple, step-by-step guide to deploy your Real Estate Chatbot.

## 📋 Prerequisites

- ✅ Code pushed to GitHub repository
- ✅ GitHub account
- ✅ Render account (free tier available)
- ✅ Vercel account (free tier available)

---

## 🔵 PART 1: Backend Deployment (Render)

### Step 1: Generate Django Secret Key

**On your local machine:**
```bash
cd backend
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Copy the generated key** (you'll need it in Step 3)

### Step 2: Create Render Account & Service

1. **Go to Render:**
   - Visit [https://dashboard.render.com](https://dashboard.render.com)
   - Sign up (free) or log in

2. **Create New Web Service:**
   - Click **"New +"** button (top right)
   - Select **"Web Service"**

3. **Connect GitHub:**
   - Click **"Connect GitHub"** or **"Connect GitLab"**
   - Authorize Render to access your repositories
   - Select your repository

4. **Configure Service:**
   ```
   Name: real-estate-backend
   Region: Choose closest to you
   Branch: main (or master)
   Root Directory: backend
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn backend.wsgi --log-file -
   ```

5. **Click "Create Web Service"** (don't deploy yet!)

### Step 3: Set Environment Variables

**In Render dashboard, go to your service → "Environment" tab:**

Click **"Add Environment Variable"** and add these one by one:

```
Key: SECRET_KEY
Value: [paste the key from Step 1]
```

```
Key: DEBUG
Value: False
```

```
Key: ALLOWED_HOSTS
Value: real-estate-backend.onrender.com
```
*(Replace with your actual service name if different)*

```
Key: CORS_ALLOWED_ORIGINS
Value: https://your-frontend.vercel.app
```
*(We'll update this after frontend deployment - use placeholder for now)*

**Optional (for OpenAI):**
```
Key: OPENAI_API_KEY
Value: sk-your-key-here
```
*(Only if you want AI summaries)*

### Step 4: Deploy Backend

1. **Click "Manual Deploy" → "Deploy latest commit"**
2. **Wait for build to complete** (3-5 minutes)
3. **Note your backend URL:** `https://real-estate-backend.onrender.com`

### Step 5: Verify Backend

**Test the health endpoint:**
```
https://your-backend.onrender.com/api/health/
```

**Should return:**
```json
{
  "status": "ok",
  "data_loaded": true,
  "rows": 20
}
```

✅ **Backend is live!**

---

## 🟢 PART 2: Frontend Deployment (Vercel)

### Step 1: Create Vercel Account

1. **Go to Vercel:**
   - Visit [https://vercel.com](https://vercel.com)
   - Sign up (free) or log in
   - Use GitHub to sign up (easiest)

### Step 2: Deploy via Vercel Dashboard

1. **Click "Add New..." → "Project"**

2. **Import Repository:**
   - Select your GitHub repository
   - Click **"Import"**

3. **Configure Project:**
   ```
   Framework Preset: Vite
   Root Directory: frontend
   Build Command: npm run build
   Output Directory: dist
   Install Command: npm install
   ```

4. **Click "Deploy"** (don't set env vars yet - we'll do that next)

5. **Wait for deployment** (1-2 minutes)

6. **Note your frontend URL:** `https://your-project.vercel.app`

### Step 3: Set Environment Variables

**In Vercel dashboard → Your Project → Settings → Environment Variables:**

Click **"Add New"** and add:

```
Key: VITE_API_URL
Value: https://real-estate-backend.onrender.com
```
*(Replace with your actual Render backend URL from Part 1, Step 4)*

**Click "Save"**

### Step 4: Redeploy Frontend

1. **Go to "Deployments" tab**
2. **Click "..." on latest deployment**
3. **Click "Redeploy"**
4. **Wait for redeployment** (1-2 minutes)

✅ **Frontend is live!**

---

## 🔄 PART 3: Connect Frontend & Backend

### Update Backend CORS

**Go back to Render dashboard:**

1. **Your Backend Service → Environment tab**
2. **Edit `CORS_ALLOWED_ORIGINS`:**
   ```
   Key: CORS_ALLOWED_ORIGINS
   Value: https://your-project.vercel.app
   ```
   *(Replace with your actual Vercel frontend URL)*

3. **Save changes**
4. **Redeploy backend** (Render will auto-redeploy or click "Manual Deploy")

---

## ✅ PART 4: Final Testing

### Test Your Live App

1. **Visit your Vercel URL**
2. **Try these queries:**
   - "Analyze Wakad"
   - "Compare Aundh and Akurdi"
   - "Show price trends for Ambegaon Budruk"

3. **Verify:**
   - ✅ Chat messages appear
   - ✅ Charts display
   - ✅ Tables show data
   - ✅ Download buttons work
   - ✅ Auto-scroll works

### Test Backend API

**In browser or terminal:**
```bash
# Test health
https://your-backend.onrender.com/api/health/

# Test localities
https://your-backend.onrender.com/api/localities/
```

---

## 📊 Deployment Checklist

### Backend (Render)
- [ ] Repository connected
- [ ] Service created with correct settings
- [ ] `SECRET_KEY` set
- [ ] `DEBUG=False` set
- [ ] `ALLOWED_HOSTS` set
- [ ] `CORS_ALLOWED_ORIGINS` set (with frontend URL)
- [ ] Backend deployed successfully
- [ ] Health endpoint returns `{"status": "ok"}`

### Frontend (Vercel)
- [ ] Repository imported
- [ ] Project configured (Vite, root: frontend)
- [ ] `VITE_API_URL` set (with backend URL)
- [ ] Frontend deployed successfully
- [ ] Can access frontend URL

### Integration
- [ ] Frontend can call backend API
- [ ] No CORS errors in browser console
- [ ] Queries work end-to-end
- [ ] Charts display correctly
- [ ] Download feature works

---

## 🎯 Quick Reference

### Your URLs:
- **Backend:** `https://real-estate-backend.onrender.com`
- **Frontend:** `https://your-project.vercel.app`

### Environment Variables:

**Render (Backend):**
```
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=real-estate-backend.onrender.com
CORS_ALLOWED_ORIGINS=https://your-project.vercel.app
OPENAI_API_KEY=sk-... (optional)
```

**Vercel (Frontend):**
```
VITE_API_URL=https://real-estate-backend.onrender.com
```

---

## 🐛 Common Issues & Fixes

### Issue: Backend build fails
**Fix:**
- Check Render build logs
- Verify `requirements.txt` exists
- Ensure `data/realestate.xlsx` is in repository
- Check Python version in `runtime.txt`

### Issue: CORS errors
**Fix:**
- Verify `CORS_ALLOWED_ORIGINS` has frontend URL (with `https://`)
- No trailing slash in URL
- Redeploy backend after changing CORS

### Issue: Frontend can't connect to backend
**Fix:**
- Check `VITE_API_URL` is set correctly
- Verify backend URL is accessible
- Check browser console for errors
- Ensure backend is deployed (not just building)

### Issue: Data not loading
**Fix:**
- Check `data/realestate.xlsx` is in repository
- Check Render logs for file loading errors
- Verify file path in `apps.py`

### Issue: 500 Internal Server Error
**Fix:**
- Check Render logs
- Verify `SECRET_KEY` is set
- Check all environment variables are correct

---

## 🎉 Success!

Once all steps are complete, your app is live! 

**Share your URLs:**
- Frontend: `https://your-project.vercel.app`
- Backend API: `https://real-estate-backend.onrender.com/api/`

---

## 📝 Notes

- **Free tiers:** Both Render and Vercel offer free tiers (perfect for this project)
- **Auto-deploy:** Both platforms auto-deploy on git push
- **Custom domains:** Can be added later in settings
- **Monitoring:** Check logs in both dashboards

---

## 🆘 Need Help?

1. **Check build logs** in Render/Vercel dashboards
2. **Check browser console** for frontend errors
3. **Verify environment variables** are set correctly
4. **Test locally first** before deploying
5. **Review error messages** carefully

**You're all set! 🚀**

