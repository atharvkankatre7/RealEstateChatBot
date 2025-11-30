# Deployment Guide

Complete guide for deploying the Real Estate Analysis Chatbot to production.

## 🎯 Deployment Overview

- **Backend**: Deploy to Render (or any Python hosting)
- **Frontend**: Deploy to Vercel (or any static hosting)

## 📦 Backend Deployment (Render)

### Step 1: Prepare Repository

Ensure your repository has:
- `backend/` directory with all Django files
- `backend/requirements.txt`
- `backend/Procfile`
- `backend/runtime.txt`
- `backend/data/realestate.xlsx`

### Step 2: Create Render Web Service

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `real-estate-backend` (or your choice)
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn backend.wsgi --log-file -`

### Step 3: Set Environment Variables

In Render dashboard, go to Environment tab and add:

```
SECRET_KEY=<generate-a-secure-secret-key>
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com
CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app
```

**Generate SECRET_KEY:**
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Step 4: Deploy

1. Click "Create Web Service"
2. Render will build and deploy automatically
3. Note your backend URL (e.g., `https://real-estate-backend.onrender.com`)

### Step 5: Verify Deployment

Visit: `https://your-backend.onrender.com/api/health/`

Should return:
```json
{
  "status": "ok",
  "data_loaded": true,
  "rows": 20
}
```

## 🎨 Frontend Deployment (Vercel)

### Step 1: Prepare Repository

Ensure your repository has:
- `frontend/` directory with all React files
- `frontend/package.json`
- `frontend/vercel.json`

### Step 2: Deploy via Vercel CLI

1. **Install Vercel CLI:**
   ```bash
   npm i -g vercel
   ```

2. **Login:**
   ```bash
   vercel login
   ```

3. **Navigate to frontend:**
   ```bash
   cd frontend
   ```

4. **Deploy:**
   ```bash
   vercel
   ```
   - Follow prompts
   - Set root directory: `frontend`
   - Confirm build settings

### Step 3: Deploy via Vercel Dashboard (Alternative)

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "Add New..." → "Project"
3. Import your GitHub repository
4. Configure:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
   - **Install Command**: `npm install`

### Step 4: Set Environment Variables

In Vercel dashboard, go to Settings → Environment Variables:

```
VITE_API_URL=https://your-backend.onrender.com
```

**Important:** Replace `your-backend.onrender.com` with your actual Render backend URL.

### Step 5: Redeploy

After setting environment variables:
- Go to Deployments tab
- Click "..." on latest deployment
- Click "Redeploy"

Or push a new commit to trigger automatic deployment.

### Step 6: Verify Deployment

Visit your Vercel URL and test:
- Query: "Analyze Wakad"
- Should display chart and table

## 🔄 Update CORS Settings

After deploying frontend, update backend CORS:

1. Go to Render dashboard → Environment Variables
2. Update `CORS_ALLOWED_ORIGINS`:
   ```
   CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app
   ```
3. Redeploy backend

## 🧪 Testing Deployment

### Test Backend:
```bash
curl https://your-backend.onrender.com/api/localities/
```

### Test Frontend:
1. Open your Vercel URL
2. Try queries:
   - "Analyze Wakad"
   - "Compare Aundh and Akurdi"
   - "Show price trends for Ambegaon Budruk"

## 🐛 Common Issues

### Backend Issues

**Issue: Data not loading**
- Check that `data/realestate.xlsx` is in repository
- Check Render build logs for errors
- Verify file path in `apps.py`

**Issue: CORS errors**
- Verify `CORS_ALLOWED_ORIGINS` includes frontend URL
- Check that frontend URL has `https://` prefix
- Redeploy backend after changing CORS settings

**Issue: 500 Internal Server Error**
- Check Render logs
- Verify all environment variables are set
- Check that `SECRET_KEY` is set

### Frontend Issues

**Issue: API calls failing**
- Verify `VITE_API_URL` is set correctly
- Check browser console for CORS errors
- Ensure backend is deployed and accessible

**Issue: Build fails**
- Check that all dependencies are in `package.json`
- Verify Node.js version (18+)
- Check Vercel build logs

**Issue: Charts not displaying**
- Check browser console for errors
- Verify Chart.js is installed
- Check that data is being received from API

## 📊 Monitoring

### Render Monitoring:
- View logs in Render dashboard
- Set up alerts for deployment failures
- Monitor resource usage

### Vercel Monitoring:
- View analytics in Vercel dashboard
- Check function logs
- Monitor build times

## 🔐 Security Checklist

- [ ] `DEBUG=False` in production
- [ ] Strong `SECRET_KEY` set
- [ ] `ALLOWED_HOSTS` configured
- [ ] CORS origins restricted to frontend domain
- [ ] Environment variables not committed to git
- [ ] HTTPS enabled (automatic on Render/Vercel)

## 🚀 Continuous Deployment

Both Render and Vercel support automatic deployments:

- **Render**: Deploys on push to main branch
- **Vercel**: Deploys on push to main branch

To disable auto-deploy:
- Render: Settings → Auto-Deploy → Disable
- Vercel: Settings → Git → Ignore Build Step

## 📝 Post-Deployment

1. Test all features
2. Monitor error logs
3. Set up error tracking (optional)
4. Configure custom domains (optional)
5. Set up SSL certificates (automatic on Render/Vercel)

## 🆘 Support

If deployment fails:
1. Check build logs
2. Verify all files are in repository
3. Check environment variables
4. Review error messages
5. Test locally first

